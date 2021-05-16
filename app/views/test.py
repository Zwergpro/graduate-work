import datetime
import os
import time
from contextlib import suppress

import numpy as np
from catboost import CatBoost
from flask import Blueprint, render_template, redirect, url_for, request, current_app
from matplotlib import pyplot as plt
from progressbar import progressbar
from sqlalchemy import desc

from collectors.dataset import DatasetCollector
from models import db
from models.dataset import Dataset, DatasetStatus
from models.test import Test, TestStatus
from models.train import Train, TrainStatus

bp = Blueprint('test', __name__, url_prefix='/test')


@bp.route('/', methods=('GET',))
def main():
    active_test = (
        Test.query
        .filter(Test.status == TestStatus.start)
        .order_by(desc(Test.dt_start))
        .first()
    )

    if active_test is not None:
        tests = Test.query.filter(Test.id != active_test.id).order_by(desc(Test.dt_start)).all()
    else:
        tests = Test.query.order_by(desc(Test.dt_start)).all()

    datasets = Dataset.query.filter(Dataset.status == DatasetStatus.end).order_by(desc(Dataset.dt_start)).all()
    trains = Train.query.filter(Train.status == TrainStatus.end).order_by(desc(Train.dt_start)).all()

    return render_template(
        'test/main_test.html',
        active_test=active_test,
        tests=tests,
        datasets=datasets,
        trains=trains,
    )


@bp.route('/delete/', methods=('POST',))
def delete():
    test_model = Test.query.get_or_404(ident=request.form.get('test_id', default=0))
    with suppress(FileNotFoundError, PermissionError):
        os.remove(test_model.path, dir_fd=True)

    local_session = db.session.object_session(test_model)
    local_session.delete(test_model)
    local_session.commit()
    return redirect(url_for('test.main'))


@bp.route('/start-test/', methods=('POST',))
def start_test():
    dataset_model = Dataset.query.get_or_404(ident=request.form.get('dataset_id', default=0))
    train_model = Train.query.get_or_404(ident=request.form.get('train_id', default=0))

    collector = DatasetCollector(dataset_model=dataset_model)

    dataset_name = 'test_' + str(time.time()).replace('.', '')
    test_dir = os.path.join(current_app.config['TEST_DIR'], dataset_name)
    os.makedirs(test_dir, exist_ok=True)

    test = Test(
        name=dataset_name,
        path=test_dir,
        dt_start=datetime.datetime.now(),
        status=TestStatus.start,
    )
    db.session.add(test)
    db.session.commit()

    annoy_index = collector.load_annoy_index()
    model = CatBoost()
    model.load_model(os.path.join(train_model.path, 'model.bin'))

    check_ds = collector.load_check_dataset()

    # user_data = get_test_data(min_appt=10)

    position_stat = []
    position_stat_after = []
    # position_stat_after_model = []
    # position_stat_after_vectors = []
    print('processing...')
    for data in progressbar(check_ds):
        # data = user_data[user]

        last_doctor = data['selected_doctor']
        town_doctors = data['suggested_doctors']
        all_appts = data['all_appts']

        if last_doctor not in town_doctors:
            continue

        index_of = town_doctors.index(last_doctor)
        if index_of > 200:
            continue

        position_stat.append(town_doctors.index(last_doctor))

        sort_func = get_sort_func(all_appts, annoy_index)
        town_doctors_1 = sort_doctors(town_doctors.copy(), model, sort_func, annoy_index)
        # town_doctors_2 = _sort_model(town_doctors.copy(), annoy_index, model)
        # town_doctors_3 = sorted(town_doctors.copy(), key=sort_func)

        position_stat_after.append(town_doctors_1.index(last_doctor))
        # position_stat_after_model.append(town_doctors_2.index(last_doctor))
        # position_stat_after_vectors.append(town_doctors_3.index(last_doctor))

    print_graphs(position_stat, position_stat_after, path=test.path)

    test.status = TestStatus.end
    test.dt_end = datetime.datetime.now()
    db.session.add(test)
    db.session.commit()

    return redirect(url_for('test.main'))


def print_graphs(before: list, after: list, path: str):
    print('-' * 30)
    print(np.mean(before))
    print_graph('before', np.array(before), os.path.join(path, 'before.png'))

    print('-' * 30)
    print(np.mean(after))
    print_graph('after', np.array(after), os.path.join(path, 'after.png'))


def print_graph(title, array, path):
    plt.title(title)
    plt.hist(array, 50)
    plt.ylabel('count')
    plt.xlabel('place')
    plt.grid(True)
    plt.savefig(path)


def get_sort_func(appts, a_index):
    def _sort_func(doctor_id):
        dists = []
        for doc_id in appts:
            dists.append(a_index.get_distance(doctor_id, doc_id))
        return min(dists) if dists else 999999

    return _sort_func


def _sort_model(data, vectors, model: CatBoost):
    data_arrays = []
    for doctor in data:
        data_arrays.append(vectors.get_item_vector(doctor))

    prob = model.predict(data_arrays)
    result = sorted(zip(data, prob), key=lambda x: x[1], reverse=True)
    return [x for x, _ in result]


def sort_doctors(data, model, sort_func, doctor_vectors):
    town_doctors = _sort_model(data, doctor_vectors, model)

    if len(town_doctors) < 11:
        return sorted(town_doctors, key=sort_func)

    town_doctors_pre = sorted(town_doctors[:10], key=sort_func)
    town_doctors_after = town_doctors[10:]
    return town_doctors_pre + town_doctors_after

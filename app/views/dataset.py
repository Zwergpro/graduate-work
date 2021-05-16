import datetime
import os
import time
import traceback
from contextlib import suppress

from flask import Blueprint, render_template, current_app, url_for, redirect, abort, jsonify, request
from sqlalchemy import desc

from collectors.dataset import DatasetCollector
from models import db
from models.appointment import Appointment
from models.dataset import Dataset, DatasetStatus, DatasetType
from redis_pool import redis_connection

bp = Blueprint('dataset', __name__, url_prefix='/dataset')


@bp.route('/', methods=('GET',))
def main():
    appt_count = Appointment.query.count()
    active_dataset = (
        Dataset.query
        .filter(Dataset.status == DatasetStatus.start)
        .order_by(desc(Dataset.dt_start))
        .first()
    )

    if active_dataset is not None:
        datasets = Dataset.query.filter(Dataset.id != active_dataset.id).order_by(desc(Dataset.dt_start)).all()
    else:
        datasets = Dataset.query.order_by(desc(Dataset.dt_start)).all()

    return render_template(
        'dataset/main_dataset.html',
        appt_count=appt_count,
        datasets=datasets,
        active_dataset=active_dataset,
    )


@bp.route('/delete/', methods=('POST',))
def delete():
    train_model = Dataset.query.get_or_404(ident=request.form.get('dataset_id', default=0))
    with suppress(FileNotFoundError, PermissionError):
        os.remove(train_model.path, dir_fd=True)

    local_session = db.session.object_session(train_model)
    local_session.delete(train_model)
    local_session.commit()
    return redirect(url_for('dataset.main'))


@bp.route('/stat/', methods=('GET',))
def stat():
    active_dataset = (
        Dataset.query
        .filter(Dataset.status == DatasetStatus.start)
        .order_by(desc(Dataset.dt_start))
        .first()
    )
    r_con = redis_connection()

    if active_dataset is None or not r_con.exists(DatasetCollector.DATASET_R_KEY.format(active_dataset.id)):
        abort(404)

    all_users = int(r_con.get(DatasetCollector.DATASET_ALL_R_KEY.format(active_dataset.id)))
    start_time = float(r_con.get(DatasetCollector.DATASET_START_R_KEY.format(active_dataset.id)))
    already_processed = int(r_con.get(DatasetCollector.DATASET_R_KEY.format(active_dataset.id)))

    return jsonify({
        'percent': (already_processed / all_users) * 100,
        'already_processed': already_processed,
        'all_users': all_users,
        'time_to_and': str(
            datetime.timedelta(seconds=int(
                ((time.time() - start_time) / already_processed) * (all_users - already_processed)),
            ),
        ),
    })


@bp.route('/create/', methods=('POST',))
def start_dataset_creating():
    start = datetime.datetime.now()
    dataset_name = 'dataset_' + str(time.time()).replace('.', '')
    dataset_dir = os.path.join(current_app.config['DATASET_DIR'], dataset_name)
    os.makedirs(dataset_dir, exist_ok=True)

    dataset = Dataset(
        name=dataset_name,
        path=dataset_dir,
        dt_start=start,
        status=DatasetStatus.start,
        type=DatasetType.top_one
    )
    db.session.add(dataset)
    db.session.commit()

    collector = DatasetCollector(dataset_model=dataset)

    try:
        # TODO: добавить параметры датасета
        collector.create_doctor_item_base_matrix()
        collector.create_datasets_for_catboost(min_appts=10)
    except Exception as e:
        traceback.print_exc()
        dataset.status = DatasetStatus.fail
        dataset.error = str(e)
    else:
        dataset.status = DatasetStatus.end
    finally:
        dataset.dt_end = datetime.datetime.now()
        db.session.add(dataset)
        db.session.commit()

    return redirect(url_for('dataset.main'))

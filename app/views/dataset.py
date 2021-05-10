import datetime
import os
import time
import traceback

from flask import Blueprint, render_template, current_app, url_for, redirect

from collectors.dataset import DatasetCollector
from models import db
from models.appointment import Appointment
from models.dataset import Dataset, DatasetStatus, DatasetType

bp = Blueprint('dataset', __name__, url_prefix='/dataset')


@bp.route('/', methods=('GET',))
def main():
    appt_count = Appointment.query.count()
    datasets = Dataset.query.order_by(Dataset.dt_start).all()
    return render_template('dataset/main_dataset.html', appt_count=appt_count, datasets=datasets)


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

    collector = DatasetCollector(dataset_dir=dataset_dir)

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

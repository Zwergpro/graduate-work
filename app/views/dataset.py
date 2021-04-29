from flask import Blueprint, render_template

from models.appointment import Appointment

bp = Blueprint('dataset', __name__, url_prefix='/dataset')


@bp.route('/', methods=('GET',))
def main():
    appt_count = Appointment.query.count()
    return render_template('dataset/main_dataset.html', appt_count=appt_count)

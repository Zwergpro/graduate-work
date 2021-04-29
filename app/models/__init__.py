from .base import db

from .doctor import Doctor
from .doctor_spec import DoctorSpec
from .doctor_town import DoctorTown
from .appointment import Appointment


def init_app(app):
    db.init_app(app)

from flask_migrate import Migrate
from .base import db

from models import appointment, doctor, doctor_spec, doctor_town, dataset, train


def init_app(app):
    db.init_app(app)
    Migrate(app, db)

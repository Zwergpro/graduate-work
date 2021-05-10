import enum

from app.models.base import db


class DatasetStatus(enum.Enum):
    start = 'start'
    end = 'end'
    fail = 'fail'


class DatasetType(enum.Enum):
    top_one = 'top_one'
    appt_docs = 'appt_docs'


class Dataset(db.Model):
    __tablename__ = 'dataset'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=50))
    path = db.Column(db.String(length=255))
    dt_start = db.Column(db.DateTime)
    dt_end = db.Column(db.DateTime)
    description = db.Column(db.Text)
    error = db.Column(db.Text)
    status = db.Column(db.Enum(DatasetStatus))
    type = db.Column(db.Enum(DatasetType))

    def __repr__(self):
        return f'<Dataset(id={self.id}, name={self.name})>'

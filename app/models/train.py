import enum

from app.models.base import db


class TrainStatus(enum.Enum):
    start = 'start'
    loading = 'loading'
    prepare = 'prepare'
    train = 'train'
    end = 'end'
    fail = 'fail'


class Train(db.Model):
    __tablename__ = 'train'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=50))
    path = db.Column(db.String(length=255))
    dt_start = db.Column(db.DateTime)
    dt_end = db.Column(db.DateTime)
    description = db.Column(db.Text)
    error = db.Column(db.Text)
    status = db.Column(db.Enum(TrainStatus))

    def __repr__(self):
        return f'<Train(id={self.id}, name={self.name})>'

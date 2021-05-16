import enum

from app.models.base import db


class TestStatus(enum.Enum):
    start = 'start'
    end = 'end'
    fail = 'fail'


class Test(db.Model):
    __tablename__ = 'test'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=50))
    path = db.Column(db.String(length=255))
    dt_start = db.Column(db.DateTime)
    dt_end = db.Column(db.DateTime)
    description = db.Column(db.Text)
    error = db.Column(db.Text)
    status = db.Column(db.Enum(TestStatus))

    def __repr__(self):
        return f'<Test(id={self.id}, name={self.name})>'

from app.models.base import db


class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    doctor_id = db.Column(db.Integer)
    spec_id = db.Column(db.Integer)
    dt_created = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Appt(user={self.user_id}, doctor={self.doctor_id})>'

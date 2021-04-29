from app.models.base import db


class DoctorTown(db.Model):
    __tablename__ = 'doctors_towns'

    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer)
    town_id = db.Column(db.Integer)
    spec_id = db.Column(db.Integer)
    wp_spec_id = db.Column(db.Integer)
    rating = db.Column(db.Numeric)

    def __repr__(self):
        return f'<DoctorTown(doctor={self.doctor_id})>'

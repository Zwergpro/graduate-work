from app.models.base import db


class DoctorSpec(db.Model):
    __tablename__ = 'doctor_spec'

    id = db.Column(db.Integer, primary_key=True)
    spec_id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return f'<Doctor_Spec(doctor={self.id}, spec={self.spec_id})>'

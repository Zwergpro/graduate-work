from typing import List, Tuple

from sqlalchemy import or_, desc, func

from src.db.models import Doctor, DoctorSpec, Appointment, DoctorTown


def get_town_list(session, town_id: int, spec_id: int) -> List[int]:
    doctors = (
        session
        .query(DoctorTown.doctor_id)
        .filter(DoctorTown.town_id == town_id)
        .filter(
            or_(DoctorTown.spec_id == spec_id, DoctorTown.wp_spec_id == spec_id)
        )
        .distinct()
        .order_by(desc(DoctorTown.rating))
    )

    return list(doc[0] for doc in doctors.all())


def get_last_appointment(session, user_id: int) -> Appointment:
    return (
        session
        .query(Appointment)
        .filter(Appointment.user_id == user_id)
        .order_by(desc(Appointment.dt_created))
        .first()
    )


def get_last_doctor(session, user_id: int) -> Doctor:
    last_appt = get_last_appointment(session, user_id)
    return session.query(Doctor).filter(Doctor.id == last_appt.doctor_id).first()


def get_last_doctor_with_all_in_town(session, user_id: int) -> Tuple[Doctor, List[int]]:
    last_doctor = get_last_doctor(session, user_id)
    town_doctors = get_town_list(session, last_doctor.town_id, last_doctor.spec_id)
    return last_doctor, town_doctors


def get_users(session, appt_count: int = 1) -> List[int]:
    return (
        session
        .query(Appointment.user_id)
        .group_by(Appointment.user_id)
        .having(func.count(Appointment.id) >= appt_count)
        .all()
    )

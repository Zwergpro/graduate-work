from typing import List, Tuple, Iterable

from sqlalchemy import or_, desc, func

from src.db.models import Doctor, DoctorSpec, Appointment, DoctorTown


def get_town_doctor_list(session, town_id: int, spec_id: int) -> List[int]:
    doctors = (
        session
        .query(DoctorTown.doctor_id)
        .filter(DoctorTown.town_id == town_id)
        .filter(DoctorTown.wp_spec_id == spec_id)
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


def get_all_appointments(session, user_id: int, exclude_doctor_ids: list) -> Iterable[Appointment]:
    return (
        session
        .query(Appointment)
        .filter(Appointment.user_id == user_id)
        .filter(~Appointment.doctor_id.in_(exclude_doctor_ids))
        .order_by(desc(Appointment.dt_created))
        .distinct()
    )


def get_all_appointment_users(session, min_appt=0) -> List[int]:
    doctors = (
        session
        .query(Appointment.user_id)
        .group_by(Appointment.user_id)
        .having(func.count(Appointment.doctor_id) > min_appt)
    )
    return list(doc[0] for doc in doctors.all())


def get_users_and_appointments(session) -> List:
    doctors = (
        session
        .query(Appointment.user_id, Appointment.doctor_id)
        .order_by(Appointment.user_id)
    )

    return doctors.all()


def get_last_doctor(session, user_id: int) -> Tuple[Appointment, Doctor]:
    last_appt = get_last_appointment(session, user_id)
    return last_appt, session.query(Doctor).filter(Doctor.id == last_appt.doctor_id).first()


def get_last_doctor_with_all_in_town(session, user_id: int) -> Tuple[Doctor, List[int], List[int]]:
    last_appt, last_doctor = get_last_doctor(session, user_id)
    town_doctors = list(set(get_town_doctor_list(session, last_doctor.town_id, last_appt.spec_id)))
    all_appts = list(set(get_all_appointments(session, user_id, [last_doctor.id])))
    return last_doctor, town_doctors, all_appts


def get_two_last_appointment(session, user_id: int) -> Tuple[Appointment, Appointment]:
    return (
        session
        .query(Appointment)
        .filter(Appointment.user_id == user_id)
        .order_by(desc(Appointment.dt_created))
        .all()
    )[:2]


def get_users(session, appt_count: int = 1) -> List[int]:
    users = (
        session
        .query(Appointment.user_id)
        .group_by(Appointment.user_id)
        .having(func.count(Appointment.id) >= appt_count)
        .all()
    )
    return [user[0] for user in users]

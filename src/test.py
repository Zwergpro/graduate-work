from sqlalchemy import or_, desc

from src.db.models import Doctor, DoctorSpec


# TODO: расположить записи на прием по дате (возможность взять последнюю запись)


def get_town_list(session, town_id, spec_id):
    doctors = (
        session
        .query(Doctor.id)
        .join(DoctorSpec, Doctor.spec_id == DoctorSpec.spec_id)
        .filter(Doctor.town_id == town_id)
        .filter(
            or_(Doctor.spec_id == spec_id, DoctorSpec.spec_id == spec_id)
        )
        .distinct()
        .order_by(desc(Doctor.rating))
    )

    return list(doc[0] for doc in doctors.all())

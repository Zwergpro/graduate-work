from progressbar import progressbar

from private.settings import PRIVATE_DIR
from src.db.base import Session
from src.db.fetcher import DB
from src.db.models import Appointment, Doctor, DoctorSpec

APPOINTMENTS = PRIVATE_DIR + '/sql/appointments.sql'
DOCTORS = PRIVATE_DIR + '/sql/doctors.sql'
DOCTOR_DF = PRIVATE_DIR + '/sql/df_data.sql'
DOCTOR_SPEC = PRIVATE_DIR + '/sql/doctor_spec.sql'


def fetch_appts(session):
    with DB() as cursor:
        print(f'fetching appointments...')
        with open(APPOINTMENTS, 'r') as f:
            query = f.read()
        cursor.execute(query)

        for appt in progressbar(cursor.fetchall()):
            session.add(
                Appointment(
                    user_id=appt[0],
                    doctor_id=appt[1],
                    spec_id=appt[2],
                    dt_created=appt[3],
                )
            )


def fetch_doctor_spec(session):
    with DB() as cursor:
        print(f'fetching doctor_spec...')
        with open(DOCTOR_SPEC, 'r') as f:
            query = f.read()
        cursor.execute(query)

        for doc_spec in progressbar(cursor.fetchall()):
            session.add(
                DoctorSpec(
                    id=doc_spec[0],
                    spec_id=doc_spec[1],
                ),
            )


def fetch_doctors(session):
    with DB() as cursor:
        print(f'fetching doctors...')
        with open(DOCTORS, 'r') as f:
            query = f.read()
        cursor.execute(query)

        for doctor in progressbar(cursor.fetchall()):
            session.add(
                Doctor(
                    id=doctor[0],
                    spec_id=doctor[1],
                    town_id=doctor[2],
                    gender=doctor[3],
                    experience=doctor[4],
                    science=doctor[5],
                    category=doctor[6],
                    position=doctor[7],
                    rating=doctor[8],
                    stars=doctor[9],
                    official_rating=doctor[10],
                    rates=doctor[11],
                    drugrates=doctor[12],
                    answers=doctor[13],
                    extrainfo=doctor[14],
                    bio=doctor[15],
                    hobby=doctor[16],
                    comments=doctor[17],
                    appointment_count=doctor[18],
                    has_owner=doctor[19],
                    lpu_pro=doctor[20],
                    min_price=doctor[21],
                    min_price_go=doctor[22],
                    min_price_online=doctor[23],
                    hits=doctor[24],
                    friendliness=doctor[25],
                    osmotr=doctor[26],
                    efficiency=doctor[27],
                    informativity=doctor[28],
                    recommend=doctor[29],
                    spec_in_title=doctor[30],
                    rate_count=doctor[31],
                    pos=doctor[32],
                    net=doctor[33],
                    neg=doctor[34],
                    wp_count=doctor[35],
                    min_price_2=doctor[36],
                    min_discount=doctor[37],
                    age_min=doctor[38],
                    age_max=doctor[39],
                    avatar=doctor[40],
                    spec_count=doctor[41],
                    ed_count=doctor[42],
                    course_count=doctor[43],
                    honor_count=doctor[44],
                    job_count=doctor[45],
                )
            )


if __name__ == '__main__':
    print('start fetching')
    session = Session()
    print('session start')

    session.execute('TRUNCATE appointments RESTART IDENTITY;')
    print('appointments truncated')
    fetch_appts(session)
    session.commit()
    print('appointments done')

    session.execute('TRUNCATE doctor_spec RESTART IDENTITY;')
    print('doctor_spec truncated')
    fetch_doctor_spec(session)
    session.commit()
    print('doctor_spec done')

    session.execute('TRUNCATE doctors RESTART IDENTITY;')
    print('doctors truncated')
    fetch_doctors(session)
    session.commit()
    print('doctors done')

    session.execute('TRUNCATE doctors_towns RESTART IDENTITY;')
    print('doctors_towns truncated')
    session.execute("""
    insert into doctors_towns (doctor_id, town_id, spec_id, wp_spec_id, rating)
    SELECT
        doctors.id as doctor_id,
        doctors.town_id,
        doctors.spec_id,
        doctor_spec.spec_id as wp_spec_id,
        doctors.rating
    FROM doctors
    JOIN doctor_spec ON doctors.id = doctor_spec.id;
    """)
    session.commit()
    print('doctors_towns done')

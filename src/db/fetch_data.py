import json
import math

from progressbar import progressbar

from private.settings import PRIVATE_DIR
from src.db.base import Session
from src.db.fetcher import DB
from src.db.models import Appointment, Doctor, DoctorSpec

APPOINTMENTS = PRIVATE_DIR + '/sql/appointments.sql'
DOCTORS = PRIVATE_DIR + '/sql/doctors.sql'
DOCTOR_DF = PRIVATE_DIR + '/sql/df_data.sql'
DOCTOR_SPEC = PRIVATE_DIR + '/sql/doctor_spec.sql'

DOCTOR_DF_JSON = PRIVATE_DIR + 'vectors/df.json'
DOCTOR_IDF_JSON = PRIVATE_DIR + 'vectors/idf.json'


def fetch_doctor_df():
    with DB() as cursor:
        print(f'fetching doctor DF...')
        with open(DOCTOR_DF, 'r') as f:
            query = f.read()
        cursor.execute(query)

        result = cursor.fetchone()

        doctor_df = {
            'all_count': result[0],
            'gender': result[1],
            'experience': result[2],
            'science': result[3],
            'category': result[4],
            'position': result[5],
            'rating': result[6],
            'stars': result[7],
            'official_rating': result[8],
            'rates': result[9],
            'drugrates': result[10],
            'answers': result[11],
            'extrainfo': result[12],
            'bio': result[13],
            'hobby': result[14],
            'comments': result[15],
            'appointment_count': result[16],
            'has_owner': result[17],
            'lpu_pro': result[18],
            'min_price': result[19],
            'min_price_go': result[20],
            'min_price_online': result[21],
            'hits': result[22],
            'friendliness': result[23],
            'osmotr': result[24],
            'efficiency': result[25],
            'informativity': result[26],
            'recommend': result[27],
            'spec_in_title': result[28],
            'rate_count': result[29],
            'pos': result[30],
            'net': result[31],
            'neg': result[32],
            'wp_count': result[33],
            'min_price_2': result[34],
            'min_discount': result[35],
            'age_min': result[36],
            'age_max': result[37],
            'avatar': result[38],
            'spec_count': result[39],
            'ed_count': result[40],
            'course_count': result[41],
            'honor_count': result[42],
            'job_count': result[43],
        }

    # with open(DOCTOR_DF_JSON, 'w') as file:
    #     json.dump(doctor_df, file)

    all_count = doctor_df.pop('all_count')
    IDF = list(map(lambda x: math.log10(all_count / x) if x != 0 else 0, result[1:]))

    with open(DOCTOR_IDF_JSON, 'w') as file:
        json.dump(IDF, file)


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
                    dt_created=appt[2],
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

    # TODO: переписать с использованием csv
    #
    # print('start fetching')
    session = Session()
    # print('session start')
    #
    # print('fetch df/idf')
    # fetch_doctor_df()
    #
    # session.execute('TRUNCATE appointments RESTART IDENTITY;')
    # print('appointments truncated')
    # fetch_appts(session)
    # session.commit()
    # print('appointments done')
    #
    # session.execute('TRUNCATE doctor_spec RESTART IDENTITY;')
    # print('doctor_spec truncated')
    # fetch_doctor_spec(session)
    # session.commit()
    # print('doctor_spec done')
    #
    # session.execute('TRUNCATE doctors RESTART IDENTITY;')
    # print('doctors truncated')
    # fetch_doctors(session)
    # session.commit()
    # print('doctors done')

    session.execute('TRUNCATE doctors_towns RESTART IDENTITY;')
    print('doctors truncated')

    # session.execute("""
    # copy (
    #     SELECT DISTINCT
    #         doctors.id as doctor_id,
    #         doctors.town_id,
    #         doctors.spec_id,
    #         doctor_spec.spec_id as wp_spec_id,
    #         doctors.rating
    #     FROM doctors
    #     JOIN doctor_spec ON doctors.id = doctor_spec.id
    # ) to '{}sql/doctors_towns.csv' DELIMITER ',' CSV HEADER;
    # """.format(PRIVATE_DIR))
    # print('doctors truncated')

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
    print('doctors done')

from progressbar import progressbar

from private.settings import PRIVATE_DIR
from src.db.base import Session
from src.db.fetcher import DB
from src.db.models import Appointment


APPOINTMENTS = PRIVATE_DIR + '/appointments.sql'
DOCTORS = PRIVATE_DIR + '/doctors.sql'


def fetch_appt(session):
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
                )
            )


if __name__ == '__main__':
    session = Session()
    session.execute('TRUNCATE appointments;')
    fetch_appt(session)
    session.commit()

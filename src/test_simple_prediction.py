import numpy as np
from progressbar import progressbar

from src.vectors import UserVector, DoctorVector
from src.test import get_users, get_last_doctor_with_all_in_town

from db.base import Session


def get_test_data(session):
    users = get_users(session, 5)

    user_data = {}
    print('prepare data')
    for user in progressbar(users):
        last_doctor, town_doctors = get_last_doctor_with_all_in_town(session, user)
        user_data[user[0]] = {
            'last_doctor': last_doctor,
            'town_doctors': town_doctors
        }
    print()
    return user_data


def test_prediction():
    session = Session()
    user_data = get_test_data(session)

    # doctor_vectors = DoctorVector()
    # doctor_vectors.load()
    # user_vectors = UserVector()
    # user_vectors.load()

    position_stat = []
    print('processing...')
    for user in progressbar(user_data.keys()):
        data = user_data[user]

        last_doctor = data['last_doctor']
        town_doctors = data['town_doctors']

        position_stat.append(town_doctors.index(last_doctor.id))
        print(town_doctors.index(last_doctor.id))

    print(np.mean(position_stat))


if __name__ == '__main__':
    test_prediction()

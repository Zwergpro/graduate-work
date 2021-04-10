import json
import os
from typing import Callable, Optional, Tuple

import numpy as np
import pandas as pd
from catboost import CatBoost
from matplotlib import pyplot as plt
from progressbar import progressbar

from db.base import Session
from db.models import Doctor
from private.settings import PRIVATE_DIR
from src.vectors import DoctorVector
from src.db_func import (
    get_users, get_last_doctor_with_all_in_town, get_all_appointment_users,
    get_town_doctor_list, get_all_appointments, get_two_last_appointment,
)


def print_graphs(before: list, after: list):
    print('-' * 30)
    print(np.mean(before))
    print_graph('before', np.array(before))

    print('-' * 30)
    print(np.mean(after))
    print_graph('after', np.array(after))

    fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)

    axs[0].hist(np.array(before), bins=20)
    axs[1].hist(np.array(after), bins=20)
    plt.show()


def print_graph(title, array):
    plt.title(title)
    plt.hist(array, 50)
    plt.ylabel('count')
    plt.xlabel('place')
    plt.grid(True)
    plt.show()


def test_model(data: dict, model: CatBoost, sort_func: Callable, max_sort_limit: Optional[int] = None) -> None:
    """Simple test for model."""
    doctor_vectors = DoctorVector()
    doctor_vectors.load()

    position_stat = []
    position_stat_after = []

    for user, test_data in progressbar(data.items()):
        last_doctor = test_data['selected_doctor']
        town_doctors = test_data['suggested_doctors']

        index_of = town_doctors.index(last_doctor)
        if max_sort_limit is not None and index_of > max_sort_limit:
            continue

        position_stat.append(town_doctors.index(last_doctor))

        sorted_docs, docs = town_doctors[:max_sort_limit], town_doctors[max_sort_limit:]
        town_doctors = sort_func(sorted_docs, doctor_vectors, model)

        final_doctors = town_doctors + docs
        position_stat_after.append(final_doctors.index(last_doctor))

    print_graphs(position_stat, position_stat_after)
    print(len(position_stat))


def create_train_data(min_appts: int) -> Tuple[pd.DataFrame, pd.DataFrame]:
    session = Session()
    all_users = get_all_appointment_users(session, min_appts)

    doctor_vectors = DoctorVector()
    doctor_vectors.load()

    test = []
    train = []

    for user in progressbar(all_users):
        # add test data
        last_appt, test_appt = get_two_last_appointment(session, user)

        test_doctor_model = session.query(Doctor).filter(Doctor.id == test_appt.doctor_id).first()
        test_doctors = get_town_doctor_list(session, test_doctor_model.town_id, test_appt.spec_id)
        for doctor in test_doctors[:100]:
            if doctor == test_doctor_model.id:
                continue
            test.append([0, user, *doctor_vectors[doctor]])
        test.append([1, user, *doctor_vectors[test_doctor_model.id]])

        # add train data
        all_user_appts = get_all_appointments(session, user, [last_appt.doctor_id, test_appt.doctor_id])
        for appt in all_user_appts:
            train.append([1, user, *doctor_vectors[appt.doctor_id]])

            train_doctor_model = session.query(Doctor).filter(Doctor.id == appt.doctor_id).first()
            train_town_doctors = get_town_doctor_list(session, train_doctor_model.town_id, appt.spec_id)
            for doctor in train_town_doctors[:20]:
                if doctor == train_doctor_model.id:
                    continue
                train.append([0, user, *doctor_vectors[doctor]])

    test_df = pd.DataFrame(test)
    train_df = pd.DataFrame(train)

    return test_df, train_df


def get_train_data(min_appts=0, flush=False):
    train_path = os.path.join(PRIVATE_DIR, 'ranking', f'train_data_{min_appts}.csv')
    test_path = os.path.join(PRIVATE_DIR, 'ranking', f'test_data_{min_appts}.csv')

    if os.path.exists(train_path) and os.path.exists(test_path) and not flush:
        train_df = pd.read_csv(train_path, header=None)
        test_df = pd.read_csv(test_path, header=None)
    else:
        test_df, train_df = create_train_data(min_appts)
        test_df.to_csv(test_path, index=False, header=False)
        train_df.to_csv(train_path, index=False, header=False)

    return test_df, train_df


def get_test_data(min_appt=5):
    file_path = os.path.join(PRIVATE_DIR, 'vectors', f'test_data_{min_appt}.json')

    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)

    session = Session()
    users = get_users(session, min_appt)

    user_data = {}
    for user in progressbar(users):
        last_doctor, town_doctors, all_appts = get_last_doctor_with_all_in_town(session, user)
        if last_doctor.id not in town_doctors:
            continue
        user_data[user] = {
            'selected_doctor': last_doctor.id,
            'suggested_doctors': town_doctors,
            'all_appts': [appt.doctor_id for appt in all_appts],
        }

    with open(file_path, 'w') as f:
        json.dump(user_data, f)
    print('len ->', len(user_data))
    return user_data

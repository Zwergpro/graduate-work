import os
from typing import Tuple, Dict, List

import pandas as pd
from annoy import AnnoyIndex
from sklearn.preprocessing import MinMaxScaler
from sqlalchemy import desc, func
from sqlalchemy.orm import load_only

from models.appointment import Appointment
from models.doctor import Doctor
from models.doctor_town import DoctorTown


class AnnoySettings:
    ITEMS = 43
    METRIC = 'angular'
    TREES = 10
    JOBS = 4


DOCTORS_CSV = 'doctors.csv'
DOCTORS_ANN = 'doctor_item_base.ann'
TEST_DATASET = 'test_dataset.csv'
TRAIN_DATASET = 'train_dataset.csv'
CHECK_DATASET = 'check_dataset.csv'


class DatasetCollector:
    """Класс для создания тренировочных и проверочных данных"""

    def __init__(self, dataset_dir: str):
        self.dataset_dir = dataset_dir
        self.annoy_index = None

    def create_doctor_item_base_matrix(self, save: bool = True) -> Tuple[pd.DataFrame, AnnoyIndex]:
        """Создание item base матрицы врачей и сохранение в индексе annoy и csv"""
        data = pd.DataFrame.from_records(Doctor.query.order_by(Doctor.id).all())

        ids = data.iloc[:, 0]
        # Производим нормализацию (MinMaxScaler переносит все точки на отрезок (0, 1))
        features = pd.DataFrame.from_records(MinMaxScaler().fit_transform(data.iloc[:, 3:]))

        matrix_data = pd.concat([ids, features], axis=1)

        self.annoy_index = AnnoyIndex(AnnoySettings.ITEMS, AnnoySettings.METRIC)
        for doc_id, doc_feature in zip(ids.values, features.values):
            self.annoy_index.add_item(doc_id, doc_feature)

        self.annoy_index.build(AnnoySettings.TREES, AnnoySettings.JOBS)

        if save:
            matrix_data.to_csv(self.get_save_path(DOCTORS_CSV), header=False, index=False)
            self.annoy_index.save(self.get_save_path(DOCTORS_ANN))

        return matrix_data, self.annoy_index

    def get_save_path(self, file_name: str) -> str:
        return os.path.join(self.dataset_dir, file_name)

    @staticmethod
    def get_appts_by_user(user_id: int) -> List[Appointment]:
        """Получает список записей на прием"""
        appts = (
            Appointment.query
            .options(load_only('id', 'doctor_id', 'spec_id'))
            .filter(Appointment.user_id == user_id)
            .order_by(desc(Appointment.dt_created))
            .distinct()
            .all()
        )
        return [appt for appt in appts]

    @staticmethod
    def get_users(min_appt=1) -> List[int]:
        """Получает список пользователей, у которых записей на прием не меньше, чем min_appt"""
        users = (
            Appointment.query
            .with_entities(Appointment.user_id)
            .group_by(Appointment.user_id)
            .having(func.count(Appointment.doctor_id) >= min_appt)
        )
        return [user[0] for user in users.all()]

    @staticmethod
    def get_doctor_towns() -> Dict[int, int]:
        """Получаем докторов и их города"""
        doctors = Doctor.query.with_entities(Doctor.id, Doctor.town_id).all()
        return {doctor_id: town_id for doctor_id, town_id in doctors}

    @staticmethod
    def get_town_doctor_list(town_id: int, spec_id: int, exclude: Tuple[int]) -> List[int]:
        """Получает список врачей в городе по заданной специальности исключая exclude"""
        doctors = (
            DoctorTown.query
            .with_entities(DoctorTown.doctor_id)
            .filter(DoctorTown.town_id == town_id)
            .filter(DoctorTown.wp_spec_id == spec_id)
            .filter(~DoctorTown.doctor_id.in_(exclude))
            .order_by(desc(DoctorTown.rating))
            .distinct()
        )
        return [doc[0] for doc in doctors.all()]

    def set_appt_dataset(self, to_list, doc_towns, appt) -> None:
        doctors = self.get_town_doctor_list(doc_towns[appt.doctor_id], appt.spec_id, exclude=(appt.doctor_id,))
        for doctor in doctors[:100]:
            to_list.append([0, appt.id, *self.annoy_index.get_item_vector(doctor)])
        to_list.append([1, appt.id, *self.annoy_index.get_item_vector(appt.doctor_id)])

    def create_datasets_for_catboost(
        self,
        min_appts: int = 1,
        save: bool = True
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Создает датасет для тренировки и тестирования"""
        assert self.annoy_index is not None, 'annoy_index does not exist'

        all_users = self.get_users(min_appts)
        doc_towns = self.get_doctor_towns()

        test, train, check = [], [], []

        # TODO: добавить отслеживание прогресса
        for user in all_users:
            last_appt, *old_appts = self.get_appts_by_user(user)
            check.append(last_appt.id)

            if not old_appts:
                continue

            test_appt, *train_user_appts = old_appts

            self.set_appt_dataset(test, doc_towns, test_appt)

            for appt in train_user_appts:
                self.set_appt_dataset(train, doc_towns, appt)

        test_df = pd.DataFrame(test)
        train_df = pd.DataFrame(train)
        check_df = pd.DataFrame(check)

        if save:
            test_df.to_csv(self.get_save_path(TEST_DATASET), header=False, index=False)
            train_df.to_csv(self.get_save_path(TRAIN_DATASET), header=False, index=False)
            check_df.to_csv(self.get_save_path(CHECK_DATASET), header=False, index=False)

        return test_df, train_df, check_df

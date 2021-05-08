import os
from typing import Tuple

import pandas as pd
from annoy import AnnoyIndex
from sklearn.preprocessing import MinMaxScaler

from db.models import Doctor


class AnnoySettings:
    ITEMS = 43
    METRIC = 'angular'
    TREES = 10
    JOBS = 4


DOCTORS_CSV = 'doctors.csv'
DOCTORS_ANN = 'doctor_item_base.ann'


class DatasetCollector:
    """Класс для создания тренировочных и проверочных данных"""

    def __init__(self, dataset_dir):
        self.dataset_dir = dataset_dir

    def create_doctor_item_base_matrix(self) -> Tuple[pd.DataFrame, AnnoyIndex]:
        """Создание item base матрицы врачей и сохранение в индексе annoy и csv"""
        data = pd.DataFrame.from_records(Doctor.query.order_by(Doctor.id).all())

        ids = data.iloc[:, 0]
        # Производим нормализацию (MinMaxScaler переносит все точки на отрезок (0, 1))
        features = pd.DataFrame.from_records(MinMaxScaler().fit_transform(data.iloc[:, 3:]))

        matrix_data = pd.concat([ids, features], axis=1)
        matrix_data.to_csv(self.get_save_path(DOCTORS_CSV), header=False, index=False)

        annoy_index = AnnoyIndex(AnnoySettings.ITEMS, AnnoySettings.METRIC)
        for doc_id, doc_feature in zip(ids, features):
            annoy_index.add_item(doc_id, doc_feature)

        annoy_index.build(AnnoySettings.TREES, AnnoySettings.JOBS)
        annoy_index.save(self.get_save_path(DOCTORS_ANN))

        return matrix_data, annoy_index

    def get_save_path(self, file_name: str) -> str:
        return os.path.join(self.dataset_dir, file_name)

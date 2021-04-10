import json
import os

import pandas as pd
import progressbar
from sklearn.preprocessing import MinMaxScaler

from db.base import Session
from db.models import Doctor
from private.settings import PRIVATE_DIR


class DoctorVector:
    FILEPATH = PRIVATE_DIR + 'vectors/doctor_vectors.json'

    _vectors = None

    def load(self):
        if not os.path.exists(self.FILEPATH):
            self.create()
            self.save()
            return

        with open(self.FILEPATH, 'r') as f_vectors:
            self._vectors = json.load(f_vectors)

    def save(self):
        with open(self.FILEPATH, 'w') as f_vectors:
            json.dump(self._vectors, f_vectors)

    def create(self):
        session = Session()
        data = pd.DataFrame.from_records(
            session.query(Doctor).order_by(Doctor.id).all(),
            columns=Doctor._fields
        )

        doctor_stats = data.iloc[:, [0, 1, 2]]
        matrix = MinMaxScaler().fit_transform(data.iloc[:, 3:])

        doctors = {}
        progress = progressbar.ProgressBar(max_value=data.shape[0])
        for stat, values in zip(doctor_stats.iterrows(), matrix):
            doctors[str(int(stat[1][0]))] = values.tolist()
            progress.next()

        self._vectors = doctors

    def __getitem__(self, item):
        return self._vectors[str(item)]

    def items(self):
        return self._vectors.items()

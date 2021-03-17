import json

import numpy as np
import progressbar

from db.base import Session
from db.models import Appointment
from private.settings import PRIVATE_DIR
from vectors.doctors import DoctorVector


class UserVector:
    FILEPATH = PRIVATE_DIR + 'vectors/user_vectors.json'

    _vectors = None

    def load(self):
        with open(self.FILEPATH, 'r') as f_vectors:
            self._vectors = json.load(f_vectors)

    def save(self):
        with open(self.FILEPATH, 'w') as f_vectors:
            json.dump(self._vectors, f_vectors)

    def create(self):
        doctor_vectors = DoctorVector()
        doctor_vectors.load()

        session = Session()

        appts = {}
        for appt in session.query(Appointment.user_id, Appointment.doctor_id).all():
            appts.setdefault(str(appt.user_id), []).append(int(appt.doctor_id))

        users_vectors = {}
        progress = progressbar.ProgressBar(max_value=len(appts))
        for user_id, doctor_ids in appts.items():
            vectors = [doctor_vectors[doctor_id] for doctor_id in doctor_ids]
            users_vectors[user_id] = np.sum(vectors, axis=0).tolist()
            progress.update(progress.value + 1)

        self._vectors = users_vectors

    def __getitem__(self, item):
        return self._vectors[str(item)]

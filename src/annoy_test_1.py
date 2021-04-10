from itertools import chain

from annoy import AnnoyIndex
from progressbar import progressbar

from db.base import Session
from private.settings import PRIVATE_DIR
from src.test_simple_prediction import get_test_data, print_graphs
from src.vectors import DoctorVector

ITEMS = 43
METRIC = 'angular'
TREES = 10
JOBS = 4


def build_model():
    doctor_vectors = DoctorVector()
    doctor_vectors.load()

    a_index = AnnoyIndex(ITEMS, METRIC)
    for doc, vector in doctor_vectors.items():
        a_index.add_item(int(doc), vector)

    a_index.build(TREES, JOBS)
    a_index.save(f'{PRIVATE_DIR}annoy_db/{METRIC}.ann')


def get_sort_func(appts, a_index):
    def _sort_func(doctor_id):
        dists = []

        if not appts:
            return 0

        _min_doctor_id = None
        _min = 1000000
        for doc_id in appts:
            dist = a_index.get_distance(doctor_id, doc_id)
            if dist < _min or _min_doctor_id is None:
                _min = dist
                _min_doctor_id = doc_id

        for doc_id in chain(appts, a_index.get_nns_by_item(_min_doctor_id, 10)):
            dists.append(a_index.get_distance(doctor_id, doc_id))
        return sum(dists) if dists else 0

    return _sort_func


if __name__ == '__main__':
    """Простой тест с моделькой annoy"""
    build_model()

    annoy_index = AnnoyIndex(ITEMS, METRIC)
    annoy_index.load(f'{PRIVATE_DIR}annoy_db/{METRIC}.ann')

    session = Session()
    user_data = get_test_data(session)

    # user_vectors = UserVector()
    # user_vectors.load()

    position_stat = []
    position_stat_after = []
    print('processing...')
    for user in progressbar(user_data.keys()):
        data = user_data[user]

        last_doctor = data['last_doctor']
        town_doctors = data['town_doctors']
        all_appts = data['all_appts']

        if last_doctor not in town_doctors:
            continue

        index_of = town_doctors.index(last_doctor)
        if index_of < 200:
            position_stat.append(town_doctors.index(last_doctor))

        sort_func = get_sort_func(all_appts, annoy_index)

        town_doctors.sort(key=sort_func)

        index_of = town_doctors.index(last_doctor)
        if index_of < 200:
            position_stat_after.append(town_doctors.index(last_doctor))

    print_graphs(position_stat, position_stat_after)

# angular 61.653031049778214 31.320811419984974
# euclidean 61.653031049778214 32.68842504743833

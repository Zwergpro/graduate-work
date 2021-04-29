import numpy as np
from annoy import AnnoyIndex
from catboost import CatBoost
from progressbar import progressbar

from private.settings import PRIVATE_DIR
from src.test_utils import get_test_data, print_graphs
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
        for doc_id in appts:
            dists.append(a_index.get_distance(doctor_id, doc_id))
        return min(dists) if dists else 999999

    return _sort_func


def _sort_model(data, vectors, model: CatBoost):
    data_arrays = []
    for doctor in data:
        data_arrays.append(vectors[doctor])

    prob = model.predict(data_arrays)
    result = sorted(zip(data, prob), key=lambda x: x[1], reverse=True)
    return [x for x, _ in result]


def sort_doctors(data, model, sort_func, doctor_vectors):
    town_doctors = _sort_model(data, doctor_vectors, model)

    town_doctors_pre = sorted(town_doctors[:10], key=sort_func)
    town_doctors_after = town_doctors[10:]
    return town_doctors_pre + town_doctors_after


if __name__ == '__main__':
    build_model()
    annoy_index = AnnoyIndex(ITEMS, METRIC)
    annoy_index.load(f'{PRIVATE_DIR}annoy_db/{METRIC}.ann')

    user_data = get_test_data(min_appt=3)

    doctor_vectors = DoctorVector()
    doctor_vectors.load()

    model = CatBoost()
    model.load_model(f'{PRIVATE_DIR}ranking/top_one_model_QuerySoftMax_3.cbm')

    position_stat = []
    position_stat_after = []
    position_stat_after_model = []
    position_stat_after_vectors = []
    print('processing...')
    for user in progressbar(user_data.keys()):
        data = user_data[user]

        last_doctor = data['selected_doctor']
        town_doctors = data['suggested_doctors']
        # last_doctor = data['last_doctor']
        # town_doctors = data['town_doctors']
        all_appts = data['all_appts']

        if last_doctor not in town_doctors:
            continue

        index_of = town_doctors.index(last_doctor)
        if index_of > 200:
            continue

        position_stat.append(town_doctors.index(last_doctor))

        sort_func = get_sort_func(all_appts, annoy_index)
        town_doctors_1 = sort_doctors(town_doctors.copy(), model, sort_func, doctor_vectors)
        town_doctors_2 = _sort_model(town_doctors.copy(), doctor_vectors, model)
        town_doctors_3 = sorted(town_doctors.copy(), key=sort_func)

        position_stat_after.append(town_doctors_1.index(last_doctor))
        position_stat_after_model.append(town_doctors_2.index(last_doctor))
        position_stat_after_vectors.append(town_doctors_3.index(last_doctor))

    print_graphs(position_stat, position_stat_after)
    print('-' * 30)
    print('all ->', np.mean(position_stat_after))
    print('model ->', np.mean(position_stat_after_model))
    print('vector ->', np.mean(position_stat_after_vectors))

# angular 61.653031049778214 31.320811419984974

# 48.0007408201659
# top 10 - first 10
# all -> 12.523424878836833
# model -> 11.617393645665052
# vector -> 31.997576736672052


# top 3 - first 20 - min
# all -> 11.512881498016357
# model -> 9.063905486943044
# vector -> 30.44671456004055

# top 3 - first 20 - sum
# all -> 11.428856894988742
# model -> 9.063905486943044
# vector -> 29.46620982756436

# top 3 - first 10 - sum
# all -> 9.957110411447621
# model -> 9.063905486943044
# vector -> 29.46620982756436

# top 3 - first 10 - min


# top 3 - first 10 - min
# all -> 11.512881498016357
# model -> 9.063905486943044
# vector -> 30.44671456004055

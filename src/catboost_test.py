from catboost import CatBoost

from private.settings import PRIVATE_DIR
from src.test_utils import test_model, get_test_data

MIN_APPTS_MODEL = 10
LOSS_FUNCTION = 'RMSE'
MIN_APPTS = 10
SORT_LIMIT = 200


def sort(data, vectors, model: CatBoost):
    data_arrays = []
    for doctor in data:
        data_arrays.append(vectors[doctor])

    prob = model.predict(data_arrays)
    result = sorted(zip(data, prob), key=lambda x: x[1], reverse=True)
    return [x for x, _ in result]


def main():
    model_path = f'{PRIVATE_DIR}ranking/model_{LOSS_FUNCTION}_{MIN_APPTS_MODEL}.cbm'
    model = CatBoost()
    model.load_model(model_path)

    data = get_test_data(min_appt=MIN_APPTS)

    test_model(data, model, sort, max_sort_limit=SORT_LIMIT)


if __name__ == '__main__':
    main()

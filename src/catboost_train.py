import os
from copy import deepcopy

from catboost import CatBoost, Pool

from private.settings import PRIVATE_DIR
from test_utils import get_train_data

MIN_APPTS = 3
LOSS_FUNCTION = 'RMSE'


def main():
    model_path = os.path.join(PRIVATE_DIR, 'ranking', f'model_{LOSS_FUNCTION}_{MIN_APPTS}.cbm')

    test_df, train_df = get_train_data(MIN_APPTS)

    X_train = train_df.drop([0, 1], axis=1).values
    y_train = train_df[0].values
    queries_train = train_df[1].values

    X_test = test_df.drop([0, 1], axis=1).values
    y_test = test_df[0].values
    queries_test = test_df[1].values

    train = Pool(
        data=X_train,
        label=y_train,
        group_id=queries_train
    )

    test = Pool(
        data=X_test,
        label=y_test,
        group_id=queries_test
    )

    default_parameters = {
        'iterations': 2000,
        'custom_metric': ['NDCG', 'PFound', 'AverageGain:top=10'],
        'verbose': False,
        'random_seed': 0,
    }

    def fit_model(loss_function: str, additional_params=None, train_pool=train, test_pool=test):
        parameters = deepcopy(default_parameters)
        parameters['loss_function'] = loss_function
        parameters['train_dir'] = os.path.join(PRIVATE_DIR, 'train', loss_function)

        if additional_params is not None:
            parameters.update(additional_params)

        model = CatBoost(parameters)
        model.fit(train_pool, eval_set=test_pool, plot=True)

        return model

    model = fit_model(LOSS_FUNCTION, {'custom_metric': ['PrecisionAt:top=5', 'RecallAt:top=5', 'MAP:top=5']})
    model.save_model(model_path)


if __name__ == '__main__':
    main()

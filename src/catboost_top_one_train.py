import os
from copy import deepcopy

import numpy as np
from catboost import CatBoost, Pool
from progressbar import progressbar

from private.settings import PRIVATE_DIR
from test_utils import get_top_one_train_data

MIN_APPTS = 3
LOSS_FUNCTION = 'QuerySoftMax'


def create_weights(queries):
    print('create weights')
    query_set = np.unique(queries)
    query_weights = np.random.uniform(size=query_set.shape[0])
    weights = np.zeros(shape=queries.shape)

    for i, query_id in enumerate(progressbar(query_set)):
        weights[queries == query_id] = query_weights[i]

    return weights


def get_best_documents(labels, queries):
    query_set = np.unique(queries)
    by_query_arg_max = {query: -1 for query in query_set}

    for i, query in enumerate(queries):
        best_idx = by_query_arg_max[query]
        if best_idx == -1 or labels[best_idx] < labels[i]:
            by_query_arg_max[query] = i

    binary_best_docs = np.zeros(shape=labels.shape)
    for arg_max in by_query_arg_max.values():
        binary_best_docs[arg_max] = 1.

    return binary_best_docs


def main():
    model_path = os.path.join(PRIVATE_DIR, 'ranking', f'top_one_model_{LOSS_FUNCTION}_{MIN_APPTS}.cbm')

    test_df, train_df = get_top_one_train_data(MIN_APPTS)
    print('loaded')
    X_train = train_df.drop([0, 1], axis=1).values
    y_train = train_df[0].values
    queries_train = train_df[1].values

    X_test = test_df.drop([0, 1], axis=1).values
    y_test = test_df[0].values
    queries_test = test_df[1].values

    default_parameters = {
        'iterations': 2000,
        'custom_metric': ['NDCG', 'PFound', 'AverageGain:top=10'],
        'verbose': False,
        'random_seed': 0,
    }

    def fit_model(loss_function: str, additional_params=None, train_pool=None, test_pool=None):
        parameters = deepcopy(default_parameters)
        parameters['loss_function'] = loss_function
        parameters['train_dir'] = os.path.join(PRIVATE_DIR, 'train', loss_function)

        if additional_params is not None:
            parameters.update(additional_params)

        model = CatBoost(parameters)
        model.fit(train_pool, eval_set=test_pool, plot=True)

        return model

    print('data creating')
    best_docs_train = get_best_documents(y_train, queries_train)
    best_docs_test = get_best_documents(y_test, queries_test)
    print('data created')

    train_with_weights = Pool(
        data=X_train,
        label=best_docs_train,
        group_id=queries_train,
        group_weight=create_weights(queries_train)
    )

    test_with_weights = Pool(
        data=X_test,
        label=best_docs_test,
        group_id=queries_test,
        group_weight=create_weights(queries_test)
    )

    print('training')
    model = fit_model(
        'QuerySoftMax',
        additional_params={'custom_metric': 'AverageGain:top=1'},
        train_pool=train_with_weights,
        test_pool=test_with_weights
    )

    model.save_model(model_path)


if __name__ == '__main__':
    main()

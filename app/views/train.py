import json
import os

import numpy as np
from catboost import CatBoost, Pool
from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from progressbar import progressbar
from sqlalchemy import desc

from app.collectors.dataset import DatasetCollector
from models.dataset import Dataset

bp = Blueprint('train', __name__, url_prefix='/train')


@bp.route('/', methods=('GET',))
def main():
    datasets = Dataset.query.order_by(desc(Dataset.id))
    return render_template('train/main_train.html', datasets=datasets)


@bp.route('/chart/', methods=('GET',))
def chart():
    index = request.args.get('index', default=0, type=int)
    with open('/Users/zwergpro/PycharmProjects/graduate-work/private/train/QuerySoftMax/catboost_training.json') as f:
        data = json.load(f)['iterations']
    return jsonify(data[index:])


@bp.route('/start_train/', methods=('POST',))
def start_train():
    dataset = Dataset.query.filter(Dataset.id == request.form.get('dataset')).first()
    collector = DatasetCollector(dataset_model=dataset)
    train_df, test_df = collector.load_dataset()

    X_train = train_df.drop([0, 1], axis=1).values
    y_train = train_df[0].values
    queries_train = train_df[1].values

    X_test = test_df.drop([0, 1], axis=1).values
    y_test = test_df[0].values
    queries_test = test_df[1].values

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

    model.save_model(collector.get_save_path('QuerySoftMax.bin'))

    print(dataset.id)
    return redirect(url_for('train.main'))


def fit_model(loss_function: str, additional_params=None, train_pool=None, test_pool=None):
    parameters = {
        'iterations': 200,
        'custom_metric': ['NDCG', 'PFound', 'AverageGain:top=10'],
        'verbose': False,
        'random_seed': 0,
        'loss_function': loss_function,
        'train_dir': os.path.join('/Users/zwergpro/PycharmProjects/graduate-work/private', 'train', loss_function),
    }

    if additional_params is not None:
        parameters.update(additional_params)

    model = CatBoost(parameters)
    model.fit(train_pool, eval_set=test_pool, plot=True, verbose=True)

    return model


def create_weights(queries):
    print('create weights')
    query_set = np.unique(queries)
    query_weights = np.random.uniform(size=query_set.shape[0])
    weights = np.zeros(shape=queries.shape)

    for i, query_id in enumerate(progressbar(query_set)):
        weights[queries == query_id] = query_weights[i]

    return weights


def get_best_documents(labels, queries):
    print('get_best_documents')
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

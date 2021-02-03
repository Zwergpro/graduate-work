import json
import os

import numpy as np
import math

import pandas as pd
import sqlite3

from sklearn.preprocessing import StandardScaler, MinMaxScaler
from scipy.stats import shapiro

import progressbar


class SQLite:
    cursor = None

    def __enter__(self):
        db = sqlite3.connect('../private/doctors.db')
        self.cursor = db.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor is not None:
            self.cursor.close()


# Задачи
# Составить вектор предпочтений
#

def normalized_attribute(matrix):
    result = StandardScaler().fit_transform(matrix)
    print(shapiro(result))
    print(result)

    result = MinMaxScaler().fit_transform(matrix)
    print(shapiro(result))
    print(result)


def get_doctors_and_dataset():
    data = pd.read_csv('../private/dataset.csv')
    doctor_stats = data.iloc[:, [0, 1, 2, 3]]
    matrix = MinMaxScaler().fit_transform(data.iloc[:, 5:])
    return doctor_stats, matrix


def get_users_and_doctors():
    data = pd.read_csv('../private/appointments.csv')

    if os.path.exists('../private/users.json'):
        print('load ../private/users.json')
        with open('../private/users.json', 'r') as fp:
            return json.load(fp)

    print('load ../private/appointments.csv')
    users_and_doctors = {}
    progress = progressbar.ProgressBar(max_value=data.shape[0])
    for row in data.iterrows():
        users_and_doctors.setdefault(int(row[1][0]), []).append(int(row[1][1]))
        progress.update(progress.value + 1)

    with open('../private/users.json', 'w') as f:
        json.dump(users_and_doctors, f)

    return users_and_doctors

def main():
    doctor_stats, matrix = get_doctors_and_dataset()
    users_and_doctors = get_users_and_doctors()
    print(users_and_doctors)

    # TODO: врачей и их вектора сделать по аналогии с пользователями и сохранить в json
    # TODO: сохранить в json вектора предпочтений пользователя
    # TODO: провести проверку

if __name__ == '__main__':
    main()


    movies = np.array([
        [1, 0, 1, 0, 1],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 1, 1],
        [0, 0, 1, 1, 0],
        [0, 1, 0, 0, 0],
        [1, 0, 0, 1, 0]
    ])

    #normalized_attribute(movies)

    users = np.array([
        [1, -1, 0, 0, 0, 1],
        [-1, 1, 0, 1, 0, 0]
    ])

    DF = np.array([2, 2, 3, 4, 2])

    total_attributes = np.array([3, 3, 2, 2, 1, 2])


    rows, columns = movies.shape

    # Normalize
    total_attributes_norm = []
    for attr in total_attributes:
        total_attributes_norm.append(1/math.sqrt(attr))

    movies = (movies.T * total_attributes_norm).T

    # print(movies)

    user_profiles = []

    for user in users:
        user_profile = []
        for index in range(columns):
            user_profile.append(sum(movies.T[index] * user))
        user_profiles.append(user_profile)

    # print(user_profiles)

    IDF = np.array(
        list(map(lambda x: math.log10(10 / x), DF))
    )
    # print(IDF)

    pred_users = []

    for user in user_profiles:
        pred_user = []

        matrix = movies * user * IDF

        for movie in matrix:
            pred_user.append(sum(movie))
        pred_users.append(pred_user)

    # print(pred_users)



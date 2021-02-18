from typing import Iterable

import psycopg2
import csv

from sshtunnel import SSHTunnelForwarder

from private.settings import DATABASES, SSH_SETTINGS

sql_files = (
    '../private/doctors.sql',
    '../private/appointments.sql'
)


class DB:
    cursor = None
    server = None

    def __enter__(self):
        self.server = SSHTunnelForwarder(**SSH_SETTINGS)
        self.server.start()
        db = psycopg2.connect(**DATABASES['default'])
        self.cursor = db.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor is not None:
            self.cursor.close()

        if self.server is not None:
            self.server.stop()


def fetch_data(cursor, query):
    cursor.execute(query)
    return cursor.fetchall()


def fetch_all(files: Iterable[str]):
    with DB() as cursor:
        for file in files:
            print(f'fetching {file}')
            with open(file, 'r') as f:
                query = f.read()

            cursor.execute(query)

            data_file = file.replace('sql', 'csv')
            with open(data_file, 'w') as csv_file:
                writer = csv.writer(csv_file, delimiter=',')
                writer.writerows(cursor.fetchall())


if __name__ == '__main__':
    fetch_all(sql_files)


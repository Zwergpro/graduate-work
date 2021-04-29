from functools import cached_property
from os import path

import sqlalchemy
from environs import Env

env = Env()
env.read_env()


class Config(object):
    DEBUG = False
    TESTING = False

    ROOT_PATH = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
    BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))
    SECRET_KEY = env('SECRET_KEY')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @cached_property
    def SQLALCHEMY_DATABASE_URI(self):
        with env.prefixed("DB_"):
            return sqlalchemy.engine.URL.create(
                drivername='postgresql+psycopg2',
                username=env('USERNAME'),
                password=env('PASSWORD'),
                host=env.str('HOST', 'localhost'),
                port=env.int('PORT', 5432),
                database=env('DATABASE'),
            )


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'secret_key'
    SQLALCHEMY_RECORD_QUERIES = True


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = 'secret_key'

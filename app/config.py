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

    with env.prefixed("DB_"):
        SQLALCHEMY_DATABASE_URI = sqlalchemy.engine.URL.create(
            drivername='postgresql+psycopg2',
            username=env('USERNAME'),
            password=env('PASSWORD'),
            host=env.str('HOST', 'localhost'),
            port=env.int('PORT', 5432),
            database=env('DATABASE'),
        )

    with env.prefixed("REDIS_"):
        REDIS_HOST = env.str('HOST', 'localhost')
        REDIS_PORT = env.int('PORT', 6379)
        REDIS_PASSWORD = env.str('PASSWORD', '')
        REDIS_DB = env.int('DB', 0)


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = 'secret_key'
    SQLALCHEMY_RECORD_QUERIES = True


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = 'secret_key'

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()


def create_app(use_test_config: bool = False):
    app = Flask(__name__)
    _load_config(app, use_test_config)
    db.init_app(app)
    return app


def _load_config(app: Flask, use_test_config: bool) -> None:
    if use_test_config:
        app.config.from_object('config.TestingConfig')
        print('Used TestingConfig')
        return

    flask_env = os.environ.get('FLASK_ENV', 'development')
    if flask_env == 'development':
        app.config.from_object('config.DevelopmentConfig')
        print('Used DevelopmentConfig')
        return

    if flask_env == 'production':
        print('Used Config')
        app.config.from_object('config.Config')
        return

    raise RuntimeError('Invalid FLASK_ENV')

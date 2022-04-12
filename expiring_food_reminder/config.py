import os

project_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ['SECRET_KEY']
    DAILY_WORK_PASSWORD = os.environ['DAILY_WORK_PASSWORD']


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(project_dir, 'static/data/data.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')


config_dict = {'develop': DevelopmentConfig,
               'product': ProductionConfig}

import os
from logging.config import dictConfig

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'helloihsaldf'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'gamedb.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    PROFILE_PHOTO_DIR = os.path.join(basedir,'static/uploaded_photo')


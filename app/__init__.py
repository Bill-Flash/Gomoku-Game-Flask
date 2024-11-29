from logging.config import dictConfig
from logging.handlers import RotatingFileHandler

from flask import Flask

from app.config import Config
from flask_sqlalchemy import SQLAlchemy


''' this file will be automatically run once the myapp.py runs
'''



app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
# __name__ is a python predefined variable that fit the module which is using
# app will be used on routes.py


from app import routes, models
# in case of circular imports

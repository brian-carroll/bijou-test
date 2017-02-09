import os
import sqlite3

from flask import Flask, g
from flask.json import JSONEncoder
from flask_sqlalchemy import SQLAlchemy


# Create the application instance and configure it
app = Flask(__name__)
db_path = os.path.join(app.root_path, 'flask.db')
app.config.update(dict(
    DATABASE=db_path,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default',
    SCRAPER_CACHE_DIR=os.path.abspath(app.root_path + '/../../scraper/data/farah'),
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % db_path,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_ECHO=False
))


# Initialize database
# sqlite3.connect(app.config['DATABASE'])
db = SQLAlchemy(app)


from .views import *

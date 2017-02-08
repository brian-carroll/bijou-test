import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from pprint import pformat
import json

# Create the application instance and configure it
app = Flask(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flask.db'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default',
    SCRAPER_CACHE_DIR=os.path.abspath(app.root_path + '/../../scraper/data/farah')
))

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.before_first_request
def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/', methods=['GET'])
def home():
    return "Hi"


def process_product(categories, data):
    '''
    - should eventually become and endpoint to be hit by scrapy directly with JSON data?
    - Do the scraper and microservice need to share a schema?

    '''
    return '/'.join(categories) + pformat(data).replace('\n','<br>').replace(' ', '&nbsp;')


@app.route('/load-data', methods=['POST', 'GET'])
def load_data():
    source_dir = app.config['SCRAPER_CACHE_DIR']
    output_str = ''

    for dirname, dirs, files in os.walk(source_dir):
        for filename in files:
            fullpath = os.path.join(dirname, filename)

            categories = dirname.split('/')
            with open(fullpath, 'r') as f:
                data = json.load(f)
            output_str += '<br>' + process_product(categories, data)

    return output_str

import os
import json
from pprint import pformat

from flask import request
from . import app


@app.route('/', methods=['GET'])
def home():
    return "Hi"


def process_product(categories, data):
    '''
    - should eventually become and endpoint to be hit by scrapy directly with JSON data?
    - Do the scraper and microservice need to share a schema?

    '''
    return '/'.join(categories) + pformat(data).replace('\n','<br>').replace(' ', '&nbsp;')

@app.route('/categories', methods=['POST', 'GET'])
def list_categories():
    try:
        limit = int(request.args.get('limit'))
    except:
        limit = None

    source_dir = app.config['SCRAPER_CACHE_DIR']
    categories = []

    count = 0
    for dirname, dirs, files in os.walk(source_dir):
        categories.append(dirname)
        count += 1
        if limit and count >= limit:
            break

    output_str = ('<ul>\n<li>'
                  + '</li>\n<li>'.join(categories)
                  + '</li>\n</ul>')
    return output_str


@app.route('/load-data', methods=['POST', 'GET'])
def load_data():
    try:
        limit = int(request.args.get('limit'))
    except:
        limit = None

    source_dir = app.config['SCRAPER_CACHE_DIR']
    output_str = ''

    count = 0
    for dirname, dirs, files in os.walk(source_dir):
        for filename in files:
            fullpath = os.path.join(dirname, filename)

            categories = dirname.split('/')
            with open(fullpath, 'r') as f:
                data = json.load(f)
            output_str += '<br>' + process_product(categories, data)
            count += 1
            if limit and count >= limit:
                break
        if limit and count >= limit:
            break

    return output_str

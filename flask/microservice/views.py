import os
import json
from pprint import pformat

from flask import request, jsonify
from . import app, db
from .models import Product, ProductImage



@app.route('/', methods=['GET'])
def home():
    return """
        <h1>Bijou Scraper</h1>
        <ul>
            <li><a href="/products">    Products                </a></li>
            <li><a href="/categories">  Categories              </a></li>
            <li><a href="/files-to-db"> Transfer files to DB    </a></li>
        </ul>
    """


@app.route('/products', methods=['GET'])
def list_products():
    try:
        limit = int(request.args.get('limit'))
    except:
        limit = None

    source_dir = app.config['SCRAPER_CACHE_DIR']
    rel = len(source_dir)  # number of characters to remove to get a relative path

    products = []
    count = 0
    for dirname, dirs, files in os.walk(source_dir):
        for filename in files:
            fullpath = dirname + '/' + filename
            with open(fullpath, 'r') as fp:
                json_data = json.load(fp)
            categories = [c for c in dirname[rel:].split('/') if c]
            p = Product(json_data, categories)
            products.append(p.serializable())
            count += 1
            if limit and count >= limit:
                break
        if limit and count >= limit:
            break

    return jsonify(data=products)


@app.route('/categories', methods=['GET'])
def list_categories():
    try:
        limit = int(request.args.get('limit'))
    except:
        limit = None

    source_dir = app.config['SCRAPER_CACHE_DIR']
    rel = 1+len(source_dir)  # number of characters to remove to get a relative path

    categories = []
    count = 0
    for dirname, dirs, files in os.walk(source_dir):
        if dirname == source_dir:
            continue
        categories.append(dirname[rel:].split('/'))
        count += 1
        if limit and count >= limit:
            break

    return jsonify(data=categories)



@app.route('/files-to-db', methods=['POST', 'GET'])
def load_files_into_db():
    '''
    - Migrate data from filesystem to DB
    - Have something to look at for debug
    '''
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
            output_str += ('<br>'
                           + '/'.join(categories)
                           )
            count += 1
            if limit and count >= limit:
                break
        if limit and count >= limit:
            break

    return output_str

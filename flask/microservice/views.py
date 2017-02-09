import os
import json
from pprint import pformat

from flask import request, jsonify
from . import app, db
from .models import *



@app.route('/', methods=['GET'])
def home():
    return """
        <h1>Bijou Scraper</h1>
        <ul>
            <li><a href="/products"> Products </a></li>
            <li><a href="/categories"> Categories </a></li>
            <li><a href="/load-categories"> Load categories into DB </a></li>
            <li><a href="/load-products"> Load products into DB </a></li>
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


@app.route('/load-categories', methods=['POST', 'GET'])
def load_categories():
    '''
    - Migrate data from filesystem to DB
    - Have something to look at for debug
    '''
    source_dir = app.config['SCRAPER_CACHE_DIR']
    rel = 1+len(source_dir)  # chars to drop to get relative path
    output_str = ''

    db_cats = Category.query.all()
    root_categories = [c for c in db_cats if c.parent is None]
    if not root_categories:
        root = Category()
        root.name = 'farah'
        db.session.add(root)
    elif len(root_categories) == 1:
        root = root_categories[0]
    else:
        raise Exception('More than one root category!')

    for dirname, dirs, files in os.walk(source_dir):
        if dirname==source_dir:
            continue
        parent = root
        hierarchy = dirname[rel:].split('/')
        for name in hierarchy:
            db_matches = [c for c in parent.subcategories if c.name==name]
            if db_matches:
                # already exists
                category = db_matches[0]
            else:
                # need to create
                category = Category()
                category.name = name
                parent.subcategories.append(category)
            parent = category

    response = jsonify(root.serializable())
    db.session.commit()
    return response




@app.route('/load-products', methods=['POST', 'GET'])
def load_products():
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

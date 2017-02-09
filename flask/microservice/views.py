import os
import json
from pprint import pformat
from datetime import datetime

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
            <li><a href="/refresh-db"> Reload Scraper data into Database </a></li>
        </ul>
    """


@app.route('/products', methods=['GET'])
def products_endpoint():
    try:
        limit = int(request.args.get('limit'))
    except:
        limit = None
    return list_products(limit)

def list_products(limit):
    products = Product.query.limit(limit)
    return jsonify([p.serializable() for p in products])


def get_root_category():
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
    return root



@app.route('/categories', methods=['GET'])
def list_categories():
    root = get_root_category()
    return jsonify(root.serializable(recursive=True))


@app.route('/refresh-db', methods=['POST', 'GET'])
def refresh_db():
    '''
    - Migrate data from filesystem to DB
    - Have something to look at for debug
    '''
    source_dir = app.config['SCRAPER_CACHE_DIR']
    rel = 1+len(source_dir)  # chars to drop to get relative path
    count = 0
    products = []

    root = get_root_category()

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

        for filename in files:
            fullpath = os.path.join(dirname, filename)
            scrape_time = datetime.fromtimestamp(os.path.getmtime(fullpath))
            with open(fullpath, 'r') as f:
                json_obj = json.load(f)
            product = Product.create(json_obj, category, scrape_time)
            products.append(product)
            count += 1

    db.session.commit()

    return jsonify({
        'categories': get_root_category().serializable(recursive=True),
        'products': [p.serializable() for p in Product.query.all()]
    })

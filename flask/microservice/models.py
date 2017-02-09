import os
import json
from datetime import datetime

from . import db




class Category(db.Model):
    __tablename__ = 'categories'
    __table_args__ = (db.UniqueConstraint('parent_id', 'name'),)

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    parent_id = db.Column(db.Integer(), db.ForeignKey('categories.id'))
    name = db.Column(db.String(255))

    children = db.relationship("Category")
    parent = db.relationship("Category", remote_side=[id])

    def serializable(self):
        return {
            'id': self.id,
            'parent_id': self.parent_id,
            'name': self.name,
        }

    @classmethod
    def create_hierarchy(cls, hierarchy_list):
        # Get all matching category names from the DB (may contain irrelevant duplicates)
        db_cats = cls.query.filter(cls.name.in_(hierarchy_list)).all()

        # Walk through the hierarchy of names, creating any missing categories
        parent = None
        for name in hierarchy_list:
            db_matches = [c for c in db_cats if c.name==name and c.parent is parent]
            if db_matches:
                # already exists
                category = db_matches[0]
            else:
                # need to create
                category = cls()
                category.name = name
                category.parent = parent
                db.session.add(category)
            # set up for the next iteration
            parent = category


product_categories = db.Table(
    'product_categories',
    db.Model.metadata,
    db.Column('product_id', db.Integer, db.ForeignKey('products.id')),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'))
    )


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    code = db.Column(db.String(255), index=True)
    name = db.Column(db.String(255))
    scrape_time = db.Column(db.DateTime)
    price_x100 = db.Column(db.Integer())
    # high_price_x100 = db.Column(db.Integer())
    # low_price_x100 = db.Column(db.Integer())
    # details = db.Column(db.String())
    # availability = db.Column(db.String())
    # shipping = db.Column(db.String())

    images = db.relationship("ProductImage", backref="product")
    variations = db.relationship("Variation", backref="product")
    categories = db.relationship("Category", secondary='product_categories')

    def serializable(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'price': self.price,
            'categories': [c.serializable() for c in self.categories],
            'images': [i.serializable() for i in self.images]
        }

    @classmethod
    def create(cls, j, category_obj, scrape_time):
        if 'ID' not in j:
            raise KeyError('Product JSON has no ID field')

        p = cls.query.filter(cls.code==int(j['ID'])).first()
        if p is None:
            p = cls()
            p.code = j['ID']
            db.session.add(p)

        if category not in p.categories:
            p.categories.append(category_obj)

        p.scrape_time = scrape_time
        p.name = j['name']

        if 'images' in j:
            for k,v in j['images'].items():
                if isinstance(v, list):
                    for i in v:
                        p.images.append(ProductImage(k,i))
        try:
            p.price_x100 = 100*round(
                (j['pricing']['showStandardPrice'] and j['pricing']['standard'])
                or j['pricing']['sale']
                )
        except:
            self.price_x100 = 0



class VariationImage(db.Model):
    __tablename__ = 'variation_images'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    variation_id = db.Column(db.Integer(), db.ForeignKey('variations.id'))
    size_label = db.Column(db.String(255))
    url = db.Column(db.String())

    def serializable(self):
        return {
            'id': self.id,
            'variation_id': self.variation_id,
            'size_label': self.size_label,
            'url': self.url,
        }



class Variation(db.Model):
    __tablename__ = 'variations'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer(), db.ForeignKey('products.id'))
    attribute_name = db.Column(db.String(255))
    val = db.Column(db.String(255))

    images = db.relationship("VariationImage")

    def serializable(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'attribute': self.attribute,
            'val': self.val,
            'images': [i.serializable() for i in self.images]
        }


class ProductImage(db.Model):
    __tablename__ = 'product_images'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer(), db.ForeignKey('products.id'))
    size_label = db.Column(db.String(255))
    url = db.Column(db.String())

    def __init__(self, resolution, url):
        self.resolution = resolution
        self.url = url

    def serializable(self):
        return {
            'id': self.id,
            'resolution': self.resolution,
            'url': self.url
        }




'''
Create all tables (unless they exist already)
'''
db.create_all()

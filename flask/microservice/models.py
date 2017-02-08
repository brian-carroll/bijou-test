import os
import json
from datetime import datetime


class Variation(object):
    id = 0
    product_id = 0
    attribute = "color"
    val = None

    def serializable(self):
        return self.__dict__


class ProductImage(object):
    id = 0
    resolution = ""
    url = ""

    def __init__(self, resolution, url):
        self.resolution = resolution
        self.url = url

    def serializable(self):
        return dict(
            id = self.id,
            resolution = self.resolution,
            url = self.url
        )


class Product(object):
    '''
      - Image
      - Item name
      - Price
      - Default colour (or "variation attributes")
      - Category, sub-category, sub-sub-category...
        - Tree structure, possibly overlapping, unclear how deep it goes.
    - Secondary fields (displayed on product detail pages)
      - Variation attributes (Size, colour, etc. Possibly separate table)
      - Low price & High price (Depend on variation attributes)
      - Image URLs (different sizes & colours)
      - Details
      - Availability (Seems likely to change fast - leave it out for now)
      - Shipping (Depends on business model, are Farah still shipping it?)
    - System fields (for tech or business operations)
      - Item number
      - Scrape timestamp
    '''
    id = 0
    code = ""
    name = ""
    scrape_time = datetime.now()
    images = []
    variations = []
    categories = []
    price = 0
    high_price = 0
    low_price = 0
    details = ""

    def __init__(self, j, categories):
        self.categories = categories

        self.code = j['ID']
        if 'images' in j:
            for k,v in j['images'].items():
                if isinstance(v, list):
                    for i in v:
                        self.images.append(ProductImage(k,i))
        self.name = j['name']
        try:
            self.price = (
                (j['pricing']['showStandardPrice'] and j['pricing']['standard'])
                or j['pricing']['sale']
                )
        except:
            self.price = None

    def serializable(self):
        return dict(
            id = self.id,
            code = self.code,
            name = self.name,
            price = self.price,
            categories = self.categories,
            images = [i.serializable() for i in self.images]
        )


class Category(object):
    id = 0
    parent = None
    name = ""

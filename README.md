Bijou Scraper
=============
Scrapes product and category info from http://www.farah.co.uk/


Project Plan
------------
- Challenges
  - Normalising the data
    - Can a product appear in more than one category?
    - How deep do the categories go?
    - Which fields are optional and which always there?

- Phase 1: Scrape unstructured data
  - [x] Get a scraper working using Scrapy
    - Save as JSON files in a directory tree (mirroring the site structure)
  - [x] Create models based on filesystem data
  - [x] Create endpoints using those models

- Phase 2: Normalise to relational data
  - [ ] Build a schema that makes sense with the data we have
  - [ ] Convert models from filesystem to database

- Phase 3: Refactor to shared models
  - [ ] Import Flask DB models into Scrapy as a package
    - The database model becomes the interface between the two projects.
  - [ ] Move normalisation code into Scrapy project
    - Perhaps Farah is a subclass that specialises the models?
    - Other retailers will have different normalisation code


Data to Store
-------------
- I'm assuming that Bijou is reselling items from multiple retailers
  - Could be wrong, business context is quite brief in the project description
- Farah website layout gives hints as to importance of each field
- Primary fields (displayed prominently on category & search pages)
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


Installation
------------
This project is written in Python 3.4 and depends on Scrapy.

Scrapy can be a bit tricky to install, and varies by OS.

To install on Ubuntu 14.04:
```
sudo apt-get install python3-lxml zlib1g-dev libxml2-dev libxslt-dev python-dev libssl-dev libffi-dev

virtualenv -p /usr/bin/python3 venv

venv/bin/pip install -r requirements.txt
```

Or just run the `install.sh` script provided.

If you have a different OS, you may need to look at the
[Scrapy installation instructions](https://doc.scrapy.org/en/latest/intro/install.html) and modify accordingly.


Running the code
----------------

```
source venv/bin/activate
cd scraper
scrapy crawl farah

# Wait...

cd ../flask
python3 runserver.py

# Endpoints:
curl http://localhost:5000/categories?limit=10
curl http://localhost:5000/products?limit=10

```

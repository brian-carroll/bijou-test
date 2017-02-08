Bijou Scraper
=============
Scrapes product and category info from http://www.farah.co.uk/

Data to Store
-------------
- From what I can gather, Bijou is reselling items from multiple retailers
- Retailers website layout gives hints as to importance of each field for sales
- System fields (needed for tech or business operations)
  - Item number
  - Scrape timestamp
- Primary fields (displayed prominently on category & search pages)
  - Image
  - Item name
  - Price
  - Default colour ("variation attributes" being the more general term)
  - Category, sub-category, sub-sub-category...
    - Tree structure, unclear how deep it goes
    - Looks like the same item could appear in multiple categories
- Secondary fields (displayed on product detail pages)
  - Variation attributes
    - Size, colour, etc.
    - Separate table of child objects
    - Default colours exist so that an image can be shown without user choosing
  - Low price & High price
    - Prices depend on variation attributes.
    - Will take some work to track down exactly how, and where the info is.
    - May need some more complicated schema for this
  - Image URLs
    - Lots of different sizes
    - Different colours too
  - Details
    - Depends on business requirements whether we need this or not
  - Availability
    - Seems likely to go out of date quickly
    - Depends on business requirements whether we need this or not
  - Shipping
    - Depends on business model, I don’t know who’s shipping it!


Project Plan
------------
- Challenges
  - Time is tight, recruiter asked for a few hours turnaround.
  - Normalising the data
    - Can a product appear in more than one category?
    - How deep do the categories go?
    - Which fields are optional and which always there?
- Phase 1: Cache scraped data as unstructured documents
  - [ ] Get a scraper working using Scrapy, cache data locally as JSON files
    - A JSON structure is available on the product pages
    - Directory tree structure mirrors URLs directly.
    - Too slow for production, but very handy for fast analysis & iteration
  - [ ] Examine the actual structure of the data
    - Linux tools like `grep` and `find` may come in handy.
  - [ ] Create endpoints
    - Models walk the directory tree instead of querying a database
    - Don't have to rerun the scraper each time we iterate the models
    - Deal with missing data or inconsistencies
- Phase 2: Normalise to relational data
  - [ ] Build a schema that makes sense with the data we have
  - [ ] Convert models from filesystem to database


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

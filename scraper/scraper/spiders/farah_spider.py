import scrapy
import re
import json
from urllib.parse import urlparse
import os


def href(link):
    return link.xpath('@href').extract()[0]


class FarahSpider(scrapy.Spider):
    name = "farah"
    script_regex = re.compile(r"app\.ProductCache = new app\.Product\(\{data:(.*)\}\);\W+jQuery")

    def start_requests(self):
        urls = [
            'http://www.farah.co.uk/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_home)


    def parse_home(self, response):
        for link in response.css('#primaryNavigationList a:not(.static)'):
            yield scrapy.Request(url=href(link), callback=self.parse_category)


    def parse_category(self, response):
        # Links to more category pages on left-hand-side
        for link in response.css('#refinement-category a.refineLink'):
            yield scrapy.Request(url=href(link), callback=self.parse_category)

        # Footer links (search results pagination)
        for link in response.css('.searchresultsfooter a'):
            yield scrapy.Request(url=href(link), callback=self.parse_category)

        # Central area with product details - link to product pages
        for link in response.css('#productresultarea .name a'):
            yield scrapy.Request(url=href(link), callback=self.parse_product)


    def parse_product(self, response):
        # Product pages have a handy script tag from which we can extract product data as JSON
        # Use a regex to extract the interesting JSON from the rest of the JavaScript
        script = response.xpath("//script[contains(., 'app.ProductCache = new app.Product')]/text()")
        json_data = script.re(self.script_regex)[0]
        product = json.loads(json_data)

        # Generate JSON files for each page extracted
        # Caching this data on the local filesystem makes development easier
        dirname = './data/' + self.name + '/'.join(urlparse(response.url).path.split('/')[:-1])
        os.makedirs(dirname, exist_ok=True)
        filename = dirname + '/' + product['ID'] + '.json'
        with open(filename, 'w') as f:
            f.write(json_data)
        self.log('Saved file %s' % filename)

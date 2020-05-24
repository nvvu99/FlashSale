# -*- coding: utf-8 -*-
# from scrapy.crawler import CrawlerProcess

# from FlashSale.spiders.sendo_api import SendoSpider
# from FlashSale.spiders.tiki_api import TikiSpider

# process = CrawlerProcess(get_project_settings())
# process.crawl(SendoSpider)
# process.start()
# process2 = CrawlerProcess(get_project_settings())
# process2.crawl(TikiSpider)
# process2.start()

import os
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

from FlashSale.spiders.sendo import SendoSpider
from FlashSale.spiders.tiki import TikiSpider

configure_logging()
settings = get_project_settings()
flashsale_dir = 'Product'

try:
    os.mkdir(flashsale_dir)
except Exception as e:
    pass

os.chdir(flashsale_dir)
category_file_name = 'category.json'
product_file_name = 'product.json'
category_file = open(category_file_name, 'w')
product_file = open(product_file_name, 'w')

category_file.close()
product_file.close()

runner = CrawlerRunner(settings)

@inlineCallbacks
def crawl():
    yield runner.crawl(SendoSpider)
    yield runner.crawl(TikiSpider)
    # yield runner.crawl(Tiki)
    reactor.stop()

crawl()
reactor.run()
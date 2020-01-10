# -*- coding: utf-8 -*-
import scrapy
from FlashSale.spiders.tiki_api import TikiSpider
from FlashSale.spiders.sendo_api import SendoSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


process = CrawlerProcess(get_project_settings())
process.crawl(SendoSpider)
process.crawl(TikiSpider)
# process.start()
process.start()

# class FlashsaleSpider(scrapy.Spider):
    # name = 'flashsale'
    # allowed_domains = ['flashsale']
    # start_urls = ['http://flashsale/']

    # def __init__(self):
    #     self.tiki_spider = TikiSpider()
    #     self.sendo_spider = SendoSpider()

    # def start_requests(self):
    #     self.tiki_spider.start_requests()
    #     self.sendo_spider.start_requests()

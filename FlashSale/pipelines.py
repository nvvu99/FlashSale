# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
from FlashSale.items import FlashsaleItem, CategoryItem
from scrapy.utils.project import get_project_settings
from pymongo import MongoClient
import json


settings = get_project_settings()
server = settings.get('MONGO_SERVER')
port = settings.get('MONGO_PORT')
db_name = settings.get('MONGO_DB')
collection_name = settings.get('MONGO_COLLECTION')
client = MongoClient(server, port)
db = client[db_name]
category_collection = db[collection_name[0]]
product_collection = db[collection_name[1]]


class DuplicateItemPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, CategoryItem):
            query = {'_id': item['category_id']}
            category_collection.delete_one(query)

        if isinstance(item, FlashsaleItem):
            query = {'_id': item['product_id']}
            product_collection.delete_one(query)

        return item


class ToDatabasePipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, CategoryItem):
            item['_id'] = item['category_id']
            category_collection.insert_one(item)

        if isinstance(item, FlashsaleItem):
            item['_id'] = item['product_id']
            product_collection.insert_one(item)

        return item


class ToJsonFilePipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def __init__(self):
        self.category_file = open('category.json', 'w', encoding = 'utf-8')
        self.product_file = open('product.json', 'w', encoding = 'utf-8')

    def process_item(self, item, spider):
        if isinstance(item, CategoryItem):
            json.dump(dict(item), self.category_file)
            self.category_file.write('\n')

        if isinstance(item, FlashsaleItem):
            json.dump(dict(item), self.product_file)
            self.product_file.write('\n')

        return item

    def spider_closed(self):
        self.category_file.close()
        self.product_file.close()
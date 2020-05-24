# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import json
import time
from pprint import pprint

from scrapy import signals
from scrapy.utils.project import get_project_settings

from FlashSale.items import FlashsaleItem, CategoryItem

settings = get_project_settings()
server = settings.get('MONGO_SERVER')
port = settings.get('MONGO_PORT')
db_name = settings.get('MONGO_DB')
collection_name = settings.get('MONGO_COLLECTION')

category_file_name = 'category.json'
product_file_name = 'product.json'
category_file = open(category_file_name, 'a', encoding='utf-16')
product_file = open(product_file_name, 'w', encoding='utf-16')

try:
    from pymongo import MongoClient
    client = MongoClient(server, port)
    db = client[db_name]
    category_collection = db[collection_name[0]]
    product_collection = db[collection_name[1]]
except:
    # failed to connect to database
    pass


class DuplicateItemPipeline(object):
    def process_item(self, item, spider):
        try:
            if isinstance(item, CategoryItem):
                query = {'_id': item['category_id']}
                category_collection.delete_one(query)

            if isinstance(item, FlashsaleItem):
                query = {'_id': item['product_id']}
                product_collection.delete_one(query)
        except:
            pass
        # pprint(item)
        return item


class ToDatabasePipeline(object):
    def process_item(self, item, spider):
        try:
            if isinstance(item, CategoryItem):
                item['_id'] = item['category_id']
                category_collection.insert_one(item)

            if isinstance(item, FlashsaleItem):
                item['_id'] = item['product_id']
                product_collection.insert_one(item)
        except:
            pass

        return item


class ToJsonFilePipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        # crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def __init__(self):
        # current_dir = os.getcwd()
        pass

    def process_item(self, item, spider):
        if isinstance(item, CategoryItem):
            json.dump(dict(item), category_file, ensure_ascii = False)
            category_file.write('\n')
            pprint('successed')

        if isinstance(item, FlashsaleItem):
            json.dump(dict(item), product_file, ensure_ascii = False)
            product_file.write('\n')

        # time.sleep(1)
        return item

    def spider_closed(self):
        category_file.close()
        product_file.close()
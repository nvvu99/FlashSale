# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Join, Identity, MapCompose, TakeFirst
import re
from datetime import datetime


def full_tiki_id(text):
    return 'tiki' + str(text)

def full_tiki_url(text):
    return 'https://tiki.vn/' + str(text)

def full_sendo_id(text):
    return 'sendo' + str(text)

def get_categoryid(text):
    p = re.compile('[0-9]+')
    return int(p.search(str(text)).group())

def isoformat_to_timestamp(text):
    return int(datetime.timestamp(datetime.fromisoformat(text)))


class FlashsaleItem(scrapy.Item):
    _id = scrapy.Field()
    product_id = scrapy.Field()
    name = scrapy.Field()
    image = scrapy.Field()
    category_id = scrapy.Field()
    url = scrapy.Field()        
    origin_price = scrapy.Field()
    discount_price = scrapy.Field()
    # status = scrapy.Field()
    quantity = scrapy.Field()
    remain = scrapy.Field()
    start_time = scrapy.Field()
    end_time = scrapy.Field()


class CategoryItem(scrapy.Item):
    _id = scrapy.Field()
    category_id = scrapy.Field(
        input_processor = MapCompose(get_categoryid),
        output_processor = TakeFirst()
        )
    category_name = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = Join('')
        )


class TikiItem(FlashsaleItem):
    product_id = scrapy.Field(
        input_processor = MapCompose(full_tiki_id)
        )
    url = scrapy.Field(
        input_processor = MapCompose(full_tiki_url)
        )
    rating = scrapy.Field()
    review = scrapy.Field()


class SendoItem(FlashsaleItem):
    product_id = scrapy.Field(
        input_processor = MapCompose(full_sendo_id)
        )
    start_time = scrapy.Field(
        input_processor = MapCompose(isoformat_to_timestamp)
        )
    end_time = scrapy.Field(
        input_processor = MapCompose(isoformat_to_timestamp)
        )
# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from scrapy.utils.project import get_project_settings

from FlashSale.items import CategoryItem, SendoItem

# maximum of number of page for each category of products
MAX_PAGE = 1


class SendoSpider(scrapy.Spider):
    name = 'sendoapi'

    def __init__(self):
        settings = get_project_settings()
        self.urls = settings.get('SENDO')

    def start_requests(self):
        deal_time_url = self.urls[1]
        yield scrapy.Request(
            url=deal_time_url,
            method='POST',
            callback=self.parse_deal_time
        )

    def parse_deal_time(self, response):

        content = json.loads(response.text)
        data = content['data']
        deal_times = data['slots']

        length = len(deal_times)
        for i in range(0, length - 1):
            deal_times[i]['end_time'] = deal_times[i + 1]['slot']
        
        del deal_times[length - 1]

        category_url = self.urls[0]
        yield scrapy.Request(
            url=category_url,
            callback=self.parse_category,
            meta={'deal_times': deal_times}
        )

    def parse_category(self, response):
        deal_times = response.meta['deal_times']
        content = json.loads(response.text)
        categories = content['data']
        # delete unneeded categories
        del categories[0]

        for category in categories:
            category_loader = ItemLoader(CategoryItem())
            category_loader.add_value('category_id', category['category_group_id'])
            category_loader.add_value('category_name', category['name'])
            yield category_loader.load_item()

            request_payload = category
            page = 1
            limit = 30  # limit products per page
            request_payload['page'] = page
            request_payload['limit'] = limit
            # for deal_time in deal_times:
            deal_time = deal_times[0]
            request_payload['slot'] = deal_time['slot']
            start_time = deal_time['slot']
            yield scrapy.Request(
                url=self.urls[2],
                method='POST',
                body=json.dumps(request_payload),
                callback=self.parse_product,
                meta={
                    'category_id': category['category_group_id'],
                    'deal_time': deal_time,
                    'request_payload': request_payload,
                }
            )

    def parse_product(self, response):
        # Parse current page
        meta = response.meta
        category_id = meta['category_id']
        deal_time = meta['deal_time']
        content = json.loads(response.text)
        products = content['data']['products']
        if products == []:
            return

        for product in products:
            sale_item_loader = ItemLoader(item=SendoItem())
            sale_item_loader.default_output_processor = TakeFirst()
            sale_item_loader.add_value('product_id', product['product_id'])
            sale_item_loader.add_value('name', product['name'])
            sale_item_loader.add_value('image', product['image'])
            sale_item_loader.add_value('url', product['url_key'])
            sale_item_loader.add_value('category_id', category_id)
            sale_item_loader.add_value('discount_price', product['final_price'])
            sale_item_loader.add_value('origin_price', product['price'])
            sale_item_loader.add_value('quantity', product['quantity'])
            sale_item_loader.add_value('remain', product['remain'])
            sale_item_loader.add_value('start_time', deal_time['slot'])
            sale_item_loader.add_value('end_time', deal_time['end_time'])
            yield sale_item_loader.load_item()

        # request to next product page
        request_payload = meta['request_payload']
        if request_payload['page'] < MAX_PAGE:
            request_payload['page'] += 1
            yield scrapy.Request(
                url=self.urls[2],
                method='POST',
                body=json.dumps(request_payload),
                callback=self.parse_product,
                meta={
                    'category_id': category_id,
                    'deal_time': deal_time,
                    'request_payload': request_payload,
                }
            )

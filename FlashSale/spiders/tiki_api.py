# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from FlashSale.items import CategoryItem, TikiItem
from scrapy.utils.project import get_project_settings
import time
import json

MAX_PAGE = 1
NOW = 0
COMING = 1


class TikiSpider(scrapy.Spider):
    name = 'tikiapi'

    def __init__(self):
        settings = get_project_settings()
        self.start_url = settings.get('TIKI_FLASHSALE').format(1)
        self.sale_urls = settings.get('TIKI_API')

    def start_requests(self):
        yield scrapy.Request(
            url = self.start_url,
            method = 'GET',
            callback = self.parseCategory
            )

    def parseCategory(self, response):
        meta = response.meta
        categories_dom_xpath = '/html/body/header/div[@class="main-nav"]/div/nav/ul/li'
        category_url_xpath = './a/@href'
        category_name_xpath = './a/span/text()'

        categories_dom = response.xpath(categories_dom_xpath)
        for category_dom in categories_dom:
            category_loader = ItemLoader(item = CategoryItem(), selector = category_dom)
            category_loader.add_xpath('category_id', category_url_xpath)
            category_loader.add_xpath('category_name', category_name_xpath)
            yield category_loader.load_item()

            category_id = category_loader.get_output_value('category_id')
            page = 1
            yield scrapy.Request(
                url = self.sale_urls[NOW].format(category_id, page), 
                callback = self.parseProduct, 
                meta = {
                    'time': NOW,
                    'category_id': category_id
                    }
                )
            yield scrapy.Request(
                url = self.sale_urls[COMING].format(category_id, page), 
                callback = self.parseProduct, 
                meta = {
                    'time': COMING,
                    'category_id': category_id
                    }
                )

    def parseProduct(self, response):
        # Parse current page
        meta = response.meta
        category_id = meta['category_id']
        time = meta['time']
        content = json.loads(response.text)

        products = content['data']
        for product in products:
            sale_item_loader = ItemLoader(item = TikiItem())
            sale_item_loader.default_output_processor = TakeFirst()

            product_info = product['product']
            progress = product['progress']
            sale_item_loader.add_value('product_id', product_info['id'])
            sale_item_loader.add_value('name', product_info['name'])
            sale_item_loader.add_value('image', product_info['thumbnail_url'])
            sale_item_loader.add_value('category_id', category_id)
            sale_item_loader.add_value('url', product_info['url_path'])
            sale_item_loader.add_value('origin_price', product_info['list_price'])
            sale_item_loader.add_value('discount_price', product_info['price'])
            sale_item_loader.add_value('quantity', progress['qty'])
            sale_item_loader.add_value('remain', progress['qty_remain'])
            sale_item_loader.add_value('start_time', product['special_from_date'])
            sale_item_loader.add_value('end_time', product['special_to_date'])
            sale_item_loader.add_value('rating', product_info['rating_average'])
            sale_item_loader.add_value('review', product_info['review_count'])
            yield sale_item_loader.load_item()

        # To next page
        paging = content['paging']
        current_page = paging['current_page']
        last_page = paging['last_page']
        if current_page < last_page and current_page < MAX_PAGE:
            yield scrapy.Request(
                url = self.sale_urls[time].format(category_id, current_page + 1), 
                callback = self.parseProduct, 
                meta = {'category_id': category_id}
                )

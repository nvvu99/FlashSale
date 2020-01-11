# -*- coding: utf-8 -*-
import time

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from scrapy.utils.project import get_project_settings

from FlashSale.items import FlashsaleItem

MAXPAGE = 100


class TikiSpider(scrapy.Spider):
    name = 'tiki'
    settings = get_project_settings()
    start_url = settings.get('TIKI')
    list_pager_xpath = '//div[@class="list-pager"]'
    current_page_xpath = './ul/li/span[@class="current"]/text()'
    next_page_xpath = './ul/li/a[@class="next"]'

    def start_requests(self):
        yield scrapy.Request(url=TikiSpider.start_url.format(1), callback=self.parseCategories)
        # driver.quit()

    def parseCategories(self, response):
        categories_xpath = '//div[@class="side-bar"]/ul[@class="filter-category"]'
        category_ids_xpath = './li/label/input/@value'
        category_ids = response.xpath(categories_xpath).xpath(category_ids_xpath).extract()

        # category_id = category_ids[0]
        for category_id in category_ids:
            category_url = response.url + '&category_ids=' + category_id
            yield scrapy.Request(url=category_url, callback=self.parseContents)
            time.sleep(1)

    def parseContents(self, response):
        # parse current page
        deal_items_xpath = '//div[@class="product-listing"]/div[@class="items"]/a[@class="deal-item"]'
        deal_items = response.xpath(deal_items_xpath)
        for deal_item in deal_items:
            # check if item is deal out
            if deal_item.xpath('./p[@class="btn deal-out"]') != []:
                continue

            loader = ItemLoader(item=FlashsaleItem(), selector=deal_item)
            loader.default_output_processor = TakeFirst()

            loader.add_xpath('name', './div[@class="title"]/text()')
            loader.add_xpath('image', './div[@class="image"]/img/@src')
            loader.add_value('link', deal_item.attrib['href'])
            loader.add_xpath('origin_price', './div[@class="price-sale"]/text()')
            loader.add_xpath('discount_price', './div[@class="price-sale"]/span/text()')
            loader.add_xpath('status',
                             './div[@class="deal-status"]/div[@class="process-bar"]/span[@class="text"]/text()')
            loader.add_xpath('progress_status', './div[@class="deal-status"]/div/div/@style')
            loader.add_value('start_time', 'now')
            loader.add_xpath('end_time', './div[@class="deal-status"]/div[@class="started"]/div/span/text()')

            yield loader.load_item()

        # move to next page
        list_pager = response.xpath(TikiSpider.list_pager_xpath)
        # try:
        current_page = int(list_pager.xpath(TikiSpider.current_page_xpath).extract_first())
        next_page = list_pager.xpath(TikiSpider.next_page_xpath)
        if (current_page < MAXPAGE) and (next_page != []):
            next_page = current_page + 1
            next_page_url = response.url.replace('page=' + str(current_page), 'page=' + str(next_page))
            yield scrapy.Request(url=next_page_url, callback=self.parseContents)
            time.sleep(1)
        # except:
        #     print(list_pager.extract())
        #     current_page = list_pager.xpath(TikiSpider.current_page_xpath).extract_first()
        #     print(type(current_page))

    def test(self, response):
        list_pager = response.xpath(TikiSpider.list_pager_xpath)
        current_page = int(list_pager.xpath(TikiSpider.current_page_xpath).extract_first())
        next_page = list_pager.xpath(TikiSpider.next_page_xpath)
        return current_page

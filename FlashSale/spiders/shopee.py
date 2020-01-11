# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy.utils.project import get_project_settings


class ShopeeSpider(scrapy.Spider):
    name = 'shopee'
    settings = get_project_settings()
    urls = settings.get('SHOPEE_API')

    def start_requests(self):
        yield scrapy.Request(url=urls[0], callback=self.parseSessions)

    def parseSessions(self, response):
        contents = json.loads(request.text)
        sessions = contents['data']['sessions']
        # current session
        current_session = sessions[0]
        meta = {
            'start_time': current_session['start_time'],
            'end_time': current_session['end_time'],
            'categories': current_session['categories'],
        }
        query_params = {
            'offset': 0,
            'limit': 16,
            'sort_soldout': True,
            'need_personalize': True,
            'with_dp_items': True
        }
        yield scrapy

    def parseCurrentSession(self, response):
        meta = response.meta

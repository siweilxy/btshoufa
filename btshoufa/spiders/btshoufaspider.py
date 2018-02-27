# -*- coding: utf-8 -*-
from btshoufa.items import BtshoufaItem
import scrapy
from scrapy.loader import ItemLoader
from scrapy.http import Request
from scrapy.loader.processors import MapCompose,Join
from scrapy.spiders import CrawlSpider,Rule
import re
import urlparse
import sys
import logging
import redis

class BtshoufaspiderSpider(CrawlSpider):
    name = 'btshoufaspider'
    allowed_domains = ['www.btshoufa.net']
    #allowed_domains = ['www.btshoufa.net/forum.php']
    start_urls = ['http://www.btshoufa.net/forum.php']
    #start_urls = ["http://www.btshoufa.net/portal.php"]

    def parse(self, response):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        baseUrl="http://www.btshoufa.net/"
        r = redis.Redis(host='192.168.1.16', port=6379, db=0)
        next_selector=response.xpath("//a/@href")
        for url in next_selector.extract():
            if not re.match("http:",url):
                url=baseUrl+url
            #logging.critical("<-----------%s"%url)
            if not re.match("http://www.btshoufa.net/home.php?mod=space&uid=", url):
                if r.get(url) is None and url != baseUrl:
                    if url == baseUrl:
                        logging.critical("this is baseurl")
                    r.set(url,1)
                    if not re.match("http://www.btshoufa.net/forum.php/?mod=attachment",url):
                        yield Request(urlparse.urljoin(response.url,url))

        selector=response.xpath("//a")
        for s in selector:
            yield self.parse_item(s,response)

    def parse_item(self,selector,response):
        l=ItemLoader(item=BtshoufaItem(),selector=selector)
        l.add_xpath('title','./text()')
        l.add_xpath('seed','./@href')

        return l.load_item()

# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import logging
import btshoufa
import scrapy
import re
from scrapy.http import Request
import urlparse

class BtshoufaSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

#www.btshoufa.com/forum.php?mod=attachment&aid=MzIzNjB8NjAwZDRkZmF8MTUxOTY1Mzc2NXwwfDEwNDY0MQ%3D%3D
    def processitem(self,item,response):
        if 'seed' in item:
            #logging.critical(".................")
            if re.match("thread",item['seed'][0]):
                item['seed'][0] = "http://www.btshoufa.net/" + item['seed'][0]
                #logging.critical("thread")
                return Request(urlparse.urljoin(response.url, item['seed'][0]))
            elif re.match("forum",item['seed'][0]):
                item['seed'][0] = "http://www.btshoufa.net/" + item['seed'][0]
                #logging.critical("match forum %s"%item['seed'][0])
            #logging.critical("after match forum%s"%item['seed'][0])
            if re.match("http://www.btshoufa.net/forum.php\?mod=attachment",item['seed'][0]):
                #if re.match("www.btshoufa.com/forum.php?mod=attachment", item['seed'][0]):
                #logging.critical("type is btshoufa.items.BtshoufaItem: ++++++++++++++++++++>%s" % (item["seed"][0]))
                return item
            return Request(urlparse.urljoin(response.url, item['seed'][0]))

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            t=type(i)
            if t is btshoufa.items.BtshoufaItem:
                #logging.critical("processitem")
                yield self.processitem(i, response)
                # logging.critical("type is btshoufa.items.BtshoufaItem:%s %s"%(i["title"][0],i["seed"][0]))
            elif t is scrapy.http.request.Request:
                if not re.match("http://www.btshoufa.net/forum.php\?mod=attachment", i.url):
                    yield i
                #logging.critical("type is scrapy.http.request.Request:%s" % i.url)

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class BtshoufaDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

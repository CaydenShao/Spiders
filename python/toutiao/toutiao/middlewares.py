# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
import time
import random
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from toutiao.settings import USER_AGENT_LIST
import requests
import json
from toutiao.config.IPProxyPoolConfig import IPPOOL
from toutiao.config.CookiesConfig import NEWS_SPIDER_COOKIES_CONFIG

class NewsSpdierMiddleware(object):
    def process_request(self, request, spider):
        if spider.name == "News":
            dcap = dict(DesiredCapabilities.PHANTOMJS)
            dcap["phantomjs.page.settings.userAgent"] = (random.choice(USER_AGENT_LIST))
            driver = webdriver.PhantomJS(desired_capabilities = dcap, service_args = ['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
            global NEWS_SPIDER_COOKIES_CONFIG
            print('*************************COOKIES****************************')
            print(NEWS_SPIDER_COOKIES_CONFIG)
            driver.delete_all_cookies()
            try:
                driver.add_cookie(NEWS_SPIDER_COOKIES_CONFIG)
            except Exception as e:
                print(e)
            driver.get(request.url)
            try:
                element = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@class='y-wrap']//div[@class='y-box container']//div[@class='y-left index-content']//div[@riot-tag='feedBox']//div[@class='feedBox']//div[@riot-tag='wcommonFeed']//div[@class='wcommonFeed']//ul//li[@ga_event='article_item_click']"))
                )
                body = driver.page_source
                NEWS_SPIDER_COOKIES_CONFIG = driver.get_cookies()
                return HtmlResponse(driver.current_url, body = body, encoding='utf-8', request=request)
            finally:
                driver.quit()
            return None
        else:
            request.headers['User-Agent'] = random.choice(USER_AGENT_LIST)


    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

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


class ToutiaoSpiderMiddleware(object):
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

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

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


class ToutiaoDownloaderMiddleware(object):
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

class IPProxyPoolMiddleware(object):
    def process_request(self, request, spider):
        #r = requests.get('http://127.0.0.1:8000/?types=0&count=5&country=国内')
        #ip_ports = json.loads(r.text)
        thisip = random.choice(IPPOOL)
        print("this is ip:"+thisip["ipaddr"])
        request.meta["proxy"] = "http://" + thisip["ipaddr"]
        pass
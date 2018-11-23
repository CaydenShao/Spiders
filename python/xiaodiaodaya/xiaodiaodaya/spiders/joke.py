#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/19 晚上18:19
# @Author  : shaokai
# @Email   : shaokai@outlook.com
# @File    : joke.py
# @Software: VS Code

import scrapy
import json
import re
from scrapy.http import Request
from xiaodiaodaya.items import JokeItem
from xiaodiaodaya.util.source_type_util import get_joke_type
from util.xpath_util import get_select_first_str
from util.print_util import print_with_defaut
from util.string_util import concat_str

class JokeSpider(scrapy.Spider):
    name = 'Joke'
    allowed = ['xiaodiaodaya.cn']
    start_urls = [
        "http://xiaodiaodaya.cn/article/list.aspx?classid=598",
        "http://xiaodiaodaya.cn/article/list.aspx?classid=597",
        "http://xiaodiaodaya.cn/article/list.aspx?classid=623",
        "http://xiaodiaodaya.cn/article/list.aspx?classid=595",
        "http://xiaodiaodaya.cn/article/list.aspx?classid=594",
        "http://xiaodiaodaya.cn/article/list.aspx?classid=593",
        "http://xiaodiaodaya.cn/article/list.aspx?classid=641",
        "http://xiaodiaodaya.cn/article/list.aspx?classid=605",
        "http://xiaodiaodaya.cn/article/list.aspx?classid=590",
        "http://xiaodiaodaya.cn/article/list.aspx?classid=591",
        "http://xiaodiaodaya.cn/article/list.aspx?classid=592",
        "http://xiaodiaodaya.cn/article/list.aspx?classid=596",
    ]

    def start_requests(self):
        cls = self.__class__
        #if method_is_overridden(cls, Spider, 'make_requests_from_url'):
        #    warnings.warn(
        #        "Spider.make_requests_from_url method is deprecated; it "
        #        "won't be called in future Scrapy releases. Please "
        #        "override Spider.start_requests method instead (see %s.%s)." % (
        #            cls.__module__, cls.__name__
        #        ),
        #    )
        for url in self.start_urls:
            start_url = url
            yield self.make_requests_from_url(url, start_url)
        #else:
        #    for url in self.start_urls:
        #        yield Request(url, dont_filter=True, meta={'start_url':start_url})

    def make_requests_from_url(self, url, start_url):
        """ This method is deprecated. """
        return Request(url, dont_filter=True, meta = {'type':None})
    
    def parse(self, response):
        type = 0
        if response.request.meta['type'] is None:
            type = get_joke_type(response.url)
        else:
            type = response.request.meta['type']
        elements = response.xpath("//*[@id='main']/div/div[@class='line1' or @class='line2']")
        if len(elements) <= 0:
            return
        e = elements[0]
        for i in range(len(elements)):
            j = i + 1
            print(str(j))
            head = "//*[@id='main']/div/div[(@class='line1' or @class='line2') and position()=" + str(j) + "]"
            href = get_select_first_str(e, head + "/a/@href", None)
            title = get_select_first_str(e, head + "/a/text()", None)
            if href is not None:
                content_url = href
                yield response.follow(content_url, callback = self.content, meta = {'type':type, 'title':title})
        next_url = get_select_first_str(response, "//*[@id='main']/div/div[@class='pgs cl']/div[@class='pg']/a[text()='下一页']/@href", None)
        if next_url is not None:
            print('###########################')
            print(next_url)
            yield scrapy.Request(next_url, callback = self.parse, meta = {'type':type})

    def content(self, response):
        item = JokeItem()
        title = response.request.meta['title']
        if title != None:
            item['title'] = title.strip()
        else:
            item['title'] = None
        joke_type = title = response.request.meta['type']
        if joke_type != None:
            item['type'] = joke_type
        else:
            item['type'] = None
        text = get_select_first_str(response, "//*[@id='main']/div/div[@class='content']", None)
        if text == None:
            print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
        item['text'] = text
        item['crawl_origin'] = '笑掉大牙网'
        item['crawl_url'] = response.url
        print(concat_str('笑话标题：', title))
        print(concat_str('内容', text))
        return item
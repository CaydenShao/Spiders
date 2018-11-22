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
from jdjhj.items import JokeItem
from jdjhj.util.source_type_util import get_joke_type
from jdjhj.util.source_type_util import get_joke_page_url_head
from util.xpath_util import get_select_first_str
from util.print_util import print_with_defaut
from util.string_util import concat_str

class JokeSpider(scrapy.Spider):
    name = 'Joke'
    allowed = ['www.jdjhj.com']
    start_urls = [
        "http://www.jdjhj.com/wz/yuanchuangxiaohua/index.html",
        "http://www.jdjhj.com/wz/qtxh/index.html",
        "http://www.jdjhj.com/wz/lxh/index.html",
        "http://www.jdjhj.com/wz/zcxh/index.html",
        "http://www.jdjhj.com/wz/tyxh/index.html",
        "http://www.jdjhj.com/wz/jdxh/index.html",
        "http://www.jdjhj.com/wz/xyxh/index.html",
        "http://www.jdjhj.com/wz/gdxh/index.html",
        "http://www.jdjhj.com/wz/kbxh/index.html",
        "http://www.jdjhj.com/wz/xxxh/index.html",
        "http://www.jdjhj.com/wz/crxh/index.html",
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
        return Request(url, dont_filter=True, meta = {'type':None, 'page_url_head':None})
    
    def parse(self, response):
        type = 0
        if response.request.meta['type'] is None:
            type = get_joke_type(response.url)
        else:
            type = response.request.meta['type']
        page_url_head = None
        if response.request.meta['page_url_head'] is None:
            page_url_head = get_joke_page_url_head(response.url)
        else:
            page_url_head = response.request.meta['page_url_head']
        if page_url_head == None:
            print('============================')
            print(response.text)
            return
        elements = response.xpath("//*[@id='main']/div/div[1]/div[2]/ul/li")
        if len(elements) <= 0:
            return
        e = elements[0]
        for i in range(len(elements)):
            j = i + 1
            print(str(j))
            head = "//*[@id='main']/div/div[1]/div[2]/ul/li[position()=" + str(j) + "]"
            href = get_select_first_str(e, head + "/div/h2/a/@href", None)
            title = get_select_first_str(e, head + "/div/h2/a/text()", None)
            if href is not None:
                content_url = "http://www.jdjhj.com" + href
                yield response.follow(content_url, callback = self.content, meta = {'type':type, 'title':title})
        next_url = get_select_first_str(response, "//*[@id='pager']/ul/li/a[text()='下一页']/@href", None)
        if next_url is not None:
            next_url = page_url_head + "/" + next_url
            print('###########################')
            print(next_url)
            yield scrapy.Request(next_url, callback = self.parse, meta = {'type':type, 'page_url_head':page_url_head})

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
        text = get_select_first_str(response, "//*[@id='main']/div/div[1]/div[2]/div[1]/p/span/span", None)
        if text == None:
            text = get_select_first_str(response, "//*[@id='main']/div/div[1]/div[2]/div[1]/p", None)
        if text == None:
            print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
        item['text'] = text
        item['crawl_origin'] = '天天搞笑网'
        item['crawl_url'] = response.url
        print(concat_str('笑话标题：', title))
        print(concat_str('内容', text))
        return item
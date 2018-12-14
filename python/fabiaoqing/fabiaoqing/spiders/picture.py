#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/08 下午16:39
# @Author  : shaokai
# @Email   : shaokai@outlook.com
# @File    : picture.py
# @Software: VS Code

import scrapy
import json
import re
from scrapy.http import Request
from fabiaoqing.items import PictureItem
from fabiaoqing.util.source_type_util import get_source_type
from fabiaoqing.models.picture import Picture
from util.xpath_util import get_select_first_str
from util.print_util import print_with_defaut
from util.string_util import concat_str
from util.source_type_util import get_picture_page_url_head
from util.source_type_util import get_source_type

class PictureSpider(scrapy.Spider):
    name = 'Picture'
    allowed = ['www.fabiaoqing.com']
    start_urls = [
        'https://www.fabiaoqing.com/bqb/lists/type/liaomei.html',
        #'https://www.fabiaoqing.com/bqb/lists/type/qunliao.html',
        #'https://www.fabiaoqing.com/bqb/lists/type/doutu.html',
        #'https://www.fabiaoqing.com/bqb/lists/type/mingxing.html',
        #'https://www.fabiaoqing.com/bqb/lists/type/zhuangbi.html',
        #'https://www.fabiaoqing.com/bqb/lists/type/wu.html',
        #'https://www.fabiaoqing.com/bqb/lists/type/toupai.html',
        #'https://www.fabiaoqing.com/bqb/lists/type/fuli.html',
        #'https://www.fabiaoqing.com/bqb/lists/type/erciyuan.html',
        #'https://www.fabiaoqing.com/bqb/lists/type/meng.html',
        #'https://www.fabiaoqing.com/bqb/lists/type/katong.html',
        #'https://www.fabiaoqing.com/bqb/lists/type/yingshi.html',
        #'https://www.fabiaoqing.com/bqb/lists/type/duiren.html',
        #'https://www.fabiaoqing.com/bqb/lists/type/wenzi.html',
        #'https://www.fabiaoqing.com/bqb/lists/type/emoji.html',
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
        return Request(url, dont_filter=True, meta = {'type':None, 'page_url_head':'https://www.fabiaoqing.com', 'stage':'page'})
    
    def parse(self, response):
        type = 0
        if response.request.meta['type'] is None:
            type = get_source_type(response.url)
        else:
            type = response.request.meta['type']
        page_url_head = None
        if response.request.meta['page_url_head'] is None:
            page_url_head = get_picture_page_url_head(response.url)
        else:
            page_url_head = response.request.meta['page_url_head']
        elements = response.xpath("//*[@id='bqblist']/a")
        if len(elements) <= 0:
            return
        e = elements[0]
        for i in range(len(elements)):
            j = i + 1
            print(str(j))
            head = "//*[@id='bqblist']/a[position()=" + str(j) + "]"
            href = get_select_first_str(e, head + "/@href", None)
            title = get_select_first_str(e, head + "/@title", None)
            if href is not None:
                href = "https://www.fabiaoqing.com" + href
                content_url = href
                pictures = []
                has_error = 'false'
                yield response.follow(content_url, callback = self.content, meta = {'type':type, 'group_url':content_url, 'stage':'content', 'pictures':pictures, 'has_error':has_error})
        next_url = get_select_first_str(response, "//*[@id='bqblist']/div[@class='ui pagination menu']/a[contains(text(), '下一页')]/@href", None)
        if next_url is not None:
            next_url = page_url_head + next_url
            yield response.follow(next_url, callback = self.parse, meta = {'type':type, 'page_url_head':page_url_head, 'stage':'page'})

    def content(self, response):
        type = 0
        if response.request.meta['type'] is None:
            type = get_source_type(response.url)
        else:
            type = response.request.meta['type']
        group_url = None
        if response.request.meta['group_url'] is None:
            group_url = None
        else:
            group_url = response.request.meta['group_url']
        pictures = []
        if response.request.meta['pictures'] is not None:
            pictures = response.request.meta['pictures']
        has_error = 'false'
        if response.request.meta['has_error'] is not None:
            has_error = response.request.meta['has_error']
        title = get_select_first_str(response, "//*[@id='bqb']/div[1]/h1/text()", None)
        if title != None:
            title = title.strip()
        images = response.xpath("//*[@id='bqb']/div[1]/div[1]/div/div/div/a")
        print(response.text)
        if images == None or len(images) == 0:
            has_error = 'true'
        for i in range(len(images)):
            j = i + 1
            print(str(j))
            head = "//*[@id='bqb']/div[1]/div[1]/div/div/div/a[position()=" + str(j) + "]"
            src = get_select_first_str(response, head + "/div/img/@data-original", None)
            description = get_select_first_str(response, head + "/div/img/@title", None)
            picture = {}
            print('====================================')
            print(src)
            picture['url'] = src
            picture['description'] = description
            pictures.append(picture)
        item = PictureItem()
        item['type'] = type
        item['title'] = title
        item['mark'] = None
        item['thumbs_up_times'] = None
        item['crawl_origin'] = '美头网'
        item['crawl_url'] = response.url
        item['group_url'] = group_url
        item['pictures'] = pictures
        item['has_error'] = has_error
        print(concat_str('图片类型：', type))
        print(concat_str('图片标题：', title))
        print(concat_str('group_url：', group_url))
        print('picture_urls：')
        print('has_error:', has_error)
        print(pictures)
        yield item
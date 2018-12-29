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
from wxcha.items import PictureItem
from wxcha.util.source_type_util import get_source_type
from util.xpath_util import get_select_first_str
from util.print_util import print_with_defaut
from util.string_util import concat_str

class PictureSpider(scrapy.Spider):
    name = 'Picture'
    allowed = ['www.wxcha.com']
    start_urls = [
        'http://www.wxcha.com/touxiang/nvsheng/',
        'http://www.wxcha.com/touxiang/nansheng/',
        'http://www.wxcha.com/touxiang/qinglv/',
        'http://www.wxcha.com/touxiang/gexing/',
        'http://www.wxcha.com/touxiang/katong/',
        'http://www.wxcha.com/touxiang/mingxing/',
        'http://www.wxcha.com/touxiang/feizhuliu/',
        'http://www.wxcha.com/touxiang/gaoxiao/',
        'http://www.wxcha.com/touxiang/wenzi/',
        'http://www.wxcha.com/biaoqing/gaoxiao/',
        'http://www.wxcha.com/biaoqing/dongman/',
        'http://www.wxcha.com/biaoqing/wenzi/',
        'http://www.wxcha.com/biaoqing/zhufu/',
        'http://www.wxcha.com/biaoqing/dongtai/',
        'http://www.wxcha.com/biaoqing/feizhuliu/',
        'http://www.wxcha.com/biaoqing/liaotian/',
        'http://www.wxcha.com/biaoqing/keai/',
        'http://www.wxcha.com/biaoqing/tieba/',
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
        return Request(url, dont_filter=True, meta = {'type':None, 'stage':'page'})
    
    def parse(self, response):
        type = 0
        if response.request.meta['type'] is None:
            type = get_source_type(response.url)
        else:
            type = response.request.meta['type']
        elements = response.xpath("/html/body/div[5]/div[1]/ul/li")
        if len(elements) <= 0:
            return
        e = elements[0]
        for i in range(len(elements)):
            j = i + 1
            print(str(j))
            head = "/html/body/div[5]/div[1]/ul/li[position()=" + str(j) + "]"
            href = get_select_first_str(e, head + "//a[position()=1]//@href", None)
            if href is not None:
                content_url = href
                picture_urls = []
                has_error = 'false'
                yield response.follow(content_url, callback = self.content, meta = {'type':type, 'group_url':content_url, 'stage':'content', 'picture_urls':picture_urls, 'has_error':has_error})
        next_url = get_select_first_str(response, "/html/body/div[5]/div[1]/div/a[text()='下一页']/@href", None)
        if next_url is not None:
            yield response.follow(next_url, callback = self.parse, meta = {'type':type, 'stage':'page'})

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
        picture_urls = []
        if response.request.meta['picture_urls'] is not None:
            picture_urls = response.request.meta['picture_urls']
        has_error = 'false'
        if response.request.meta['has_error'] is not None:
            has_error = response.request.meta['has_error']
        title = get_select_first_str(response, "/html/body/div[5]/div[1]/div[1]/h1/text()", None)
        if title != None:
            title = title.strip()
        mark = self.parse_mark(response)
        thumbs_up = get_select_first_str(response, "/html/body/div[5]/div[1]/div[4]/a[1]/i/text()", None)
        thumbs_up_times = None
        if thumbs_up == None:
            thumbs_up_times = None
        else:
            r = re.findall('[0-9]\d*', thumbs_up)
            if r != None and r.__len__() > 0:
                thumbs_up_times = int(r[0])
                if '万' in thumbs_up:
                    thumbs_up_times = thumbs_up_times * 10000
        images = response.xpath("//*[@id='txtabbox']/div[2]/ul/li")
        if images == None or len(images) == 0:
            images = response.xpath("/html/body/div[5]/div[1]/ul/li")
            if images == None or len(images) == 0:
                has_error = 'true'
            else:
                for i in range(len(images)):
                    j = i + 1
                    print(str(j))
                    head = "/html/body/div[5]/div[1]/ul/li[position()=" + str(j) + "]"
                    src = get_select_first_str(response, head + "/img/@data-original", None)
                    picture_urls.append(src)
        else:
            for i in range(len(images)):
                j = i + 1
                print(str(j))
                head = "//*[@id='txtabbox']/div[2]/ul/li[position()=" + str(j) + "]"
                src = get_select_first_str(response, head + "//a//img/@data-original", None)
                picture_urls.append(src)
        item = PictureItem()
        item['type'] = type
        item['title'] = title
        item['mark'] = mark
        item['thumbs_up_times'] = thumbs_up_times
        item['crawl_origin'] = '微茶'
        item['crawl_url'] = response.url
        item['group_url'] = group_url
        item['picture_urls'] = picture_urls
        item['has_error'] = has_error
        print(concat_str('图片类型：', type))
        print(concat_str('图片标题：', title))
        print(concat_str('图片标签：', mark))
        print(concat_str('点赞数量：', str(thumbs_up_times)))
        print(concat_str('group_url：', group_url))
        print('picture_urls：')
        print('has_error:', has_error)
        print(picture_urls)
        yield item
    
    def parse_mark(self, response):
        mark = None
        index = 1
        result = get_select_first_str(response, "/html/body/div[5]/div[1]/div[6]/p/a[position()='1']/text()", None)
        if result != None:
            while True:
                r = get_select_first_str(response, "/html/body/div[5]/div[1]/div[6]/p/a[position()=" + str(index) + "]/text()", None)
                if r == None:
                    break
                index = index + 1
                if mark == None:
                    mark = r
                else:
                    mark = mark + ',' + r
        else:
            result = get_select_first_str(response, "/html/body/div[5]/div[1]/div[5]/p/a[position()='1']/text()", None)
            index = 1
            if result != None:
                while True:
                    r = get_select_first_str(response, "/html/body/div[5]/div[1]/div[5]/p/a[position()=" + str(index) + "]/text()", None)
                    if r == None:
                        break
                    index = index + 1
                    if mark == None:
                        mark = r
                    else:
                        mark = mark + ',' + r
        return mark
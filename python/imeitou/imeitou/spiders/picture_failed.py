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
import pymysql
from scrapy.http import Request
from imeitou.items import PictureItem
from imeitou.util.source_type_util import get_source_type
from util.xpath_util import get_select_first_str
from util.print_util import print_with_defaut
from util.string_util import concat_str
from imeitou.config.db_config import DB_CONFIG

class PictureFailedSpider(scrapy.Spider):
    name = 'PictureFailed'
    allowed = ['www.wxcha.com']
    start_urls = []
    type_mappings = {}
    # 读取需要爬取的图片分组url
    db = pymysql.connect(**DB_CONFIG)
    cursor = db.cursor()
    try:
        sql = "SELECT DISTINCT group_url, type FROM picture_crawl_failed;"
        cursor.execute(sql)
        datas = cursor.fetchall()
        count = 0
        for data in datas:
            if data[0] != None:
                count += 1
                print(str(count) + ':' + data[0])
                start_urls.append(data[0])
                type_mappings[data[0]] = data[1]
        db.commit() # 提交数据
    except Exception as e:
        print(e)
        db.rollback()
    finally:
        cursor.close()
        db.close()

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
        picture_urls = []
        has_error = 'false'
        type = None
        if self.type_mappings.__contains__(start_url):
            type = self.type_mappings[start_url]
        return Request(url, dont_filter=True, meta = {'type':type, 'group_url':start_url, 'stage':'content', 'picture_urls':picture_urls, 'has_error':has_error})
    
    def parse(self, response):
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
        title = get_select_first_str(response, "/html/body/div[3]/div[3]/div[1]/div[1]/div[1]/h1/text()", None)
        if title != None:
            title = title.strip()
        images = response.xpath("//*[@id='content']/ul/center/img")
        if images == None or len(images) == 0:
            images = response.xpath("//*[@id='content']/ul/center//img")
            if images == None or len(images) == 0:
                has_error = 'true'
            else:
                divs = response.xpath("//*[@id='content']/ul/center//div")
                for d in range(len(divs)):
                    images = response.xpath("//*[@id='content']/ul/center//div[position()=" + str(d) + "]//img")
                    for i in range(len(images)):
                        j = i + 1
                        print(str(j))
                        head = "//*[@id='content']/ul/center//div[position()=" + str(d) + "]//img[position()=" + str(j) + "]"
                        src = get_select_first_str(response, head + "/@src", None)
                        picture_urls.append(src)
        else:
            for i in range(len(images)):
                j = i + 1
                print(str(j))
                head = "//*[@id='content']/ul/center/img[position()=" + str(j) + "]"
                src = get_select_first_str(response, head + "/@src", None)
                picture_urls.append(src)
        item = PictureItem()
        item['type'] = type
        item['title'] = title
        item['mark'] = None
        item['thumbs_up_times'] = None
        item['crawl_origin'] = '美头网'
        item['crawl_url'] = response.url
        item['group_url'] = group_url
        item['picture_urls'] = picture_urls
        item['has_error'] = has_error
        print(concat_str('图片类型：', type))
        print(concat_str('图片标题：', title))
        print(concat_str('group_url：', group_url))
        print('picture_urls：')
        print('has_error:', has_error)
        print(picture_urls)
        yield item
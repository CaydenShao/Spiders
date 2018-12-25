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
from fabiaoqing.items import PictureItem
from fabiaoqing.util.source_type_util import get_source_type
from util.xpath_util import get_select_first_str
from util.print_util import print_with_defaut
from util.string_util import concat_str
from fabiaoqing.config.db_config import DB_CONFIG

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
        pictures = []
        has_error = 'false'
        type = None
        if self.type_mappings.__contains__(start_url):
            type = self.type_mappings[start_url]
        return Request(url, dont_filter=True, meta = {
            'type':type, 
            'group_url':start_url, 
            'stage':'content', 
            'pictures':pictures, 
            'has_error':has_error
            })
    
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
        pictures = []
        if response.request.meta['pictures'] is not None:
            pictures = response.request.meta['pictures']
        has_error = 'false'
        if response.request.meta['has_error'] is not None:
            has_error = response.request.meta['has_error']
        title = get_select_first_str(response, "//*[@id='bqb']/div[1]/h1/text()", None)
        if title != None:
            title = title.strip()
        images = response.xpath("//*[@id='bqb']//div[1]//div[1]//div//div//div[@class='bqppdiv1']")
        if images == None or len(images) == 0:
            has_error = 'true'
        else:
            for i in range(len(images)):
                j = i + 1
                print(str(j))
                head = "//*[@id='bqb']//div[1]//div[1]//div//div//div[position()=" + str(j) + "]"
                src = get_select_first_str(response, head + "//img//@data-original", None)
                description = get_select_first_str(response, head + "//img//@title", None)
                picture = {}
                picture['url'] = src
                picture['description'] = description
                pictures.append(picture)
        marks = response.xpath('//*[@id="bqb"]/div[1]/div[2]/a')
        mark = ''
        if marks == None or len(marks) == 0:
            mark = None
        else:
            for i in range(len(marks)):
                j = i + 1
                mark_str = get_select_first_str(response, '//*[@id="bqb"]/div[1]/div[2]/a[position()=' + str(j) + "]/@title", None)
                mark = mark + mark_str.replace("表情包", "") + ','
            if mark != '':
                mark = mark[:-1]
        item = PictureItem()
        item['type'] = type
        item['title'] = title
        item['mark'] = mark
        item['thumbs_up_times'] = None
        item['crawl_origin'] = '发表情'
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
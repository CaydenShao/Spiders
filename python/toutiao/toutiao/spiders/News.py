#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/21 下午16:05
# @Author  : shaokai
# @Email   : shaokai@outlook.com
# @File    : NewsHot.py
# @Software: VS Code

import scrapy
import json
import re
from util.XPathUtil import get_select_first_str
from util.PrintUtil import print_with_defaut
from util.StringUtil import concat_str
from util.NewsTypeUtil import get_news_type
from toutiao.items import NewsItem
from config.RepeatUrlConfig import REPEAT_URL_CONFIG
from models import RepeatUrlConfig

class NewsSpider(scrapy.Spider):
    name = 'News'
    allowed = ['www.toutiao.com']
    start_urls = []
    # 添加要爬去的url
    for config in REPEAT_URL_CONFIG:
        for i in range(config.get_times()):
            start_urls.append(config.get_url())

    def parse(self, response):
        elements = response.xpath("//div[@class='y-wrap']//div[@class='y-box container']//div[@class='y-left index-content']//div[@riot-tag='feedBox']//div[@class='feedBox']//div[@riot-tag='wcommonFeed']//div[@class='wcommonFeed']//ul//li[@ga_event='article_item_click']")
        e = elements[0]
        for i in range(len(elements)):
            item = NewsItem()
            j = i + 1
            print(str(j))
            item['type'] = get_news_type(response.url)
            head = "//div[@class='y-wrap']//div[@class='y-box container']//div[@class='y-left index-content']//div[@riot-tag='feedBox']//div[@class='feedBox']//div[@riot-tag='wcommonFeed']//div[@class='wcommonFeed']//ul//li[@ga_event='article_item_click' and position()=" + str(j) + "]"
            title = get_select_first_str(e, head + "//div[@class='item-inner y-box']//div[@class='rbox-inner']//div[@class='title-box']//a/text()", None)
            if title != None:
                item['title'] = title.strip()
            else:
                item['title'] = None
            media_url = get_select_first_str(e, head + "//div[@class='item-inner y-box']//a[@class='lbtn media-avatar']/@href", None)
            if media_url != None:
                media_url = 'https://www.toutiao.com' + media_url
                item['media_url'] = media_url
            else:
                item['media_url'] = None
            media_avatar_img = get_select_first_str(e, head + "//div[@class='item-inner y-box']//a[@class='lbtn media-avatar']//img/@src", None)
            if media_avatar_img != None:
                media_avatar_img = 'https:' + media_avatar_img
                item['media_avatar_img'] = media_avatar_img
            else:
                item['media_avatar_img'] = None
            media_name = get_select_first_str(e, head + "//div[@class='item-inner y-box']//a[@class='lbtn source']/text()", None)
            if media_name != None:
                media_name = media_name.replace('\xa0', '')
                media_name = media_name.replace('⋅', '')
            item['media_name'] = media_name
            comment = get_select_first_str(e, head + "//div[@class='item-inner y-box']//a[@class='lbtn comment']/text()", None)
            if comment == None:
                item['comment_count'] = None
            else:
                r = re.findall('[1-9]\d*', comment)
                if r != None and r.__len__() > 0:
                    comment_count = int(r[0])
                    if '万' in comment:
                        comment_count = comment_count * 10000
                    item['comment_count'] = comment_count
                else:
                    item['comment_count'] = None
            article_img = get_select_first_str(e, head + "//div[@class='item-inner y-box']//a[@class='img-wrap']//img/@src", None)
            if article_img != None:
                article_img = 'https:' + article_img
                item['article_img'] = article_img
            else:
                item['article_img'] = None
            article_url = get_select_first_str(e, head + "//div[@class='item-inner y-box']//a[@class='link title']/@href", None)
            if article_url != None:
                article_url = 'https://www.toutiao.com' + article_url
                item['article_url'] = article_url
            else:
                item['article_url'] = None
            item['mark'] = None
            item['crawl_origin'] = '今日头条'
            item['crawl_url'] = response.url
            print(concat_str('文章标题：', title))
            print(concat_str('源媒体：', media_url))
            print(concat_str('源媒体头像：', media_avatar_img))
            print(concat_str('源媒体名称：', media_name))
            print(concat_str('评论数：', comment))
            print(concat_str('文章图片：', article_img))
            print(concat_str('文章url：', article_url))
            yield item
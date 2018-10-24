#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/21 下午16:05
# @Author  : shaokai
# @Email   : shaokai@outlook.com
# @File    : NewsHot.py
# @Software: VS Code

import scrapy
import json
from util.XPathUtil import get_select_first_str
from util.PrintUtil import print_with_defaut
from util.StringUtil import concat_str

class NewsHotSpider(scrapy.Spider):
    name = 'NewsHot'
    allowed = ['www.toutiao.com']
    #start_urls = ['https://www.toutiao.com/ch/news_hot/']
    start_urls = ['https://www.toutiao.com/ch/news_tech/']

    def parse(self, response):
        elements = response.xpath("//div[@class='y-wrap']//div[@class='y-box container']//div[@class='y-left index-content']//div[@riot-tag='feedBox']//div[@class='feedBox']//div[@riot-tag='wcommonFeed']//div[@class='wcommonFeed']//ul//li[@ga_event='article_item_click']")
        e = elements[0]
        print("---------------------------------------------------")
        for i in range(len(elements)):
            j = i + 1
            print(str(j))
            head = "//div[@class='y-wrap']//div[@class='y-box container']//div[@class='y-left index-content']//div[@riot-tag='feedBox']//div[@class='feedBox']//div[@riot-tag='wcommonFeed']//div[@class='wcommonFeed']//ul//li[@ga_event='article_item_click' and position()=" + str(j) + "]"
            title = get_select_first_str(e, head + "//div[@class='item-inner y-box']//div[@class='rbox-inner']//div[@class='title-box']//a/text()", None)
            media_url = get_select_first_str(e, head + "//div[@class='item-inner y-box']//a[@class='lbtn media-avatar']/@href", None)
            if media_url != None:
                media_url = 'https://www.toutiao.com' + media_url
            media_avatar_img = get_select_first_str(e, head + "//div[@class='item-inner y-box']//a[@class='lbtn media-avatar']//img/@src", None)
            if media_avatar_img != None:
                media_avatar_img = 'https:' + media_avatar_img
            media_name = get_select_first_str(e, head + "//div[@class='item-inner y-box']//a[@class='lbtn source']/text()", None)
            comment = get_select_first_str(e, head + "//div[@class='item-inner y-box']//a[@class='lbtn comment']/text()", None)
            article_img = get_select_first_str(e, head + "//div[@class='item-inner y-box']//a[@class='img-wrap']//img/@src", None)
            if article_img != None:
                article_img = 'https:' + article_img
            article_url = get_select_first_str(e, head + "//div[@class='item-inner y-box']//a[@class='link title']/@href", None)
            if article_url != None:
                article_url = 'https://www.toutiao.com' + article_url
            print(concat_str('文章标题：', title))
            print(concat_str('源媒体：', media_url))
            print(concat_str('源媒体头像：', media_avatar_img))
            print(concat_str('源媒体名称：', media_name))
            print(concat_str('评论数：', comment))
            print(concat_str('文章图片：', article_img))
            print(concat_str('文章url：', article_url))
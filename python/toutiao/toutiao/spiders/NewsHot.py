#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/21 下午16:05
# @Author  : shaokai
# @Email   : shaokai@outlook.com
# @File    : NewsHot.py
# @Software: VS Code

import scrapy

class NewsHotSpider(scrapy.Spider):
    name = 'NewsHot'
    allowed = ['www.toutiao.com']
    start_urls = ['https://www.toutiao.com/ch/news_hot/']

    def parse(self, response):
        print('response_url:' + response.url)
        elements = response.xpath("//div[@class='y-wrap']//div[@class='y-box container']//div[@class='y-left index-content']//div[@riot-tag='feedBox']//div[@class='feedBox']//div[@riot-tag='wcommonFeed']//div[@class='wcommonFeed']//ul//li")
        print("---------------------------------------------------")
        print(elements)
        for e in elements:
            title = e.xpath("//div[@class='item-inner y-box']//div[@class='rbox-inner']//div[@class='title-box']//a/text()").extract_first()
            media_url = 'https://www.toutiao.com' + e.xpath("//div[@class='item-inner y-box']//a[@class='lbtn media-avatar']/@href").extract_first()
            media_avatar_img = 'https:' + e.xpath("//div[@class='item-inner y-box']//a[@class='lbtn media-avatar']//img/@src").extract_first()
            media_name = e.xpath("//div[@class='item-inner y-box']//a[@class='lbtn source']/text()").extract_first()
            comment = e.xpath("//div[@class='item-inner y-box']//a[@class='lbtn comment']/text()").extract_first()
            article_img = 'https:' + e.xpath("//div[@class='item-inner y-box']//a[@class='img-wrap']//img/@src").extract_first()
            article_url = 'https://www.toutiao.com' + e.xpath("//div[@class='item-inner y-box']//a[@class='img-wrap']/@href").extract_first()
            print('文章标题：' + title)
            print('源媒体：' + media_url)
            print('源媒体头像：' + media_avatar_img)
            print('源媒体名称：' + media_name)
            print('评论数：' + comment)
            print('文章图片：' + article_img)
            print('文章url：' + article_url)
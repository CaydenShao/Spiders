#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/25 下午16:05
# @Author  : shaokai
# @Email   : shaokai@outlook.com
# @File    : NewsHot.py
# @Software: VS Code

import scrapy

class ContentSpider(scrapy.Spider):
    name = 'Content'
    allowed = ['www.toutiao.com']
    start_urls = ['https://www.toutiao.com/a6615945226852762119/']

    def parse(self, response):
        print('response.content:' + response.text)
        content = response.xpath("//div[@class='y-box container']//div[@class='y-left index-middle']//div[@id='article-main']")
        print('content:')
        print(content.extract_first())
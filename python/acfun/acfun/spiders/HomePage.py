#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/14 晚上23:53
# @Author  : shaokai
# @Email   : shaokai@outlook.com
# @File    : HomePage.py
# @Software: VS Code

import scrapy
import sys
from acfun.items import HomePageItem

class HomePageSpider(scrapy.Spider):
    name = 'HomePage'
    allowed = ["www.acfun.cn"]
    start_urls = ["http://www.acfun.cn/"]

    def parse(self, response):
        type = sys.getfilesystemencoding() 
        print(response.text)
        f = open('homepage.html', 'w', encoding='utf-8')
        f.write(response.text)
        f.close()
        item = HomePageItem()
        
        return item
        
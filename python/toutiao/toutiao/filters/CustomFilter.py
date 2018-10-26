#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/26 下午19:05
# @Author  : shaokai
# @Email   : shaokai@outlook.com
# @File    : CustomFilter.py
# @Software: VS Code

from scrapy.dupefilter import RFPDupeFilter
from models.RepeatUrlConfig import RepeatUrlConfig

class CustomFilter(RFPDupeFilter):
    def __init__(self):
        self.configs = set([
            RepeatUrlConfig('https://www.toutiao.com/ch/news_hot/', 20),
            RepeatUrlConfig('https://www.toutiao.com/ch/news_tech/', 10)
        ])

    def get_config(self, url):
        for config in self.configs:
            if config.get_url == url:
                return config
        return None

    def request_seen(self, request):
        #-------------自定义部分--------------
        config = self.get_config(request.url)
        if config != None:
            if config.can_repeat():
                config.request()
                return False
        #------------------------------------
        fp = self.request_fingerprint(request)
        if fp in self.fingerprints:
            return True
        self.fingerprints.add(fp)
        if self.file:
            self.file.write(fp + os.linesep)
            
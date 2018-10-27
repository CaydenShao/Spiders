#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/26 下午19:05
# @Author  : shaokai
# @Email   : shaokai@outlook.com
# @File    : CustomFilter.py
# @Software: VS Code

from scrapy.dupefilters import RFPDupeFilter
from models.RepeatUrlConfig import RepeatUrlConfig
import os

class CustomFilter(RFPDupeFilter):
    configs = set([
        RepeatUrlConfig('https://www.toutiao.com/ch/news_hot/', 2),
        RepeatUrlConfig('https://www.toutiao.com/ch/news_tech/', 1)
    ])

    def get_config(self, url):
        for config in self.configs:
            print(config.to_string())
            if config.get_url() == url:
                return config
        return None

    def request_seen(self, request):
        #-------------自定义部分--------------
        config = self.get_config(request.url)
        if config != None:
            if config.can_repeat():
                config.request()
                return False
            else:
                return True
        #------------------------------------
        fp = self.request_fingerprint(request)
        if fp in self.fingerprints:
            return True
        self.fingerprints.add(fp)
        if self.file:
            self.file.write(fp + os.linesep)
            
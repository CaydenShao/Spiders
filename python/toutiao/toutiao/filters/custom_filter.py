#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/26 下午19:05
# @Author  : shaokai
# @Email   : shaokai@outlook.com
# @File    : CustomFilter.py
# @Software: VS Code

from scrapy.dupefilters import RFPDupeFilter
from models.repeat_url_config import RepeatUrlConfig
from config.repeat_url_config import REPEAT_URL_CONFIG
import os

class CustomFilter(RFPDupeFilter):
    def get_config(self, url):
        for config in REPEAT_URL_CONFIG:
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
            
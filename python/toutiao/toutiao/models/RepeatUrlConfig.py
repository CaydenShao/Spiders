#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/26 下午19:05
# @Author  : shaokai
# @Email   : shaokai@outlook.com
# @File    : RepeatUrlConfig.py
# @Software: VS Code

class RepeatUrlConfig(object):
    def __init__(self, request_url, request_times):
        self.url = request_url
        self.times = request_times
        self.current_times = 0

    def get_url(self):
        return self.url

    def get_times(self):
        return self.times

    def get_current_times(self):
        return self.current_times

    def request(self):
        if self.can_repeat():
            self.current_times = self.current_times + 1
            return True
        else:
            return False

    def can_repeat(self):
        if self.times <= self.current_times:
            return False
        else:
            return True
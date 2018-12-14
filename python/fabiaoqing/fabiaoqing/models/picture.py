#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/14 下午12:05
# @Author  : shaokai
# @Email   : shaokai@outlook.com
# @File    : picture.py
# @Software: VS Code

class Picture(object):
    def __init__(self, picture_url, picture_description):
        self.url = picture_url
        self.description = picture_description
    
    def get_url(self):
        return self.url
    
    def get_description(self):
        return self.description
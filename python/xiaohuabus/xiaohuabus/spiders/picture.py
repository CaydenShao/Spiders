#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/19 晚上18:19
# @Author  : shaokai
# @Email   : shaokai@outlook.com
# @File    : picture.py
# @Software: VS Code

import scrapy
import json
import re
from xiaohuabus.items import PictureItem
from util.xpath_util import get_select_first_str
from util.print_util import print_with_defaut
from util.string_util import concat_str

class PictureSpider(scrapy.Spider):
    name = 'Picture'
    allowed = ['www.xiaohuabus.com']
    start_urls = ['http://www.xiaohuabus.com/picNews.html']
    
    def parse(self, response):
        elements = response.xpath("//div[@class='th']//div[@class='main']//div[@class='main_info']")
        if len(elements) <= 0:
            return None
        e = elements[0]
        for i in range(len(elements)):
            item = PictureItem()
            j = i + 1
            print(str(j))
            item['type'] = '1'
            head = "//div[@class='th']//div[@class='main']//div[@class='main_info' and position()=" + str(j) + "]"
            title = get_select_first_str(e, head + "//div[@class='main_info_top']//div[@id='main_info_top_right']//div[@class='head_title_2']//span//a//h1/text()", None)
            if title != None:
                item['title'] = title.strip()
            else:
                item['title'] = None
            mark = None
            index = 1
            while True:
                r = get_select_first_str(e, head + "//div[@class='main_info_top']//div[@id='main_info_top_right']//div[@id='head_title']//div[@class='publish_info']//span//a[position()=" + str(index) + "]/text()", None)
                if r == None:
                    break
                index = index + 1
                if mark == None:
                    mark = r
                else:
                    mark = mark + ',' + r
            item['mark'] = mark
            media_url = get_select_first_str(e, head + "//div[@class='main_info_top']//div[@class='main_info_top_left']//div[@id='head_photo']//a/@href", None)
            if media_url != None:
                media_url = 'http://www.xiaohuabus.com' + media_url
                item['media_url'] = media_url
            else:
                item['media_url'] = None
            media_avatar_img = get_select_first_str(e, head + "//div[@class='main_info_top']//div[@class='main_info_top_left']//div[@id='head_photo']//a//img/@src", None)
            if media_avatar_img != None:
                media_avatar_img = 'http://www.xiaohuabus.com' + media_avatar_img
                item['media_avatar_img'] = media_avatar_img
            else:
                item['media_avatar_img'] = None
            media_name = get_select_first_str(e, head + "//div[@class='main_info_top']//div[@id='main_info_top_right']//div[@id='head_title']//div[@class='user_info']//span[@id='yonghuming']//a/text()", None)
            if media_name != None:
                media_name = media_name.replace('\xa0', '')
                media_name = media_name.replace('⋅', '')
            item['media_name'] = media_name
            thumbs_up = get_select_first_str(e, head + "//div[@class='feix']//div[@class='feix_right']//a[position()=1]//span[position()=2]/text()", None)
            thumbs_up_times = None
            if thumbs_up == None:
                item['thumbs_up_times'] = None
            else:
                r = re.findall('[1-9]\d*', thumbs_up)
                if r != None and r.__len__() > 0:
                    thumbs_up_times = int(r[0])
                    if '万' in thumbs_up:
                        thumbs_up_times = thumbs_up_times * 10000
                    item['thumbs_up_times'] = thumbs_up_times
                else:
                    item['thumbs_up_times'] = None
            thumbnail = get_select_first_str(e, head + "//div[@class='main_info_bottom']//p//img/@src", None)
            item['picture_url'] = thumbnail
            item['thumbnail'] = thumbnail
            item['crawl_origin'] = '笑话巴士'
            item['crawl_url'] = response.url
            print(concat_str('图片标题：', title))
            print(concat_str('源媒体：', media_url))
            print(concat_str('源媒体头像：', media_avatar_img))
            print(concat_str('源媒体名称：', media_name))
            print(concat_str('获赞数：', str(thumbs_up_times)))
            print(concat_str('标签：', mark))
            print(concat_str('缩略图：', thumbnail))
            print(concat_str('图片：', thumbnail))
            yield item
        next_url = get_select_first_str(response, "//div[@class='th']//div[@class='main']//div[@class='pager']//a[@class='page' and text()='下一页']/@href", None)
        if next_url is not None:
            next_url = "http:" + next_url
            yield scrapy.Request(next_url, callback = self.parse)
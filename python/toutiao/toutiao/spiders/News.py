#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/21 下午16:05
# @Author  : shaokai
# @Email   : shaokai@outlook.com
# @File    : NewsHot.py
# @Software: VS Code

import scrapy
import json
import re
from util.XPathUtil import get_select_first_str
from util.PrintUtil import print_with_defaut
from util.StringUtil import concat_str
from util.NewsTypeUtil import get_news_type
from toutiao.items import NewsItem
from config.RepeatUrlConfig import REPEAT_URL_CONFIG
from models import RepeatUrlConfig

class NewsSpider(scrapy.Spider):
    name = 'News'
    allowed = ['www.toutiao.com']
    start_urls = [
        #'https://www.toutiao.com/ch/news_hot/', # 热点
        #'https://www.toutiao.com/ch/news_tech/', # 科技
        #'https://www.toutiao.com/ch/internet/', # 互联网
        #'https://www.toutiao.com/ch/software/', # 软件
        #'https://www.toutiao.com/ch/smart_home/', # 智能家居
        #'https://www.toutiao.com/ch/news_entertainment/', # 娱乐
        #'https://www.toutiao.com/ch/movie/', # 电影
        #'https://www.toutiao.com/ch/teleplay/', # 电视剧
        #'https://www.toutiao.com/ch/shows/', # 综艺
        #'https://www.toutiao.com/ch/gossip/', # 明星八卦
        #'https://www.toutiao.com/ch/news_game/', # 游戏
        #'https://www.toutiao.com/ch/news_sports/', # 体育
        #'https://www.toutiao.com/ch/nba/', # NBA
        #'https://www.toutiao.com/ch/cba/', # CBA
        #'https://www.toutiao.com/ch/csl/', # 中超
        #'https://www.toutiao.com/ch/football_italy/', # 意甲
        #'https://www.toutiao.com/ch/news_car/', # 汽车
        #'https://www.toutiao.com/ch/car_new_arrival/', # 新车
        #'https://www.toutiao.com/ch/suv/', # SUV
        #'https://www.toutiao.com/ch/car_guide/', # 汽车导购
        #'https://www.toutiao.com/ch/car_usage/', # 用车
        #'https://www.toutiao.com/ch/news_finance/', # 财经
        #'https://www.toutiao.com/ch/investment/', # 投资
        #'https://www.toutiao.com/ch/stock_channel/', # 股票
        #'https://www.toutiao.com/ch/finance_management/', # 理财
        #'https://www.toutiao.com/ch/macro_economic/', # 宏观经济
        #'https://www.toutiao.com/ch/funny/', # 搞笑
        #'https://www.toutiao.com/ch/news_military/', # 军事
        #'https://www.toutiao.com/ch/military_china/', # 中国军情
        #'https://www.toutiao.com/ch/weaponry/', # 武器装备
        #'https://www.toutiao.com/ch/military_world/', # 环球军事
        #'https://www.toutiao.com/ch/news_world/', # 国际
        #'https://www.toutiao.com/ch/news_fashion/', # 时尚
        #'https://www.toutiao.com/ch/fashion/', # 时装
        #'https://www.toutiao.com/ch/body_shaping/', # 美体
        #'https://www.toutiao.com/ch/watch/', # 腕表
        #'https://www.toutiao.com/ch/jewelry/', # 珠宝
        #'https://www.toutiao.com/ch/news_travel/', # 旅游
        #'https://www.toutiao.com/ch/news_discovery/', # 探索
        #'https://www.toutiao.com/ch/news_baby/', # 育儿
        #'https://www.toutiao.com/ch/news_regimen/', # 养生
        #'https://www.toutiao.com/ch/news_essay/', # 美文
        #'https://www.toutiao.com/ch/news_history/', # 历史
        #'https://www.toutiao.com/ch/news_food/', # 美食
        ]
    # 添加要爬去的url
    for config in REPEAT_URL_CONFIG:
        for i in range(config.get_times()):
            start_urls.append(config.get_url())

    def parse(self, response):
        elements = response.xpath("//div[@class='y-wrap']//div[@class='y-box container']//div[@class='y-left index-content']//div[@riot-tag='feedBox']//div[@class='feedBox']//div[@riot-tag='wcommonFeed']//div[@class='wcommonFeed']//ul//li[@ga_event='article_item_click']")
        e = elements[0]
        for i in range(len(elements)):
            item = NewsItem()
            j = i + 1
            print(str(j))
            item['type'] = get_news_type(response.url)
            head = "//div[@class='y-wrap']//div[@class='y-box container']//div[@class='y-left index-content']//div[@riot-tag='feedBox']//div[@class='feedBox']//div[@riot-tag='wcommonFeed']//div[@class='wcommonFeed']//ul//li[@ga_event='article_item_click' and position()=" + str(j) + "]"
            title = get_select_first_str(e, head + "//div[@class='item-inner y-box']//div[@class='rbox-inner']//div[@class='title-box']//a/text()", None)
            if title != None:
                item['title'] = title.strip()
            else:
                item['title'] = None
            media_url = get_select_first_str(e, head + "//div[@class='item-inner y-box']//a[@class='lbtn media-avatar']/@href", None)
            if media_url != None:
                media_url = 'https://www.toutiao.com' + media_url
                item['media_url'] = media_url
            else:
                item['media_url'] = None
            media_avatar_img = get_select_first_str(e, head + "//div[@class='item-inner y-box']//a[@class='lbtn media-avatar']//img/@src", None)
            if media_avatar_img != None:
                media_avatar_img = 'https:' + media_avatar_img
                item['media_avatar_img'] = media_avatar_img
            else:
                item['media_avatar_img'] = None
            media_name = get_select_first_str(e, head + "//div[@class='item-inner y-box']//a[@class='lbtn source']/text()", None)
            if media_name != None:
                media_name = media_name.replace('\xa0', '')
                media_name = media_name.replace('⋅', '')
            item['media_name'] = media_name
            comment = get_select_first_str(e, head + "//div[@class='item-inner y-box']//a[@class='lbtn comment']/text()", None)
            if comment == None:
                item['comment_count'] = None
            else:
                r = re.findall('[1-9]\d*', comment)
                if r != None and r.__len__() > 0:
                    comment_count = int(r[0])
                    if '万' in comment:
                        comment_count = comment_count * 10000
                    item['comment_count'] = comment_count
                else:
                    item['comment_count'] = None
            article_img = get_select_first_str(e, head + "//div[@class='item-inner y-box']//a[@class='img-wrap']//img/@src", None)
            if article_img != None:
                article_img = 'https:' + article_img
                item['article_img'] = article_img
            else:
                item['article_img'] = None
            article_url = get_select_first_str(e, head + "//div[@class='item-inner y-box']//a[@class='link title']/@href", None)
            if article_url != None:
                article_url = 'https://www.toutiao.com' + article_url
                item['article_url'] = article_url
            else:
                item['article_url'] = None
            print(concat_str('文章标题：', title))
            print(concat_str('源媒体：', media_url))
            print(concat_str('源媒体头像：', media_avatar_img))
            print(concat_str('源媒体名称：', media_name))
            print(concat_str('评论数：', comment))
            print(concat_str('文章图片：', article_img))
            print(concat_str('文章url：', article_url))
            response.follow(article_url, callback = self.content)
            yield item

    def content(self, response):
        print('===================================================')
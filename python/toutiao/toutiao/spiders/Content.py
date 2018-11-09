#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/25 下午16:05
# @Author  : shaokai
# @Email   : shaokai@outlook.com
# @File    : NewsHot.py
# @Software: VS Code

import scrapy
import pymysql
from toutiao.config.NewsDBConfig import news_db_config
from toutiao.items import ContentItem

class ContentSpider(scrapy.Spider):
    name = 'Content'
    allowed = ['www.toutiao.com']
    start_urls = []
    # 读取需要爬取的文章内容url
    db = pymysql.connect(**news_db_config)
    cursor = db.cursor()
    try:
        sql = "SELECT DISTINCT news.article_url FROM news WHERE news.article_url NOT IN (SELECT article_url FROM news_content);"
        cursor.execute(sql)
        datas = cursor.fetchall()
        count = 0
        for data in datas:
            if data[0] != None:
                count += 1
                print(str(count) + ':' + data[0])
                start_urls.append(data[0])
        db.commit() # 提交数据
    except Exception as e:
        print(e)
        db.rollback()
    finally:
        cursor.close()
        db.close()

    def parse(self, response):
        content = response.xpath("//div[@class='y-box container']//div[@class='y-left index-middle']//div[@id='article-main']")
        print(content)
        if content == None:
            return
        text = content.extract_first()
        if text == None:
            return
        item = ContentItem()
        item['content'] = content
        item['article_url'] = response.url
        print('content:')
        print(content.extract_first())
        return item
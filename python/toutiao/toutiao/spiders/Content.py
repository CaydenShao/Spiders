#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/25 下午16:05
# @Author  : shaokai
# @Email   : shaokai@outlook.com
# @File    : NewsHot.py
# @Software: VS Code

import scrapy
import pymysql
from toutiao.config.NewsDBConfig import NEWS_DB_CONFIG
from toutiao.items import ContentItem
from scrapy.http import Request

class ContentSpider(scrapy.Spider):
    name = 'Content'
    allowed = []
    start_urls = []
    # 读取需要爬取的文章内容url
    db = pymysql.connect(**NEWS_DB_CONFIG)
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
    
    def start_requests(self):
        cls = self.__class__
        #if method_is_overridden(cls, Spider, 'make_requests_from_url'):
        #    warnings.warn(
        #        "Spider.make_requests_from_url method is deprecated; it "
        #        "won't be called in future Scrapy releases. Please "
        #        "override Spider.start_requests method instead (see %s.%s)." % (
        #            cls.__module__, cls.__name__
        #        ),
        #    )
        for url in self.start_urls:
            start_url = url
            yield self.make_requests_from_url(url, start_url)
        #else:
        #    for url in self.start_urls:
        #        yield Request(url, dont_filter=True, meta={'start_url':start_url})

    def make_requests_from_url(self, url, start_url):
        """ This method is deprecated. """
        return Request(url, dont_filter=True, meta={'start_url':start_url})

    def parse(self, response):
        item = ContentItem()
        item['crawl_result'] = "false"
        item['content'] = None
        item['article_url'] = response.meta['start_url']
        item['target_url'] = response.url
        item['article_origin'] = -1
        content = response.xpath("//div[@class='y-box container']//div[@class='y-left index-middle']//div[@id='article-main']")
        text = None
        if content == None:
            content = response.xpath("//body")
            if content == None:
                print("--------------Content is None----------------")
                return item
            else:
                text = content.extract_first()
                item['article_origin'] = 2
        else:
            text = content.extract_first()
            if text == None:
                content = response.xpath("//body")
                if content == None:
                    print("--------------Content is None----------------")
                    return item
                else:
                    text = content.extract_first()
                    item['article_origin'] = 2
            else:
                item['article_origin'] = 1
        if text == None:
            print("--------------头条文章 Text is None----------------")
            return item
        item['crawl_result'] = "true"
        item['content'] = text
        item['article_url'] = response.meta['start_url']
        item['target_url'] = response.url
        print('---------------文章内容----------------')
        print(text)
        return item
        
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XiaodiaodayaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class JokeItem(scrapy.Item):
    type = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()
    crawl_origin = scrapy.Field()
    crawl_url = scrapy.Field()
    pass
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WxchaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class PictureItem(scrapy.Item):
    result = scrapy.Field()
    type = scrapy.Field()
    title = scrapy.Field()
    mark = scrapy.Field()
    thumbs_up_times = scrapy.Field()
    picture_url = scrapy.Field()
    crawl_origin = scrapy.Field()
    crawl_url = scrapy.Field()
    group_url = scrapy.Field()
    pass

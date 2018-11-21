# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XiaohuabusItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class PictureItem(scrapy.Item):
    type = scrapy.Field()
    title = scrapy.Field()
    media_url = scrapy.Field()
    media_avatar_img = scrapy.Field()
    media_name = scrapy.Field()
    thumbs_up_times = scrapy.Field()
    thumbnail = scrapy.Field()
    picture_url = scrapy.Field()
    mark = scrapy.Field()
    crawl_origin = scrapy.Field()
    crawl_url = scrapy.Field()
    pass

class TextItem(scrapy.Item):
    type = scrapy.Field()
    title = scrapy.Field()
    media_url = scrapy.Field()
    media_avatar_img = scrapy.Field()
    media_name = scrapy.Field()
    thumbs_up_times = scrapy.Field()
    text = scrapy.Field()
    mark = scrapy.Field()
    crawl_origin = scrapy.Field()
    crawl_url = scrapy.Field()
    pass

class JokeItem(scrapy.Item):
    type = scrapy.Field()
    title = scrapy.Field()
    media_url = scrapy.Field()
    media_avatar_img = scrapy.Field()
    media_name = scrapy.Field()
    thumbs_up_times = scrapy.Field()
    text = scrapy.Field()
    mark = scrapy.Field()
    crawl_origin = scrapy.Field()
    crawl_url = scrapy.Field()
    pass

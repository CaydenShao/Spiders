# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):
    # define the fields for your item here like:
    type = scrapy.Field()
    title = scrapy.Field()
    media_url = scrapy.Field()
    media_avatar_img = scrapy.Field()
    media_name = scrapy.Field()
    comment_count = scrapy.Field()
    article_img = scrapy.Field()
    article_url = scrapy.Field()
    mark = scrapy.Field()
    crawl_origin = scrapy.Field()
    crawl_url = scrapy.Field()
    pass

class ContentItem(scrapy.Item):
    # define the fields for your item here like:
    article_url = scrapy.Field()
    content = scrapy.Field()
    pass

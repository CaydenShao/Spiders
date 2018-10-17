# -*- coding: utf-8 -*-
import scrapy
from AoiSolas.items import AoisolasItem

class AoisolaspiderSpider(scrapy.Spider):
    name = "AoiSola"
    allowed_domain = ["www.mm131.com"]
    start_urls = [
        'http://www.mm131.com/xinggan/',
        'http://www.mm131.com/qingchun/',
        'http://www.mm131.com/xiaohua/',
        'http://www.mm131.com/chemo/',
        'http://www.mm131.com/qipao/',
        'http://www.mm131.com/mingxing/'
    ]

    def parse(self, response):
        list = response.css('.list-left dd:not(.page)')
        for img in list:
            imgname = img.css('a::text').extract_first()
            imgurl = img.css('a::attr(href)').extract_first()
            imgurl2 = str(imgurl)
            print(imgurl2)
            next_url = response.css('.page-en:nth-last-child(2)::attr(href)').extract_first()
            if next_url is not None:
                # 下一页
                yield response.follow(next_url, callback = self.parse)
            yield scrapy.Request(imgurl2, callback = self.content)

    def content(self, response):
        item = AoisolasItem()
        item['name'] = response.css('.content h5::text').extract_first()
        item['ImgUrl'] = response.css('.content-pic img::attr(src)').extract_first()
        yield item
        # 提取图片，存入文件夹
        # print(item['ImgUrl'])
        next_url = response.css('.page-ch:last-child::attr(href)').extract_first()

        if next_url is not None:
            # 下一页
            yield response.follow(next_url, callback = self.content)
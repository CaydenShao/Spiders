import scrapy
from scrapy_test.items import ImagespiderItem

class ImgSpider(scrapy.Spider):
    name = 'ImgSpider'
    allowed_domains = ['lab.scrapyd.cn']
    start_urls = ['http://lab.scrapyd.cn/archives/55.html']

    def parse(self, response):
        item = ImagespiderItem() # 实例化item
        imgurls = response.css(".post img::attr(src)").extract() # 这里是一个集合也就是多张图片
        item['imgurl'] = imgurls
        yield item
        pass
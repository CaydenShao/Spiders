import scrapy
from myimage.items import MyimageItem

class MyimageSpider(scrapy.Spider):
    name = 'myimage'
    allowed_domains = ['www.mmonly.cc']
    start_urls = ['http://www.mmonly.cc/tag/yr/']

    def parse(self, response):
        print("url:" + response.url)
        items = response.xpath("//div[@class='Clbc_Game']//div[@class='item_list infinite_scroll masonry']/div[@class='item masonry_brick masonry-brick']")
        for i in items:
            item = MyimageItem()
            imageurl = i.xpath("//div[@class='item_b clearfix']//div[@class='items_comment']//a/@title").extract_first()
            item["name"] = str(imageurl)
            print(item["name"])
            item["image_url"] = i.xpath("div[@class='item_t']//div[@class='img']//div[@class='ABox']//a//img/@original").extract_first()
            print(item["image_url"])
            yield item
        print("responseurl:" + response.url)
        next_url = response.xpath("//div[@class='wrappic']//div[@class='pages']//ul//li//a[text()='下一页']/@href").extract_first()
        print(next_url)
        if next_url is not None:
            yield response.follow(next_url, callback = self.parse)
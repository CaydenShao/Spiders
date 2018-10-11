# -*- coding: utf-8 -*-
# 比如我们要爬取标签：爱情，我们可以这样：scrapy crawl argsSpider -a tag=爱情

import scrapy

class ArgsSpider(scrapy.Spider):
    name = 'argsSpider'

    def start_requests(self):
        url = 'http://lab.scrapyd.cn/'
        tag = getattr(self, 'tag', None) # 获取tag值，也就是爬取时传过来的参数
        if tag is not None: # 判断是否存在tag，若存在，重新构造url
            url = url + 'tag/' + tag # 构造url若tag=爱情，url="http://lab.scrapyd.cn/tag/爱情"
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        cayden = response.css('div.quote')
        for v in cayden: # 循环获取每一条名言里面的：名言内容、作者、标签
            text = v.css('.text::text').extract_first() # 提取名言
            author = v.css('.author::text').extract_first() # 提取作者
            tags = v.css('.tags .tag::text').extract_first() # 提取标签
            tags = ','.join(tags) # 数组转换为字符串
            filename = '%s-语录.txt' % author # 爬取的内容存入文件，文件名为：作者-语录.txt
            with open(filename, "a+") as f: # 追加写入文件
                f.write(text) # 写入名言内容
                f.write('\n') # 换行
                f.write('标签：' + tags) # 写入标签
                f.write('\n---------\n')
                f.close() # 关闭文件操作
        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
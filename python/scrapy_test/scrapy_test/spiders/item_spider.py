import scrapy

class itemSpider(scrapy.Spider):
    name = 'itemSpider'
    start_urls = ['http://lab.scrapyd.cn']

    def parse(self, response):
        cayden = response.css('div.quote')
        
        for v in cayden:
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
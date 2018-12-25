# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from jdjhj.config.db_config import DB_CONFIG
from jdjhj.util.encryption_util import get_md5_value

class JdjhjPipeline(object):
    def process_item(self, item, spider):
        if spider.name == "Joke":
            if item['type'] == None or item['title'] == None or item['text'] == None or item['crawl_url'] == None:
                return item
            db = pymysql.connect(**DB_CONFIG)
            cursor = db.cursor()
            try:
                sql = "INSERT INTO joke "
                sql += "("
                sql += "type, "
                sql += "title, "
                sql += "content, "
                sql += "crawl_time, "
                sql += "crawl_origin, "
                sql += "crawl_url, "
                sql += "crawl_url_md5"
                sql += ") "
                sql += "VALUES (%s, %s, %s, now(), %s, %s, %s);"
                cursor.execute(sql, (
                    item['type'], 
                    item['title'], 
                    item['text'], 
                    item['crawl_origin'], 
                    item['crawl_url'], 
                    get_md5_value(bytes(item['crawl_url'], encoding = "utf8"))
                    ))
                print("the last rowid is", cursor.lastrowid)
                db.commit()
            except Exception as e:
                print(e)
                db.rollback()
            finally:
                cursor.close()
                db.close()
        return item

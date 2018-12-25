# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from xiaohuabus.config.db_config import DB_CONFIG
from xiaohuabus.util.encryption_util import get_md5_value

class XiaohuabusPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'Picture':
            if item['type'] == None or item['title'] == None or item['picture_url'] == None or item['crawl_origin'] == None or item['crawl_url'] == None:
                return item
            db = pymysql.connect(**DB_CONFIG)
            cursor = db.cursor()
            try:
                sql = "INSERT INTO picture "
                sql += "("
                sql += "type, "
                sql += "title, "
                sql += "media_url, "
                sql += "media_avatar_img, "
                sql += "media_name, "
                sql += "thumbs_up_times, "
                sql += "thumbnail, "
                sql += "picture_url, "
                sql += "picture_url_md5, "
                sql += "mark, "
                sql += "crawl_time, "
                sql += "crawl_origin, "
                sql += "crawl_url"
                sql += ") "
                sql += "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), %s, %s);"
                cursor.execute(sql, (
                    item['type'], 
                    item['title'], 
                    item['media_url'], 
                    item['media_avatar_img'], 
                    item['media_name'], 
                    item['thumbs_up_times'], 
                    item['thumbnail'], 
                    item['picture_url'], 
                    get_md5_value(bytes(item['picture_url'], encoding = "utf8")), 
                    item['mark'], 
                    item['crawl_origin'], 
                    item['crawl_url']
                    ))
                print("the last rowid is", cursor.lastrowid)
                db.commit()
            except Exception as e:
                print(e)
                db.rollback()
            finally:
                cursor.close()
                db.close()
        if spider.name == "Joke":
            if item['type'] == None or item['title'] == None or item['text'] == None or item['crawl_origin'] == None or item['crawl_url'] == None:
                return item
            db = pymysql.connect(**DB_CONFIG)
            cursor = db.cursor()
            try:
                sql = "INSERT INTO joke "
                sql += "("
                sql += "type, "
                sql += "title, "
                sql += "media_url, "
                sql += "media_avatar_img, "
                sql += "media_name, "
                sql += "thumbs_up_times, "
                sql += "content, "
                sql += "mark, "
                sql += "crawl_time, "
                sql += "crawl_origin, "
                sql += "crawl_url, "
                sql += "crawl_url_md5"
                sql += ") "
                sql += "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, now(), %s, %s, %s);"
                cursor.execute(sql, (
                    item['type'], 
                    item['title'], 
                    item['media_url'], 
                    item['media_avatar_img'], 
                    item['media_name'], 
                    item['thumbs_up_times'], 
                    item['text'], 
                    item['mark'], 
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

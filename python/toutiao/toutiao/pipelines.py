# -*- coding: utf-8 -*-

import pymysql
from toutiao.config.NewsDBConfig import NEWS_DB_CONFIG
from toutiao.config.ContentDBConfig import CONTENT_DB_CONFIG
from toutiao.util.EncryptionUtil import get_md5_value

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

class ToutiaoPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'News':
            if item['type'] == None or item['title'] == None or item['article_url'] == None or item['crawl_origin'] == None or item['crawl_url'] == None:
                return
            db = pymysql.connect(**NEWS_DB_CONFIG)
            cursor = db.cursor()
            try:
                sql = "INSERT INTO news (type, title, media_url, media_avatar_img, media_name, comment_count, article_img, article_url, article_url_md5, mark, crawl_time, crawl_origin, crawl_url) "
                sql += "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), %s, %s);"
                cursor.execute(sql, (item['type'], item['title'], item['media_url'], item['media_avatar_img'], item['media_name'], item['comment_count'], item['article_img'], item['article_url'], get_md5_value(bytes(item['article_url'], encoding = "utf8")), item['mark'], item['crawl_origin'], item['crawl_url']))
                print("the last rowid is", cursor.lastrowid)
                db.commit()
            except Exception as e:
                print(e)
                db.rollback()
            finally:
                cursor.close()
                db.close()
        if spider.name == 'Content':
            if item['article_url'] == None:
                return
            if item['content'] == None or item['crawl_result'] == 'false':
                # 爬取失败
                db = pymysql.connect(**CONTENT_DB_CONFIG)
                cursor = db.cursor()
                try:
                    sql = "UPDATE news SET crawl_failed_times = crawl_failed_times + 1 WHERE article_url = %s;"
                    cursor.execute(sql, (item['article_url']))
                    print("Update the crawl_failed_times sucess!")
                    db.commit()
                except Exception as e:
                    print(e)
                    db.rollback()
                finally:
                    cursor.close()
                    db.close()
            if item['content'] != None and item['crawl_result'] == 'true':
                db = pymysql.connect(**CONTENT_DB_CONFIG)
                cursor = db.cursor()
                try:
                    sql = "INSERT INTO news_content (article_url, target_url, content, crawl_time) "
                    sql += "VALUES (%s, %s, %s, now());"
                    cursor.execute(sql, (item['article_url'], item['target_url'], item['content']))
                    print("the last rowid is", cursor.lastrowid)
                    db.commit()
                except Exception as e:
                    print(e)
                    db.rollback()
                finally:
                    cursor.close()
                    db.close()

# -*- coding: utf-8 -*-

import pymysql
from toutiao.config.db_config import DB_CONFIG
from toutiao.util.encryption_util import get_md5_value

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

class ToutiaoPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'News':
            if item['type'] == None or item['title'] == None or item['article_url'] == None or item['crawl_origin'] == None or item['crawl_url'] == None:
                return
            db = pymysql.connect(**DB_CONFIG)
            cursor = db.cursor()
            try:
                sql = "INSERT INTO news "
                sql += "("
                sql += "type, "
                sql += "title, "
                sql += "media_url, "
                sql += "media_avatar_img, "
                sql += "media_name, "
                sql += "comment_count, "
                sql += "article_img, "
                sql += "article_url, "
                sql += "article_url_md5, "
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
                    item['comment_count'], 
                    item['article_img'], 
                    item['article_url'], 
                    get_md5_value(bytes(item['article_url'], encoding = "utf8")), 
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
        if spider.name == 'Content':
            if item['article_url'] == None:
                return
            if item['content'] == None or item['crawl_result'] == 'false':
                # 爬取失败
                db = pymysql.connect(**DB_CONFIG)
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
                db = pymysql.connect(**DB_CONFIG)
                cursor = db.cursor()
                try:
                    sql = "INSERT INTO news_content "
                    sql += "("
                    sql += "article_url, "
                    sql += "target_url, "
                    sql += "article_origin, "
                    sql += "content, "
                    sql += "crawl_time"
                    sql += ") "
                    sql += "VALUES (%s, %s, %s, %s, now());"
                    cursor.execute(sql, (
                        item['article_url'], 
                        item['target_url'], 
                        item['article_origin'], 
                        item['content']
                        ))
                    print("the last rowid is", cursor.lastrowid)
                    db.commit()
                except Exception as e:
                    print(e)
                    db.rollback()
                finally:
                    cursor.close()
                    db.close()

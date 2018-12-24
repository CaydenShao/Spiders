# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from fabiaoqing.config.db_config import DB_CONFIG
from fabiaoqing.util.encryption_util import get_md5_value

class FabiaoqingPipeline(object):
    def process_item(self, item, spider):
        if spider.name == "Picture" or spider.name == "PictureFailed":
            if item['group_url'] == None:
                return item
            if item['title'] == None or len(item['pictures']) == 0 or item['has_error'] == 'true':
                db = pymysql.connect(**DB_CONFIG)
                cursor = db.cursor()
                try:
                    sql = "INSERT INTO picture_crawl_failed (group_url, group_url_md5, type) "
                    sql += "VALUES (%s, %s, %s);"
                    group_url_md5 = get_md5_value(bytes(item['group_url'], encoding = "utf8"))
                    cursor.execute(sql, (item['group_url'], group_url_md5, item['type']))
                    print("the last rowid is", cursor.lastrowid)
                    db.commit()
                except Exception as e:
                    print(e)
                    db.rollback()
                finally:
                    cursor.close()
                    db.close()
            else:
                db = pymysql.connect(**DB_CONFIG)
                cursor = db.cursor()
                try:
                    sql = "DELETE FROM picture_crawl_failed WHERE group_url_md5 = %s;"
                    group_url_md5 = get_md5_value(bytes(item['group_url'], encoding = "utf8"))
                    cursor.execute(sql, (group_url_md5))
                    sql = "INSERT INTO picture_group (type, title, thumbs_up_times, mark, group_url, group_url_md5, crawl_time, crawl_origin, crawl_url) "
                    sql += "VALUES (%s, %s, %s, %s, %s, %s, now(), %s, %s);"
                    cursor.execute(sql, (item['type'], item['title'], item['thumbs_up_times'], item['mark'], item['group_url'], group_url_md5, item['crawl_origin'], item['crawl_url']))
                    picture_group_id = cursor.lastrowid
                    print("the last rowid is", picture_group_id)
                    pictures = item['pictures']
                    for p in pictures:
                        sql = "INSERT INTO picture (picture_group_id, description, picture_url, picture_url_md5) "
                        sql += "VALUES (%s, %s, %s, %s);"
                        cursor.execute(sql, (picture_group_id, p['description'], p['url'], get_md5_value(bytes(p['url'], encoding = "utf8"))))
                        print("the last rowid is", cursor.lastrowid)
                    db.commit()
                except Exception as e:
                    print(e)
                    db.rollback()
                finally:
                    cursor.close()
                    db.close()
        return item

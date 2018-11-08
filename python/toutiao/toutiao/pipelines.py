# -*- coding: utf-8 -*-

import pymysql
from toutiao.config.NewsDBConfig import news_db_config
from toutiao.util.EncryptionUtil import get_md5_value

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

class ToutiaoPipeline(object):
    def process_item(self, item, spider):
        if spider.name == 'News':
            db = pymysql.connect(**news_db_config)
            cursor = db.cursor()
            try:
                sql = "INSERT INTO news (type, title, media_url, media_avatar_img, media_name, comment_count, article_img, article_url, mark, crawl_time, crawl_origin, crawl_url) "
                sql += "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, current_date(), %s, %s);"
                # execute返回受影响的行数
                cursor.execute(sql, (item['type'], item['title'], item['media_url'], item['media_avatar_img'], item['media_name'], item['comment_count'], item['article_url'], item['article_url'], item['mark'], item['crawl_origin'], item['crawl_url']))
                # 当表中有自增的主键的时候，可以使用lastrowid来获取最后一次自增的ID
                print("the last rowid is", cursor.lastrowid)
                db.commit() # 提交数据
            except Exception as e:
                print(e)
                db.rollback()
            finally:
                cursor.close()
                db.close()

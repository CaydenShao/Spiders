import pymysql
from config.db_config import DB_CONFIG
from config.db_config import PERSISTENCE_DB_CONFIG

def persistence_insert(news, content):
    if news != None and content != None:
        db = pymysql.connect(**PERSISTENCE_DB_CONFIG)
        cursor = db.cursor()
        result = True
        try:
            sql = "INSERT INTO news (type, title, media_url, media_avatar_img, media_name, comment_count, article_img, article_url, article_url_md5, mark, crawl_time, crawl_origin, crawl_url) "
            sql += "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), %s, %s);"
            cursor.execute(sql, (news['type'], news['title'], news['media_url'], news['media_avatar_img'], news['media_name'], news['comment_count'], news['article_img'], news['article_url'], news['article_url_md5'], news['mark'], news['crawl_origin'], news['crawl_url']))
            print("the last rowid is", cursor.lastrowid)
            news['news_id'] = cursor.lastrowid
            sql = "INSERT INTO news_content (news_id, target_url, article_origin, content, crawl_time) "
            sql += "VALUES (%s, %s, %s, %s, now());"
            cursor.execute(sql, (news['news_id'], content['target_url'], content['article_origin'], content['content']))
            print("the last rowid is", cursor.lastrowid)
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()
            result = False
        finally:
            cursor.close()
            db.close()
        return result
    else:
        return True

if __name__ == "__main__":
    index = 0
    failed = 0
    error = 0
    while True:
        db = pymysql.connect(**DB_CONFIG)
        cursor = db.cursor()
        news_data = {}
        content_data = {}
        try:
            sql = "SELECT news_id, type, title, media_url, media_avatar_img, media_name, comment_count, article_img, article_url, article_url_md5, mark, crawl_time, crawl_origin, crawl_url FROM news "
            sql += "ORDER BY news_id limit " + str(index) + ",1;"
            cursor.execute(sql)
            datas = cursor.fetchall()
            if datas == None or datas.__len__() <= 0:
                index = index - 1
                break
            for data in datas:
                if data[0] != None:
                    news_data['news_id'] = data[0]
                    news_data['type'] = data[1]
                    news_data['title'] = data[2]
                    news_data['media_url'] = data[3]
                    news_data['media_avatar_img'] = data[4]
                    news_data['media_name'] = data[5]
                    news_data['comment_count'] = data[6]
                    news_data['article_img'] = data[7]
                    news_data['article_url'] = data[8]
                    news_data['article_url_md5'] = data[9]
                    news_data['mark'] = data[10]
                    news_data['crawl_time'] = data[11]
                    news_data['crawl_origin'] = data[12]
                    news_data['crawl_url'] = data[13]
                else:
                    break
            sql = "SELECT news_content_id, article_url, target_url, article_origin, content, crawl_time FROM news_content "
            sql += "WHERE article_url = %s;"
            cursor.execute(sql, (news_data['article_url']))
            datas = cursor.fetchall()
            for data in datas:
                if data[0] != None:
                    content_data['news_content_id'] = data[0]
                    content_data['news_id'] = data[1]
                    content_data['target_url'] = data[2]
                    content_data['article_origin'] = data[3]
                    content_data['content'] = data[4]
                    content_data['crawl_time'] = data[5]
            if persistence_insert(news_data, content_data):
                print("=======Insert success!========")
            else:
                print("=======Insert failed!========")
                failed = failed + 1
            db.commit() # 提交数据
        except Exception as e:
            print(e)
            db.rollback()
            error = error + 1
        finally:
            index = index + 1
            cursor.close()
            db.close()
    print("----------------persistence end-----------------")
    print("count:" + str(index) + ",failed:" + str(failed) + ",error:" + str(error))
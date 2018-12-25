import pymysql
from config.db_config import DB_CONFIG
from config.db_config import PERSISTENCE_DB_CONFIG

def persistence_insert(essay):
    if essay != None:
        db = pymysql.connect(**PERSISTENCE_DB_CONFIG)
        cursor = db.cursor()
        result = True
        try:
            sql = "INSERT INTO essay "
            sql += "("
            sql += "type, "
            sql += "title, "
            sql += "text, "
            sql += "mark, "
            sql += "media_url, "
            sql += "media_avatar_img, "
            sql += "media_name, "
            sql += "comment_count, "
            sql += "thumbs_up_times, "
            sql += "img_url, "
            sql += "crawl_time, "
            sql += "crawl_origin, "
            sql += "crawl_url, "
            sql += "crawl_url_md5"
            sql += ") "
            sql += "VALUES "
            sql += "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(sql, (
                essay['type'], 
                essay['title'], 
                essay['text'], 
                None, 
                None, 
                None, 
                None, 
                None, 
                None, 
                None, 
                essay['crawl_time'], 
                essay['crawl_origin'], 
                essay['crawl_url'],
                essay['crawl_url_md5']
                ))
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
        essay = {}
        try:
            sql = "SELECT "
            sql += "joke_id, "
            sql += "type, "
            sql += "title, "
            sql += "content, "
            sql += "crawl_time, "
            sql += "crawl_origin, "
            sql += "crawl_url, "
            sql += "crawl_url_md5 "
            sql += "FROM joke "
            sql += "ORDER BY joke_id limit " + str(index) + ",1;"
            cursor.execute(sql)
            datas = cursor.fetchall()
            if datas == None or datas.__len__() <= 0:
                index = index - 1
                break
            for data in datas:
                if data[0] != None:
                    essay['joke_id'] = data[0]
                    essay['type'] = data[1]
                    essay['title'] = data[2]
                    essay['text'] = data[3]
                    essay['crawl_time'] = data[4]
                    essay['crawl_origin'] = data[5]
                    essay['crawl_url'] = data[6]
                    essay['crawl_url_md5'] = data[7]
                else:
                    break
            if persistence_insert(essay):
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
import pymysql
from config.db_config import DB_CONFIG
from config.db_config import PERSISTENCE_DB_CONFIG

def persistence_insert(group, pictures):
    if group != None and pictures != None:
        db = pymysql.connect(**PERSISTENCE_DB_CONFIG)
        cursor = db.cursor()
        result = True
        try:
            sql = "INSERT INTO picture_group "
            sql += "("
            sql += "type, "
            sql += "title, "
            sql += "mark, "
            sql += "group_url, "
            sql += "group_url_md5, "
            sql += "media_url, "
            sql += "media_avatar_img, "
            sql += "media_name, "
            sql += "comment_count, "
            sql += "thumbs_up_times, "
            sql += "crawl_time, "
            sql += "crawl_origin, "
            sql += "crawl_url"
            sql += ") "
            sql += "VALUES "
            sql += "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(sql, (
                group['type'], 
                group['title'], 
                group['mark'], 
                group['group_url'], 
                group['group_url_md5'], 
                None, 
                None, 
                None, 
                None, 
                group['thumbs_up_times'], 
                group['crawl_time'], 
                group['crawl_origin'], 
                group['crawl_url']
                ))
            print("the last rowid is", cursor.lastrowid)
            picture_group_id = cursor.lastrowid
            if pictures == None or len(pictures) == 0:
                print('图片分组没有图片')
                result = False
                db.rollback()
            else:
                for p in pictures:
                    sql = "INSERT INTO picture "
                    sql += "("
                    sql += "picture_group_id, "
                    sql += "description, "
                    sql += "picture_url, "
                    sql += "picture_url_md5"
                    sql += ") "
                    sql += "VALUES (%s, %s, %s, %s);"
                    cursor.execute(sql, (
                        picture_group_id, 
                        None, 
                        p['picture_url'], 
                        p['picture_url_md5']
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
        group_data = {}
        pictures_data = []
        try:
            sql = "SELECT "
            sql += "picture_group_id, "
            sql += "type, "
            sql += "title, "
            sql += "thumbs_up_times, "
            sql += "mark, "
            sql += "group_url, "
            sql += "group_url_md5, "
            sql += "crawl_time, "
            sql += "crawl_origin, "
            sql += "crawl_url "
            sql += "FROM picture_group "
            sql += "ORDER BY picture_group_id limit " + str(index) + ",1;"
            cursor.execute(sql)
            datas = cursor.fetchall()
            if datas == None or datas.__len__() <= 0:
                index = index - 1
                break
            for data in datas:
                if data[0] != None:
                    group_data['picture_group_id'] = data[0]
                    group_data['type'] = data[1]
                    group_data['title'] = data[2]
                    group_data['thumbs_up_times'] = data[3]
                    group_data['mark'] = data[4]
                    group_data['group_url'] = data[5]
                    group_data['group_url_md5'] = data[6]
                    group_data['crawl_time'] = data[7]
                    group_data['crawl_origin'] = data[8]
                    group_data['crawl_url'] = data[9]
                else:
                    break
            sql = "SELECT "
            sql += "picture_id, "
            sql += "picture_group_id, "
            sql += "picture_url, "
            sql += "picture_url_md5 "
            sql += "FROM picture "
            sql += "WHERE picture_group_id = %s;"
            cursor.execute(sql, (group_data['picture_group_id']))
            datas = cursor.fetchall()
            for data in datas:
                if data[0] != None:
                    picture_data = {}
                    picture_data['picture_id'] = data[0]
                    picture_data['picture_group_id'] = data[1]
                    picture_data['picture_url'] = data[2]
                    picture_data['picture_url_md5'] = data[3]
                    pictures_data.append(picture_data)
            if persistence_insert(group_data, pictures_data):
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
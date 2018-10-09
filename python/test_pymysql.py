import pymysql

config = {
    "host" : "127.0.0.1", 
    "user" : "root", 
    "password" : "123456",
    "database" : "imooc"
}

def select():
    # 连接数据库
    db = pymysql.connect(**config)
    # 使用cursor()方法创建一个游标对象
    cursor = db.cursor()
    # 使用execute()方法执行SQL语句
    cursor.execute("SELECT * FROM imooc_goddess;")
    # 使用fetchall()获取全部数据
    # fetchone():获取下一行数据，第一次为首行；
    # fetchall():获取所有行数据源
    # fetchmany(4):获取下4行数据
    data = cursor.fetchall()
    # cursor.scroll(1,mode='relative')  # 相对当前位置移动
    # cursor.scroll(2,mode='absolute') # 相对绝对位置移动
    # 第一个值为移动的行数，整数为向下移动，负数为向上移动，mode指定了是相对当前位置移动，还是相对于首行移动
    # 打印获取到的数据
    print(data)
    # 关闭游标和数据库的连接
    cursor.close()
    db.close()

def insert():
    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql = "INSERT INTO imooc_goddess (user_name, sex, age, birthday, email, mobile, create_user, create_date, update_user, update_date, isdel) "
    sql += "VALUES ('小玲', 1, 20, '1998-12-20', 'xiaoling@163.com', 13988888888, 'ADMIN', current_date(), 'ADMIN', current_date(), 1);"
    cursor.execute(sql)
    db.commit() # 提交数据
    cursor.close()
    db.close()

def insert2(): # 推荐（防止SQL注入）
    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql = "INSERT INTO imooc_goddess (user_name, sex, age, birthday, email, mobile, create_user, create_date, update_user, update_date, isdel) "
    sql += "VALUES (%s, %s, %s, %s, %s, %s, %s, current_date(), %s, current_date(), %s);"
    # execute返回受影响的行数
    cursor.execute(sql, ('小甜', 1, 19, '1999-12-20', 'xiaoling@163.com', 13988888888, 'ADMIN', 'ADMIN', 1))
    # 当表中有自增的主键的时候，可以使用lastrowid来获取最后一次自增的ID
    print("the last rowid is", cursor.lastrowid)
    db.commit() # 提交数据
    cursor.close()
    db.close()

def insert_many():
    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql = "INSERT INTO imooc_goddess (user_name, sex, age, birthday, email, mobile, create_user, create_date, update_user, update_date, isdel) "
    sql += "VALUES (%s, %s, %s, %s, %s, %s, %s, current_date(), %s, current_date(), %s);"
    # executemany返回受影响的行数
    cursor.executemany(sql, [('小甜', 1, 19, '1999-12-20', 'xiaoling@163.com', 13988888888, 'ADMIN', 'ADMIN', 1), ('小甜', 1, 19, '1999-12-20', 'xiaoling@163.com', 13988888888, 'ADMIN', 'ADMIN', 1)])
    db.commit()
    cursor.close()
    db.close()

def delete():
    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql = "DELETE FROM imooc_goddess WHERE user_name = %s"
    # executemany返回受影响的行数
    res = cursor.executemany(sql, ('小甜',))
    print("res = ", res)
    db.commit()
    cursor.close()
    db.close()

if __name__ == '__main__':
    insert2()
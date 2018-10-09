# coding:utf-8
# https://www.cnblogs.com/onemorepoint/p/8331555.html
from pymongo import MongoClient

if __name__ == '__main__':
    # 使用下面的代码片段，将建立连接到默认主机（localhost）和端口（27017）。
    client = MongoClient()
    # 指定主机和/或使用端口：
    # client = MongoClient('localhost', 27017)
    # 或者使用MongoURI格式：
    # client = MongoClient('mongodb://localhost:27017')

    # 一旦你有一个连接的MongoClient实例，你可以在Mongo服务器中访问任何数据库。如果要访问一个数据库，你可以当作属性一样访问：
    db = client.pymongo_test
    # 或者你也可以使用字典形式的访问：
    # db = client['pymongo_test']

    # 在数据库中存储数据，就如同调用只是两行代码一样容易。第一行指定你将使用哪个集合。在MongoDB中术语中，一个集合是在数据库中存储在一起的一组文档(相当于SQL的表)。集合和文档类似于SQL表和行。第二行是使用集合插入数据insert_one()的方法：
    posts = db.posts
    post_data = {
        'title': 'Python and MongoDB',
        'content': 'PyMongo is fun, you guys',
        'author': 'Scott'
    }
    result = posts.insert_one(post_data)
    print('One post: {0}'.format(result.inserted_id))

    # 我们甚至可以使用insert_one()同时插入很多文档，如果你有很多的文档添加到数据库中，可以使用方法insert_many()。此方法接受一个list参数：
    post_1 = {
        'title': 'Python and MongoDB',
        'content': 'PyMongo is fun, you guys',
        'author': 'Scott'
    }
    post_2 = {
        'title': 'Virtual Environments',
        'content': 'Use virtual environments, you guys',
        'author': 'Scott'
    }
    post_3 = {
        'title': 'Learning Python',
        'content': 'Learn Python, it is easy',
        'author': 'Bill'
    }
    new_result = posts.insert_many([post_1, post_2, post_3])
    print('Multiple posts: {0}'.format(new_result.inserted_ids))

    # 检索文档可以使用find_one()方法，比如要找到author为Bill的记录:
    bills_post = posts.find_one({'author': 'Bill'})
    print(bills_post)

    # 如果需要查询多条记录可以使用find()方法：
    scotts_posts = posts.find({'author': 'Scott'})
    print(scotts_posts)

    # 他的主要区别在于文档数据不是作为数组直接返回给我们。相反，我们得到一个游标对象的实例。这Cursor是一个包含相当多的辅助方法，以帮助您处理数据的迭代对象。要获得每个文档，只需遍历结果：
    for post in scotts_posts:
        print(post)
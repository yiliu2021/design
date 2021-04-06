import pymysql
db = pymysql.connect(host = 'localhost', user = 'root', password = 'lgx', port = 3306)
cursor = db.cursor()
cursor.execute('SELECT VERSION()')
data = cursor.fetchone()
# 打印版本
print(data)
cursor.execute("CREATE DATABASE IF NOT EXISTS face")
# 查看现有的库
cursor.execute("show databases")
print(cursor.fetchall())
cursor.close()
db.close()
face = pymysql.connect(host = 'localhost', user = 'root', password = 'lgx', port = 3306, db = 'face')
cur = face.cursor()
table_sql = 'CREATE TABLE IF NOT EXISTS users (user VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL, PRIMARY KEY (user))'
cur.execute(table_sql)
cur.execute('show tables')
print(cur.fetchall())

try:
    data = {'user': 'admin', 'password': 'admin'}
    table = 'users'
    keys = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))
    # 整合成sql语句
    insert_sql = 'INSERT INTO {table}({keys}) VALUES ({values}) '.format(table=table, keys=keys, values=values)
    print(insert_sql)
    if cur.execute(insert_sql, tuple(data.values())):
        print('successful')
        face.commit()
except:
    print("failed")
    face.rollback()
cur.execute('select * from users where user="admin";')
print(cur.fetchone())
face.close()
print ('*'*40)

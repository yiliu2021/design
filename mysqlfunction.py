
import pymysql


def Loaddata():
    db = pymysql.connect(host='localhost', user='root', password='lgx', port=3306)
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS face")
    cursor.close()
    db.close()
    face = pymysql.connect(host='localhost', user='root', password='lgx', port=3306, db='face')
    cur = face.cursor()
    usertable_sql = """CREATE TABLE IF NOT EXISTS users (
                    user VARCHAR(20) NOT NULL, 
                    password VARCHAR(20) NOT NULL, 
                    PRIMARY KEY (user))"""
    cur.execute(usertable_sql)
    insidertable_sql = """CREATE TABLE IF NOT EXISTS insiders (
                    number VARCHAR(30) NOT NULL, 
                    name VARCHAR(10) NOT NULL, 
                    sex VARCHAR(2) NOT NULL,
                    other VARCHAR(255),
                    PRIMARY KEY (number))"""
    cur.execute(insidertable_sql)
    externaltable_sql = """CREATE TABLE IF NOT EXISTS externals (
                        number VARCHAR(30) NOT NULL, 
                        name VARCHAR(10) NOT NULL, 
                        sex VARCHAR(2) NOT NULL,
                        other VARCHAR(255),
                        PRIMARY KEY (number))"""
    cur.execute(externaltable_sql)
    leavepstable_sql = """CREATE TABLE IF NOT EXISTS leaveps (
                        number VARCHAR(30) NOT NULL, 
                        name VARCHAR(10) NOT NULL, 
                        sex VARCHAR(2) NOT NULL,
                        other VARCHAR(255),
                        PRIMARY KEY (number))"""
    cur.execute(leavepstable_sql)
    visitorstable_sql = """CREATE TABLE IF NOT EXISTS visitors (
                            number VARCHAR(30) NOT NULL, 
                            name VARCHAR(10) NOT NULL, 
                            sex VARCHAR(2) NOT NULL,
                            other VARCHAR(255),
                            PRIMARY KEY (number))"""
    cur.execute(visitorstable_sql)
    checkintable_sql = """CREATE TABLE IF NOT EXISTS checkin (
                                number VARCHAR(30) NOT NULL, 
                                name VARCHAR(10) NOT NULL, 
                                sex VARCHAR(2) NOT NULL,
                                date VARCHAR(20) NOT NULL,
                                time VARCHAR(20) NOT NULL,
                                other VARCHAR(255),
                                PRIMARY KEY (number))"""
    cur.execute(checkintable_sql)
    comeintable_sql = """CREATE TABLE IF NOT EXISTS comein (
                                    number VARCHAR(30) NOT NULL, 
                                    name VARCHAR(10) NOT NULL, 
                                    sex VARCHAR(2) NOT NULL,
                                    date VARCHAR(20) NOT NULL,
                                    time VARCHAR(20) NOT NULL,
                                    other VARCHAR(255),
                                    PRIMARY KEY (number))"""
    cur.execute(comeintable_sql)
    goouttable_sql = """CREATE TABLE IF NOT EXISTS goout (
                                        number VARCHAR(30) NOT NULL, 
                                        name VARCHAR(10) NOT NULL, 
                                        sex VARCHAR(2) NOT NULL,
                                        date VARCHAR(20) NOT NULL,
                                        time VARCHAR(20) NOT NULL,
                                        other VARCHAR(255),
                                        PRIMARY KEY (number))"""
    cur.execute(goouttable_sql)
    try:
        data = {'user': 'admin', 'password': 'admin'}
        table = 'users'
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        # 整合成sql语句
        insert_sql = 'INSERT INTO {table}({keys}) VALUES ({values}) '.format(table=table, keys=keys, values=values)
        if cur.execute(insert_sql, tuple(data.values())):
            face.commit()
    except:
        face.rollback()
    face.close()

if __name__ == '__main__':
    Loaddata()

#cursor.execute('SELECT VERSION()')
#data = cursor.fetchone()
# 打印版本
#print(data)
# 查看现有的库
#cursor.execute("show databases")
#cur.execute('show tables')
#print(cur.fetchall())
#cur.execute('select * from users where user="admin";')
#print(cur.fetchone())
#sql = "SELECT * FROM EMPLOYEE WHERE INCOME > '%d'" % (1000)
print ('*'*40)

import pymysql
from datetime import datetime, timedelta

def connectsql():
    face = pymysql.connect(host='localhost', user='root', password='lgx', port=3306, db='face')
    cur = face.cursor()
    return(face,cur)
def closesql(face,cur):
    cur.close()
    face.close()
def del_logs(table):
    face, cur = connectsql()
    now_time = datetime.now()
    cut_time = now_time - timedelta(days=30)
    c_time = cut_time.strftime("%Y-%m-%d %H:%M:%S")
    start_time = now_time - timedelta(days=60)
    s_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
    sql = "DELETE FROM {table} where DATE_FORMAT(datetime,'%Y-%m-%d %H:%i:%s') BETWEEN'{a}'and'{b}'".format(
        table=table, a=s_time, b=c_time)
    num = cur.execute(sql)
    closesql(face, cur)
    return num
def Loaddata():
    db = pymysql.connect(host='localhost', user='root', password='lgx', port=3306)
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS face")
    cursor.close()
    db.close()
    face, cur=connectsql()
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
    visitorstable_sql = """CREATE TABLE IF NOT EXISTS visitors (
                            number VARCHAR(30) NOT NULL, 
                            name VARCHAR(10) NOT NULL, 
                            sex VARCHAR(2) NOT NULL,
                            datetime VARCHAR(20) NOT NULL,
                            other VARCHAR(255),
                            PRIMARY KEY (number))"""
    cur.execute(visitorstable_sql)
    checkintable_sql = """CREATE TABLE IF NOT EXISTS checkin (
                                number VARCHAR(30) NOT NULL, 
                                name VARCHAR(10) NOT NULL, 
                                datetime VARCHAR(20),
                                other VARCHAR(255))"""
    cur.execute(checkintable_sql)
    comeintable_sql = """CREATE TABLE IF NOT EXISTS comein (
                                    number VARCHAR(30) NOT NULL, 
                                    name VARCHAR(10) NOT NULL, 
                                    datetime VARCHAR(20),
                                    other VARCHAR(255))"""
    cur.execute(comeintable_sql)
    gooutpersontable_sql = """CREATE TABLE IF NOT EXISTS gooutperson (
                                            number VARCHAR(30) NOT NULL, 
                                            name VARCHAR(10) NOT NULL, 
                                            sex VARCHAR(2) NOT NULL,
                                            datetime VARCHAR(20) NOT NULL,
                                            other VARCHAR(255),
                                            PRIMARY KEY (number))"""
    cur.execute(gooutpersontable_sql)
    goouttable_sql = """CREATE TABLE IF NOT EXISTS goout (
                                        number VARCHAR(30) NOT NULL, 
                                        name VARCHAR(10) NOT NULL, 
                                        datetime VARCHAR(20),
                                        other VARCHAR(255))"""
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
    a = del_logs('checkin')
    b = del_logs('comein')
    c = del_logs('goout')
    closesql(face, cur)
def whether_or_not(table,key,value):
    face, cur = connectsql()
    sel_sql = "select count(*) from %s where %s = '%s'" % (table,key,value)
    cur.execute(sel_sql)
    count = cur.fetchone()
    closesql(face, cur)
    return count[0]
def exsit_or_not(table,value):
    face, cur = connectsql()
    sel_sql = "select datetime from %s where number = '%s'" %(table, value)
    cur.execute(sel_sql)
    exsit = cur.fetchone()
    closesql(face, cur)
    currenttime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    now_time = datetime.strptime(currenttime, '%Y-%m-%d %H:%M:%S')
    if exsit == None:
        return False
    else:
        try:
            person_time = datetime.strptime(exsit[0], '%Y-%m-%d %H:%M:%S')
            flag = person_time-now_time
            if flag.days >= 0:
                return True
            else:
                return False
        except:
            return False
def select_table_section(table,start_time,end_time):
    face, cur = connectsql()
    sql = "select * from {table} where DATE_FORMAT(datetime,'%Y-%m-%d %H:%i:%s') BETWEEN'{a}'and'{b}'".format(
        table=table, a=start_time, b=end_time)
    cur.execute(sql)
    nead_table = cur.fetchall()
    logs=len(nead_table)
    closesql(face, cur)
    return nead_table, logs

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

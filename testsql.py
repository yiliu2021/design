from mysqlload import *
from datetime import datetime, timedelta
face ,cur = connectsql()
cur.execute('SELECT VERSION()')
data = cur.fetchone()
# 打印版本
print(data)
now_time = datetime.now()
end_time = now_time + timedelta(days=30)
a=now_time.strftime("%Y%m%d %H:%M:%S")
c = datetime.strptime(a, '%Y%m%d %H:%M:%S')
b=end_time.strftime("%Y%m%d %H:%M:%S")
d= datetime.strptime(b, '%Y%m%d %H:%M:%S')
print(a)
print(b)
print(d)
sql = "select * from gooutperson where DATE_FORMAT(datetime,'%Y%m%d %H:%i:%s') BETWEEN'{a}'and'{b}'" .format(a=a,b=b)
print(sql)
cur.execute(sql)
c= cur.fetchall()
print(c)


sql = "select * from gooutperson where DATE_FORMAT(datetime,'%Y%m%d') = '20210416'"
cur.execute(sql)
a= cur.fetchone()
print(a)

sql = "select * from gooutperson where DATE_FORMAT(datetime,'%Y%m%d %H:%i:%s') BETWEEN '20210412 21:00:00' and  '20210416 22:00:00'"
cur.execute(sql)
a= cur.fetchall()
print(a)

#一行一行打
sql = "select * from users"
cur.execute(sql)
while True:
    row = cur.fetchone()
    if not row:
        break
    print('现在表格内容：',row)
#改hh的密码
a='aa'
b='hh'
sql="update users set password='%s' where user='%s'"%(a,b)
print(sql)
update=cur.execute(sql)
print('修改行数：',update)
face.commit()
cur.close()
face.close()


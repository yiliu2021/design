import pymysql
face = pymysql.connect(host='localhost', user='root', password='lgx', port=3306, db='face')
cur = face.cursor()
# 打整个表
sql = "select * from users"
cur.execute(sql)
suppass = cur.fetchall()
print('现在表格内容：',suppass)
#插一行
sql="INSERT INTO users VALUES ('ll','ll')"
print('插入一行',sql)
cur.execute(sql)
#打一行
sql = "select password from users where user='admin'"
cur.execute(sql)
sqlpassword = cur.fetchone()
print('表格第一行内容：',sqlpassword)
#查某个值
user_name='ll'
sel_sql="select count(*) from users where user = '%s'"%(user_name)
cur.execute(sel_sql)
count=cur.fetchone()
print('ll的内容行数：',count[0])
if count[0]==1:
    print('count[0]是整数1')
#一行一行打
sql = "select * from users"
cur.execute(sql)
while True:
    row = cur.fetchone()
    if not row:
        break
    print('现在表格内容：',row)
#删一行
user_name='ll'
del_sql="DELETE FROM {table} WHERE user='{condition}'".format(table = 'users', condition = user_name)
print(del_sql)
cur.execute(del_sql)
print('sha')
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
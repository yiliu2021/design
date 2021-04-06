import pymysql
face = pymysql.connect(host='localhost', user='root', password='lgx', port=3306, db='face')
cur = face.cursor()
a='a'
sql = "select password from users where user='%s'"%(a)
cur.execute(sql)
data = cur.fetchone()
print(data)
if(data==None):
    print('no')

b='admin'
#if(data[0]==b):
    #print('ok')
#else:
    #print('no')
face.close()

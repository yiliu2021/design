import pymysql
db = pymysql.connect(host = 'localhost', user = 'root', password = 'lgx', port = 3306, db = 'face')
cursor = db.cursor()
cursor.execute('SELECT VERSION()')
data = cursor.fetchone()
# 打印版本
print(data)
# 整合成sql语句
sql = "insert into users values ('admin', 'admin');"
print(sql)
cursor.execute(sql)
db.commit()
print('successful')
db.close()


import pymysql

#打开数据库连接
db = pymysql.connect("localhost", "root", "123", "quanluo")

#使用cursor（）方法获取游标
cursor = db.cursor()
#查询数据 数据表quan 中年龄大于10的数据
sql = "SELECT * FROM quan WHERE age > '%d'" % (10)
try:
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        fname = row[0]
        lname = row[1]
        age = row[2]
        sex = row[3]
        #输出查询结果
        print("fname=%s, lname=%s, age=%d, sex=%c" % (fname, lname, age, sex))
except:
    print("Error: unable to fecth data")
#关闭数据库
db.close()

sql="""CREATE TABLE IF NOT EXISTS `user` (
	  `id` int(11) NOT NULL AUTO_INCREMENT,
	  `name` varchar(255) NOT NULL,
	  `age` int(11) NOT NULL,
	  PRIMARY KEY (`id`)
	) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0"""
        #self.ui.editin.toggled.connect(lambda: self.btnstate(self.ui.editin))
        #self.ui.editout.toggled.connect(lambda: self.btnstate(self.ui.editout))
        self.ui.commit.clicked.connect(self.radiostate)
    def radiostate(self):
        print(self.ui.editin.isChecked())
        print(self.ui.editout.isChecked())

    def btnstate(self, btn):
        # 输出按钮1与按钮2的状态，选中还是没选中
        if btn.isChecked() == True:
            a='被选中'
        else:
            a='未选中'
        print(btn.text()+a)
        QMessageBox.warning(self,
                            "警告",
                            "用户名和密码不得为空！",
                            QMessageBox.Yes)
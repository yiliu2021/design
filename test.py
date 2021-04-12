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
    #self.ui.editin.toggled.connect(lambda: self.btnstate(self.ui.editin))
    #self.ui.editout.toggled.connect(lambda: self.btnstate(self.ui.editout))
        QMessageBox.warning(self,
                            "警告",
                            "用户名和密码不得为空！",
                            QMessageBox.Yes)
now = datetime.now().strftime("%Y%m%d %H:%M:%S")#系统时间转字符串
print(now)
c = datetime.strptime(now, '%Y%m%d %H:%M:%S')#字符串转可用于运算时间
print(c)
a = self.ui.dateTimeEdit.dateTime().toString("yyyy-MM-dd hh:mm:ss")#控件时间转字符串
d = datetime.strptime(a, '%Y-%m-%d %H:%M:%S')
print(a)
print(d)
e=d-c#时间运算
print(e.days)
print(e.seconds)
self.ui.name_3.setText(a)
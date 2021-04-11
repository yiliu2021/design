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

        #self.ui.editin.toggled.connect(lambda: self.btnstate(self.ui.editin))
        #self.ui.editout.toggled.connect(lambda: self.btnstate(self.ui.editout))

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
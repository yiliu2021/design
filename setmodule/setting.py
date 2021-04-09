from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pymysql
import sys
global logoinuser
#设置模块在独立于主程序的文件夹，为确保主程序引入不出错误，独立模块文件夹内相互引用宜加上文件夹名称
from setmodule.setting_ui import Ui_userset
import sys
sys.path.append('../')
from warnning import Ui_warn
from mysqlload import *

class set_mod(QWidget):
    def __init__(self):
        super().__init__()
        self.ui=Ui_userset()
        self.ui.setupUi(self)
        #self.setWindowFlags(Qt.WindowStaysOnTopHint)
        global logoinuser
        logoinuser=''
        self.ui.addmanager.clicked.connect(self.add_manager)
        self.ui.delmanager_2.clicked.connect(self.del_manager)
        self.ui.query.clicked.connect(self.edit_password)


    def deal_emit_slot(self, name):
        _translate = QtCore.QCoreApplication.translate
        global logoinuser
        logoinuser=name
        # 如从登录界面启动此处可接收logoin发送的信号，可以执行下一条程序，即可跳转设置模块
        # self.show()
        if logoinuser=='admin':
            self.ui.welcome.setText(_translate("userset","<html><head/><body><p align=\"center\">" + logoinuser + "，你好！</p></body></html>"))
            try:
                self.show_user()
            except:
                self.warn = Ui_warn('数据加载失败！')
                self.warn.setWindowModality(Qt.ApplicationModal)
                self.warn.show()
        else:
            self.ui.welcome.setText(_translate("userset","<html><head/><body><p align=\"center\">" + logoinuser + "，你好！</p></body></html>"))
            self.ui.tableWidget_3.setRowCount(0)
            self.ui.adduser.setEnabled(False)
            self.ui.label_12.setText(_translate("userset", "<html><head/><body><p align=\"center\">账户编辑需管理员权限！</p></body></html>"))

        #如从登录界面启动此处可接收logoin发送的信号，可以执行下一条程序，即可跳转设置模块
        #self.show()
    def show_user(self):
        _translate = QtCore.QCoreApplication.translate
        self.ui.adduser.setEnabled(True)
        face,cur=connectsql()
        sql = "select user from users"
        cur.execute(sql)
        #返回表格所有数据
        suppass = cur.fetchall()
        user_rows=len(suppass)
        self.ui.tableWidget_3.setRowCount(user_rows)
        for i in range(user_rows):
            item = QtWidgets.QTableWidgetItem()
            self.ui.tableWidget_3.setVerticalHeaderItem(i, item)
            item = self.ui.tableWidget_3.verticalHeaderItem(i)
            item.setText(_translate("userset", str(i+1)))
        # 遍历二维元组, 将user显示到界面表格上
        x = 0
        for i in suppass:
            y = 0
            for j in i:
                self.ui.tableWidget_3.setItem(x, y, QtWidgets.QTableWidgetItem(str(suppass[x][y])))
                y = y + 1
            x = x + 1
        closesql(face, cur)
    def add_manager(self):
        ad_pass = self.ui.adminpass.text()
        user_name = self.ui.manageuser.text()
        user_pass = self.ui.userpass.text()
        user_pass2 = self.ui.userpass_2.text()
        face,cur = connectsql()
        sql = "select password from users where user='admin'"
        cur.execute(sql)
        suppass = cur.fetchone()
        if ad_pass=='' or user_name==''or user_pass==''or user_pass2=='':
            self.warn = Ui_warn('无效信息！')
            self.warn.setWindowModality(Qt.ApplicationModal)
            self.warn.show()
        elif user_pass==user_pass2 and user_name !='admin' and ad_pass == suppass[0]:
            try:
                insert_sql = "insert into users values ('%s','%s')"%(user_name,user_pass)
                if cur.execute(insert_sql):
                    face.commit()
                    self.ui.tableWidget_3.setRowCount(0)
                    self.show_user()
                    self.warn = Ui_warn('用户添加成功！')
                    self.warn.setWindowModality(Qt.ApplicationModal)
                    self.warn.show()
            except:
                face.rollback()
                self.warn = Ui_warn('用户添加失败！\n请确认用户是否存在！\n请检查数据连接！')
                self.warn.setWindowModality(Qt.ApplicationModal)
                self.warn.show()
        else:
            self.warn = Ui_warn('信息输入错误！')
            self.warn.setWindowModality(Qt.ApplicationModal)
            self.warn.show()
        closesql(face, cur)
        self.ui.adminpass.clear()
        self.ui.manageuser.clear()
        self.ui.userpass.clear()
        self.ui.userpass_2.clear()
    def del_manager(self):
        ad_pass = self.ui.adminpass.text()
        user_name = self.ui.manageuser.text()
        if ad_pass=='' or user_name=='':
            self.warn = Ui_warn('无效信息！')
            self.warn.setWindowModality(Qt.ApplicationModal)
            self.warn.show()
        else:
            face, cur = connectsql()
            sql = "select password from users where user='admin'"
            cur.execute(sql)
            suppass = cur.fetchone()
            sel_sql="select count(*) from users where user = '%s'"%(user_name)
            cur.execute(sel_sql)
            count=cur.fetchone()
            if ad_pass == suppass[0] and count[0]==1:
                try:
                    del_sql="DELETE FROM {table} WHERE user='{condition}'".format(table = 'users', condition = user_name)
                    if cur.execute(del_sql):
                        face.commit()
                        self.ui.tableWidget_3.setRowCount(0)
                        self.show_user()
                        self.warn = Ui_warn('用户删除成功！')
                        self.warn.setWindowModality(Qt.ApplicationModal)
                        self.warn.show()
                except:
                    face.rollback()
                    self.warn = Ui_warn('用户删除失败！\n请检查数据连接！')
                    self.warn.setWindowModality(Qt.ApplicationModal)
                    self.warn.show()
            else:
                self.warn = Ui_warn('管理员密码错误!\n或用户不存在！')
                self.warn.setWindowModality(Qt.ApplicationModal)
                self.warn.show()
            closesql(face, cur)
        self.ui.adminpass.clear()
        self.ui.manageuser.clear()
        self.ui.userpass.clear()
        self.ui.userpass_2.clear()
    def edit_password(self):
        old_pass = self.ui.passold.text()
        new_pass = self.ui.newpass.text()
        new_passagain = self.ui.newpass_2.text()
        global logoinuser
        face, cur = connectsql()
        sql = "select password from users where user='%s'"%(logoinuser)
        cur.execute(sql)
        user_pass = cur.fetchone()
        if old_pass=='' or new_pass==''or new_passagain=='':
            self.warn = Ui_warn('无效信息！')
            self.warn.setWindowModality(Qt.ApplicationModal)
            self.warn.show()
        elif new_pass==new_passagain and user_pass[0]==old_pass:
            try:
                edit_sql="update users set password='%s' where user='%s'"%(new_pass,logoinuser)
                if cur.execute(edit_sql):
                    face.commit()
                    self.warn = Ui_warn('密码修改成功！')
                    self.warn.setWindowModality(Qt.ApplicationModal)
                    self.warn.show()
            except:
                face.rollback()
                self.warn = Ui_warn('密码修改失败！')
                self.warn.setWindowModality(Qt.ApplicationModal)
                self.warn.show()
        else:
            self.warn = Ui_warn('重新输入密码！\n新密码两次输入要求一致')
            self.warn.setWindowModality(Qt.ApplicationModal)
            self.warn.show()
        closesql(face, cur)
        self.ui.passold.clear()
        self.ui.newpass.clear()
        self.ui.newpass_2.clear()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    test_import = set_mod()
    test_import.show()  # 最大化显示
    sys.exit(app.exec_())
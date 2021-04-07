from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
global logoinuser
#设置模块在独立于主程序的文件夹，为确保主程序引入不出错误，独立模块文件夹内相互引用宜加上文件夹名称
from setmodule.setting_ui import Ui_userset

class set_mod(QWidget):
    def __init__(self):
        super().__init__()
        self.ui=Ui_userset()
        self.ui.setupUi(self)
        #self.setWindowFlags(Qt.WindowStaysOnTopHint)
        global logoinuser
        logoinuser=''
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

    def deal_emit_slot(self, name):
        global logoinuser
        logoinuser=name
        self.ui.welcome.setText(QtCore.QCoreApplication.translate("userset","<html><head/><body><p align=\"center\">" + logoinuser + "，你好！</p></body></html>"))
        #如从登录界面启动此处可接收logoin发送的信号，可以执行下一条程序，即可跳转设置模块
        #self.show()
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    test_import = set_mod()
    test_import.show()  # 最大化显示
    sys.exit(app.exec_())
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import qtawesome

class Ui_warn(QWidget):
    def __init__(self,message='数据加载失败！'):
        super().__init__()
        self.setupUi(self)
        self.retranslateUi(self)
        #弹出传递参数内容
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("warn", message))
        #设置窗口置顶
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.setWindowOpacity(0.9)  # 设置窗口透明度
        #self.setAttribute(QtCore.Qt.WA_TranslucentBackground) # 设置窗口背景透明
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        pe = QPalette()
        self.setAutoFillBackground(True)
        pe.setColor(QPalette.Window, Qt.darkCyan)  # 设置背景色
        self.setPalette(pe)



    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def mousePressEvent(self, event):
        self.close()

    def setupUi(self, warn):
        warn.setObjectName("warn")
        warn.resize(300, 150)
        self.label = QtWidgets.QLabel(warn)
        self.label.setGeometry(QtCore.QRect(30, 30, 240, 90))
        self.label.setStyleSheet("background-color:rgba(0,0,0,0);border-color:rgba(0,0,0,255);color: rgba(0, 0, 0,254);border-style:none;border-width:0px;border-radius:8px;font:20px \"华文中宋\";font-style:normal;font-weight: lighter;text-decoration:blink;")
        self.label.setObjectName("label")

        spin_icon = qtawesome.icon('fa5s.exclamation-circle', color='black')
        warn.setWindowIcon(spin_icon)

        self.retranslateUi(warn)
        QtCore.QMetaObject.connectSlotsByName(warn)

    def retranslateUi(self, warn):
        _translate = QtCore.QCoreApplication.translate
        warn.setWindowTitle(_translate("warn", "提示框"))
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_warn('你好啊！')
    ui.show()
    sys.exit(app.exec_())
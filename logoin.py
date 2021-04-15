from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from setmodule.setting import set_mod
from warnning import Ui_warn
from mysqlload import *
import qtawesome


class Ui_logoin(QWidget):
    Signal_parp = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.retranslateUi(self)


    @pyqtSlot()
    def on_yes_clicked(self):
        recusername = self.lineEdit.text()
        recpassword = self.lineEdit_2.text()
        if (recusername == '') or (recpassword == ''):
            self.warn = Ui_warn('用户名和密码不得为空！')
            self.warn.setWindowModality(Qt.ApplicationModal)
            self.warn.show()
        else:
            try:
                face,cur = connectsql()
                sql = "select password from users where user='%s'"%(recusername)
                cur.execute(sql)
                sqlpassword = cur.fetchone()
                closesql(face, cur)
                if sqlpassword==None:
                    self.warn = Ui_warn('用户不存在！')
                    self.warn.setWindowModality(Qt.ApplicationModal)
                    self.warn.show()
                elif sqlpassword[0]==recpassword:
                    data_str = recusername
                    self.Signal_parp.emit(data_str)
                    self.close()
                else:
                    self.warn = Ui_warn('密码错误！')
                    self.warn.setWindowModality(Qt.ApplicationModal)
                    self.warn.show()
            except:
                self.warn = Ui_warn('数据连接失败，请设置数据库！')
                self.warn.setWindowModality(Qt.ApplicationModal)
                self.warn.show()
            self.lineEdit.clear()
            self.lineEdit_2.clear()


    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def setupUi(self, logoin):
        logoin.setObjectName("logoin")
        logoin.resize(320, 214)
        self.gridLayout = QtWidgets.QGridLayout(logoin)

        spin_icon = qtawesome.icon('fa5s.angle-double-right', color='black')
        logoin.setWindowIcon(spin_icon)

        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.title = QtWidgets.QLabel(logoin)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title.sizePolicy().hasHeightForWidth())
        self.title.setSizePolicy(sizePolicy)
        self.title.setMinimumSize(QtCore.QSize(300, 60))
        self.title.setMaximumSize(QtCore.QSize(300, 70))
        self.title.setFocusPolicy(QtCore.Qt.NoFocus)
        self.title.setStyleSheet("background-color:rgba(0,0,0,0);border-color:rgba(0,0,0,255);color: rgba(0, 0, 0,255);border-style:none;border-width:1px;border-radius:0px;font:29px \"方正小标宋简体\";font-style:normal;font-weight: normal;text-decoration:blink;")
        self.title.setObjectName("title")
        self.verticalLayout.addWidget(self.title)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.count = QtWidgets.QLabel(logoin)
        self.count.setMinimumSize(QtCore.QSize(60, 30))
        self.count.setStyleSheet("background-color:rgba(0,0,0,0);border-color:rgba(0,0,0,255);color: rgba(0, 0, 0,255);border-style:none;border-width:1px;border-radius:0px;font:20px \"黑体\";font-style:normal;font-weight: normal;text-decoration:blink;")
        self.count.setObjectName("count")
        self.horizontalLayout_2.addWidget(self.count)
        self.lineEdit = QtWidgets.QLineEdit(logoin)
        self.lineEdit.setStyleSheet("background-color:rgba(0,0,0,11);border-color:rgba(0,0,0,255);color: rgba(0, 0, 0,255);border-style:solid;border-width:1px;border-radius:7px;font:18px \"Times New Roman\";")
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.words = QtWidgets.QLabel(logoin)
        self.words.setMinimumSize(QtCore.QSize(60, 50))
        self.words.setStyleSheet("background-color:rgba(0,0,0,0);border-color:rgba(0,0,0,255);color: rgba(0, 0, 0,255);border-style:none;border-width:1px;border-radius:0px;font:20px \"黑体\";font-style:normal;font-weight: normal;text-decoration:blink;")
        self.words.setObjectName("words")
        self.horizontalLayout.addWidget(self.words)
        self.lineEdit_2 = QtWidgets.QLineEdit(logoin)
        self.lineEdit_2.setStyleSheet("background-color:rgba(0,0,0,11);border-color:rgba(0,0,0,255);color: rgba(0, 0, 0,255);border-style:solid;border-width:1px;border-radius:7px;font:18px \"Times New Roman\";")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout.addWidget(self.lineEdit_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.yes = QtWidgets.QPushButton(logoin)
        self.yes.setMinimumSize(QtCore.QSize(50, 30))
        self.yes.setMaximumSize(QtCore.QSize(80, 30))
        self.yes.setStyleSheet("")
        self.yes.setObjectName("yes")
        self.horizontalLayout_3.addWidget(self.yes)
        self.quit = QtWidgets.QPushButton(logoin)
        self.quit.setMinimumSize(QtCore.QSize(80, 30))
        self.quit.setMaximumSize(QtCore.QSize(80, 30))
        self.quit.setStyleSheet("")
        self.quit.setAutoRepeatDelay(300)
        self.quit.setObjectName("quit")
        self.horizontalLayout_3.addWidget(self.quit)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        logoin.setWindowOpacity(0.9)  # 设置窗口透明度
        # logoin.setAttribute(QtCore.Qt.WA_TranslucentBackground) # 设置窗口背景透明
        logoin.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        pe = QPalette()
        logoin.setAutoFillBackground(True)
        pe.setColor(QPalette.Window, Qt.lightGray)  # 设置背景色
        logoin.setPalette(pe)

        self.retranslateUi(logoin)
        self.quit.clicked.connect(logoin.close)
        QtCore.QMetaObject.connectSlotsByName(logoin)

    def retranslateUi(self, logoin):
        _translate = QtCore.QCoreApplication.translate
        logoin.setWindowTitle(_translate("logoin", "登录"))
        self.title.setText(_translate("logoin", "<html><head/><body><p align=\"center\">信息管理系统登录</p></body></html>"))
        self.count.setText(_translate("logoin", "用户名："))
        self.lineEdit.setPlaceholderText(_translate("logoin", "输入用户名"))
        self.lineEdit_2.setPlaceholderText(_translate("logoin", "输入密码"))
        self.words.setText(_translate("logoin", "密  码："))
        self.yes.setText(_translate("logoin", "确定"))
        self.quit.setText(_translate("logoin", "退出"))
        self.quit.setShortcut(_translate("logoin", "Ctrl+R"))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_logoin()
    myset = set_mod()
    ui.show()
    ui.Signal_parp.connect(myset.deal_emit_slot)
    sys.exit(app.exec_())
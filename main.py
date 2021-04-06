from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import qtawesome
from mysqlfunction import *

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(600, 400)
        self.label_time = QtWidgets.QLabel(Form)
        self.label_time.setGeometry(QtCore.QRect(20, 360, 230, 30))
        self.label_time.setText("")
        self.label_time.setObjectName("label_time")
        #设置关闭按钮
        self.close = QtWidgets.QPushButton(Form)
        self.close.setText("")
        self.close.setObjectName("close")
        close_icon = qtawesome.icon('fa5s.power-off', color='white')
        self.close.setIcon(close_icon)  # 设置图标
        self.close.setIconSize(QtCore.QSize(35, 35))
        self.close.setGeometry(QtCore.QRect(550, 10, 40, 40))  # 依次对应x、y坐标，按钮长宽
        self.close.setStyleSheet('''QPushButton{border:none;}
                                QPushButton:hover{color:white;
                                            border:0px solid #F3F3F5;
                                            border-radius:5px;
                                            background:red;}''')
        # border-radius不是设置半径，设置圆角大小，最大值是图标长宽其中较小的边长的一半。
        #设置最小化按钮
        self.min = QtWidgets.QPushButton(Form)
        self.min.setText("")
        self.min.setObjectName("min")
        min_icon = qtawesome.icon('fa5s.minus-circle', color='white')
        self.min.setIcon(min_icon)  # 设置图标
        self.min.setIconSize(QtCore.QSize(40, 40))
        self.min.setGeometry(QtCore.QRect(510, 10, 40, 40))  # 依次对应x、y坐标，按钮长宽
        self.min.setStyleSheet('''QPushButton{border:none;}
                                        QPushButton:hover{color:white;
                                                    border:0px solid #F3F3F5;
                                                    border-radius:5px;
                                                    background:darkGray;}''')
        #设置图标
        self.set = QtWidgets.QPushButton(Form)
        self.set.setGeometry(QtCore.QRect(70, 70, 100, 100))
        self.set.setText("")
        self.set.setObjectName("set")
        set_icon = qtawesome.icon('fa5s.cog', color='white')
        self.set.setIcon(set_icon)  # 设置图标
        self.set.setIconSize(QtCore.QSize(95, 95))
        self.set.setStyleSheet('''QPushButton{border:none;}
                                                QPushButton:hover{color:white;
                                                            border:0px solid #F3F3F5;
                                                            border-radius:5px;
                                                            background:darkGray;}''')

        self.set_2 = QtWidgets.QLabel(Form)
        self.set_2.setGeometry(QtCore.QRect(78, 180, 80, 20))
        self.set_2.setStyleSheet("background-color:rgba(0,0,0,0);border-color:rgba(0,0,0,0);color: rgba(0, 0, 0,255);border-style:none;border-width:1px;border-radius:0px;font:20px \"黑体\";font-style:normal;font-weight: normal;text-decoration:blink;")
        self.set_2.setObjectName("set_2")
        #考勤图标
        self.checkingin = QtWidgets.QPushButton(Form)
        self.checkingin.setGeometry(QtCore.QRect(240, 70, 100, 100))
        self.checkingin.setText("")
        self.checkingin.setAutoRepeatInterval(100)
        self.checkingin.setObjectName("checkingin")
        checkingin_icon = qtawesome.icon('fa5s.user-edit', color='white')
        self.checkingin.setIcon(checkingin_icon)  # 设置图标
        self.checkingin.setIconSize(QtCore.QSize(95, 95))
        self.checkingin.setStyleSheet('''QPushButton{border:none;}
                                                        QPushButton:hover{color:white;
                                                                    border:0px solid #F3F3F5;
                                                                    border-radius:5px;
                                                                    background:darkGray;}''')

        self.checkingin_2 = QtWidgets.QLabel(Form)
        self.checkingin_2.setGeometry(QtCore.QRect(270, 180, 40, 20))
        self.checkingin_2.setStyleSheet("background-color:rgba(0,0,0,0);border-color:rgba(0,0,0,0);color: rgba(0, 0, 0,255);border-style:none;border-width:1px;border-radius:0px;font:20px \"黑体\";font-style:normal;font-weight: normal;text-decoration:blink;")
        self.checkingin_2.setObjectName("checkingin_2")
        #门禁图标
        self.entrance = QtWidgets.QPushButton(Form)
        self.entrance.setGeometry(QtCore.QRect(410, 70, 100, 100))
        self.entrance.setText("")
        self.entrance.setObjectName("entrance")
        entrance_icon = qtawesome.icon('fa5s.user-circle', color='white')
        self.entrance.setIcon(entrance_icon)  # 设置图标
        self.entrance.setIconSize(QtCore.QSize(95, 95))
        self.entrance.setStyleSheet('''QPushButton{border:none;}
                                                        QPushButton:hover{color:white;
                                                                    border:0px solid #F3F3F5;
                                                                    border-radius:5px;
                                                                    background:darkGray;}''')

        self.entrance_2 = QtWidgets.QLabel(Form)
        self.entrance_2.setGeometry(QtCore.QRect(420, 140, 100, 100))
        self.entrance_2.setStyleSheet("background-color:rgba(0,0,0,0);border-color:rgba(0,0,0,0);color: rgba(0, 0, 0,255);border-style:none;border-width:1px;border-radius:0px;font:20px \"黑体\";font-style:normal;font-weight: normal;text-decoration:blink;")
        self.entrance_2.setObjectName("entrance_2")
        #外出图标
        self.goout = QtWidgets.QPushButton(Form)
        self.goout.setGeometry(QtCore.QRect(70, 220, 100, 100))
        self.goout.setText("")
        self.goout.setObjectName("goout")
        goout_icon = qtawesome.icon('fa5s.paper-plane', color='white')
        self.goout.setIcon(goout_icon)  # 设置图标
        self.goout.setIconSize(QtCore.QSize(95, 95))
        self.goout.setStyleSheet('''QPushButton{border:none;}
                                                        QPushButton:hover{color:white;
                                                                    border:0px solid #F3F3F5;
                                                                    border-radius:5px;
                                                                    background:darkGray;}''')

        self.goout_2 = QtWidgets.QLabel(Form)
        self.goout_2.setGeometry(QtCore.QRect(78, 330, 80, 20))
        self.goout_2.setStyleSheet("background-color:rgba(0,0,0,0);border-color:rgba(0,0,0,0);color: rgba(0, 0, 0,255);border-style:none;border-width:1px;border-radius:0px;font:20px \"黑体\";font-style:normal;font-weight: normal;text-decoration:blink;")
        self.goout_2.setObjectName("goout_2")
        #来访图标
        self.visit = QtWidgets.QPushButton(Form)
        self.visit.setGeometry(QtCore.QRect(240, 220, 100, 100))
        self.visit.setText("")
        self.visit.setObjectName("visit")
        visit_icon = qtawesome.icon('fa5s.coffee', color='white')
        self.visit.setIcon(visit_icon)  # 设置图标
        self.visit.setIconSize(QtCore.QSize(95, 95))
        self.visit.setStyleSheet('''QPushButton{border:none;}
                                                        QPushButton:hover{color:white;
                                                                    border:0px solid #F3F3F5;
                                                                    border-radius:5px;
                                                                    background:darkGray;}''')

        self.visit_2 = QtWidgets.QLabel(Form)
        self.visit_2.setGeometry(QtCore.QRect(250, 330, 80, 20))
        self.visit_2.setStyleSheet("background-color:rgba(0,0,0,0);border-color:rgba(0,0,0,0);color: rgba(0, 0, 0,255);border-style:none;border-width:1px;border-radius:0px;font:20px \"黑体\";font-style:normal;font-weight: normal;text-decoration:blink;")
        self.visit_2.setObjectName("visit_2")
        #查询图标
        self.select = QtWidgets.QPushButton(Form)
        self.select.setGeometry(QtCore.QRect(410, 220, 100, 100))
        self.select.setText("")
        self.select.setObjectName("select")
        select_icon = qtawesome.icon('fa5s.search', color='white')
        self.select.setIcon(select_icon)  # 设置图标
        self.select.setIconSize(QtCore.QSize(95, 95))
        self.select.setStyleSheet('''QPushButton{border:none;}
                                                        QPushButton:hover{color:white;
                                                                    border:0px solid #F3F3F5;
                                                                    border-radius:5px;
                                                                    background:darkGray;}''')

        self.select_2 = QtWidgets.QLabel(Form)
        self.select_2.setGeometry(QtCore.QRect(440, 330, 40, 20))
        self.select_2.setStyleSheet("background-color:rgba(0,0,0,0);border-color:rgba(0,0,0,0);color: rgba(0, 0, 0,255);border-style:none;border-width:1px;border-radius:0px;font:20px \"黑体\";font-style:normal;font-weight: normal;text-decoration:blink;")
        self.select_2.setObjectName("select_2")

        Form.setWindowOpacity(0.9)  # 设置窗口透明度
        # Form.setAttribute(QtCore.Qt.WA_TranslucentBackground) # 设置窗口背景透明
        Form.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        pe = QPalette()
        Form.setAutoFillBackground(True)
        pe.setColor(QPalette.Window, Qt.lightGray)  # 设置背景色
        Form.setPalette(pe)

        spin_icon = qtawesome.icon('fa5s.clone', color='black')
        Form.setWindowIcon(spin_icon)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "智慧营区"))
        self.set_2.setText(_translate("Form", "系统设置"))
        self.checkingin_2.setText(_translate("Form", "考勤"))
        self.entrance_2.setText(_translate("Form", "进入门禁"))
        self.visit_2.setText(_translate("Form", "宾客来访"))
        self.goout_2.setText(_translate("Form", "外出门禁"))
        self.select_2.setText(_translate("Form", "查询"))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui= Ui_Form()
        self.ui.setupUi(self)
        self.ui.close.clicked.connect(self.close)  #关闭窗口
        self.ui.min.clicked.connect(self.showMinimized)  #最小化窗口

        timer = QTimer(self)
        timer.timeout.connect(self.showTimeText)
        timer.start()

    def showTimeText(self):
        # 设置宽度
        self.ui.label_time.setFixedWidth(220)
        # 设置显示文本格式
        self.ui.label_time.setStyleSheet(
            # "QLabel{background:white;}" 此处设置背景色
            "QLabel{color:rgb(300,300,300,120); font-size:14px; font-weight:bold; font-family:宋体;}")
        datetime = QDateTime.currentDateTime().toString("yyyy-MM-dd  hh:mm:ss  ddd")
        self.ui.label_time.setText(datetime)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

if __name__ == '__main__':
    try:
        Loaddata()
        print('successful')
    except:
        print('加载失败')
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
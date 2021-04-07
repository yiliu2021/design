from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
global logoinuser
from setmodule.setting_ui import Ui_userset

class set_mod(QWidget):
    def __init__(self):
        super().__init__()
        self.ui=Ui_userset()
        self.ui.setupUi(self)
        #self.setWindowFlags(Qt.WindowStaysOnTopHint)
        global logoinuser
        logoinuser=''

    def deal_emit_slot(self, name):
        global logoinuser
        logoinuser=name
        self.ui.welcome.setText(QtCore.QCoreApplication.translate("userset","<html><head/><body><p align=\"center\">" + logoinuser + "，你好！</p></body></html>"))
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    test_import = set_mod()
    test_import.show()  # 最大化显示
    sys.exit(app.exec_())
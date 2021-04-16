from PyQt5 import QtCore, QtGui, QtWidgets
import qtawesome

class Ui_comein(object):
    def setupUi(self, comein):
        comein.setObjectName("comein")
        comein.resize(730, 574)

        spin_icon = qtawesome.icon('fa5s.coffee', color='black')
        comein.setWindowIcon(spin_icon)

        self.gridLayout = QtWidgets.QGridLayout(comein)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(comein)
        self.label.setStyleSheet("background-color:rgba(0,0,0,91);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.retranslateUi(comein)
        QtCore.QMetaObject.connectSlotsByName(comein)

    def retranslateUi(self, comein):
        _translate = QtCore.QCoreApplication.translate
        comein.setWindowTitle(_translate("comein", "门禁系统"))

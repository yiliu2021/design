# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'goout_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import qtawesome

class Ui_goout(object):
    def setupUi(self, goout):
        goout.setObjectName("goout")
        goout.resize(730, 574)

        spin_icon = qtawesome.icon('fa5s.paper-plane', color='black')
        goout.setWindowIcon(spin_icon)

        self.gridLayout = QtWidgets.QGridLayout(goout)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(goout)
        self.label.setStyleSheet("background-color:rgba(0,0,0,91);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.retranslateUi(goout)
        QtCore.QMetaObject.connectSlotsByName(goout)

    def retranslateUi(self, goout):
        _translate = QtCore.QCoreApplication.translate
        goout.setWindowTitle(_translate("goout", "外出门禁"))

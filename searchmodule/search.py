from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage, QIcon, QPixmap
from PyQt5.QtCore import *
from search_ui import Ui_inquire
import sys
sys.path.append('../')
from warnning import Ui_warn
from mysqlload import *

class inquire_mod(QWidget):
    def __init__(self):
        super().__init__()
        self.ui=Ui_inquire()
        self.ui.setupUi(self)
        self.ui.starting_time.setDateTime(QDateTime.currentDateTime())
        self.ui.end_time.setDateTime(QDateTime.currentDateTime())
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)

        self.ui.search.clicked.connect(self.inquire_logs)
    def inquire_logs(self):
        s_time = self.ui.starting_time.dateTime().toString("yyyy-MM-dd hh:mm:ss")
        e_time = self.ui.end_time.dateTime().toString("yyyy-MM-dd hh:mm:ss")
        if s_time == e_time:
            self.warn = Ui_warn('请设置查询起止时间！')
            self.warn.setWindowModality(Qt.ApplicationModal)
            self.warn.show()
            QtCore.QTimer().singleShot(2000, self.warn.close)
        elif s_time != e_time:
            if self.ui.checkin.isChecked():
                log_table = 'checkin'
            elif self.ui.comein.isChecked():
                log_table = 'comein'
            elif self.ui.goout.isChecked():
                log_table = 'goout'
            contents = self.ui.lineEdit.text()
            if contents == '':
                result, rows = select_table_section(log_table, s_time, e_time)
            else:
                sql = '''SELECT * FROM {table} where ((DATE_FORMAT(
                        datetime,'%Y-%m-%d %H:%i:%s')BETWEEN'{time1}'and'{time2}')
                        AND (number LIKE '%{content}%' OR name LIKE '%{content}%'
                        OR datetime LIKE '%{content}%' OR other LIKE '%{content}%'))'''.format(
                    table=log_table, time1=s_time, time2=e_time, content=contents)
                face, cur = connectsql()
                cur.execute(sql)
                result = cur.fetchall()
                rows = len(result)
                face, cur = connectsql()
            _translate = QtCore.QCoreApplication.translate
            self.ui.tableWidget.setRowCount(rows)
            for i in range(rows):
                item = QtWidgets.QTableWidgetItem()
                self.ui.tableWidget.setVerticalHeaderItem(i, item)
                item = self.ui.tableWidget.verticalHeaderItem(i)
                item.setText(_translate("inquire", str(i + 1)))
            # 遍历二维元组, 显示到界面表格上
            x = 0
            for i in result:
                y = 0
                for j in i:
                    self.ui.tableWidget.setItem(x, y, QtWidgets.QTableWidgetItem(str(result[x][y])))
                    y = y + 1
                x = x + 1
            closesql(face, cur)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    test_import = inquire_mod()
    test_import.show()
    sys.exit(app.exec_())
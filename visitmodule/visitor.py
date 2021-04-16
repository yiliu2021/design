from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage, QIcon, QPixmap
from PyQt5.QtCore import *
from visitor_ui import Ui_visitor
import sys
sys.path.append('../')
from warnning import Ui_warn
from mysqlload import *
from GeneratorModel import *
from datetime import datetime, timedelta
import threading

class visitor_mod(QWidget):
    def __init__(self):
        super().__init__()
        self.ui=Ui_visitor()
        self.ui.setupUi(self)

        # 初始化摄像头
        self.url = cv2.CAP_DSHOW
        self.cap = cv2.VideoCapture()
        self.photos = 0

        self.show_person()
        self.ui.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
        self.ui.dateTimeEdit_2.setDateTime(QDateTime.currentDateTime())
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)

        self.ui.commit.clicked.connect(self.type_in)
        self.ui.start.clicked.connect(self.openCam)
        self.ui.start_2.clicked.connect(self.takePhoto)
        self.ui.start_3.clicked.connect(self.trainModel)
        self.ui.search.clicked.connect(self.search)
        self.ui.edit.clicked.connect(self.edit_person)
        self.ui.delpeo.clicked.connect(self.del_person)

    def type_in(self):
        person_num = self.ui.num.text()
        person_name = self.ui.name.text()
        person_other= self.ui.other.text()
        visit_time = self.ui.dateTimeEdit.dateTime().toString("yyyy-MM-dd hh:mm:ss")
        if self.ui.sex_man.isChecked():
            person_sex='男'
        elif self.ui.sex_wo.isChecked():
            person_sex = '女'
        insider = whether_or_not('insiders', 'number', person_num)
        outsider = whether_or_not('externals', 'number', person_num)
        exist=whether_or_not('visitors','number',person_num)
        if person_num == '' or person_name == '' :
            self.warn = Ui_warn('请完善信息！')
            self.warn.setWindowModality(Qt.ApplicationModal)
            self.warn.show()
        elif insider!=1 and outsider!=1 and exist != 1:
            face, cur = connectsql()
            try:
                sql = "INSERT INTO visitors VALUES {condition}".format(
                    condition=(person_num, person_name, person_sex, visit_time, person_other))
                if cur.execute(sql):
                    face.commit()
                    self.show_person()
                    self.warn = Ui_warn('采集成功！\n请继续录入人脸信息')
                    self.warn.setWindowModality(Qt.ApplicationModal)
                    self.warn.show()
            except:
                face.rollback()
                self.warn = Ui_warn('录入信息失败！')
                self.warn.setWindowModality(Qt.ApplicationModal)
                self.warn.show()
            closesql(face, cur)
        else:
            self.warn = Ui_warn('编号已存在！')
            self.warn.setWindowModality(Qt.ApplicationModal)
            self.warn.show()
    def openCam(self):
        # 判断摄像头是否打开，如果打开则为true，反之为false
        flagCam = self.cap.isOpened()
        if flagCam == False:
            self.num_text = self.ui.num.text()
            exist = whether_or_not('visitors', 'number', self.num_text)
            if exist==1:
                self.warn = Ui_warn('开始采集编号\n'+self.num_text+'图像！')
                self.warn.setWindowModality(Qt.ApplicationModal)
                self.warn.show()
                self.cap.open(self.url)
                t2 = threading.Thread(target=self.showCapture, args=())
                t2.setDaemon(True)
                t2.start()
                #self.showCapture()
            else:
                self.warn = Ui_warn('请输入采集人员编号！')
                self.warn.setWindowModality(Qt.ApplicationModal)
                self.warn.show()
        elif flagCam == True:
            self.cap.release()
    def showCapture(self):
        self.ui.start.setText('停止采集')
        # 导入opencv人脸检测xml文件,文件导入需根据工作目录变更，如从本代码进入删除掉setmodule\\
        cascade = 'setmodule\\haarcascade_frontalface_alt2.xml'
        # 加载 Haar级联人脸检测库
        detector = cv2.CascadeClassifier(cascade)
        # 循环来自视频文件流的帧
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            frame = imutils.resize(frame, width=500)
            QApplication.processEvents()
            rects = detector.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 1.02, 5)
            if len(rects) > 0:  # 大于0则检测到人脸
                for x, y, w, h in rects:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    frame = cv2.putText(frame, "Have token {}/20 face".format(self.photos),
                                        (50, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 100, 50), 2)

            # 显示输出框架
            show_video = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 这里指的是显示原图
            # opencv读取图片的样式，不能通过Qlabel进行显示，需要转换为Qimage。
            # QImage(uchar * data, int width, int height, int bytesPerLine, Format format)
            self.showImage = QImage(show_video.data, show_video.shape[1], show_video.shape[0], QImage.Format_RGB888)
            self.ui.label.setPixmap(QPixmap.fromImage(self.showImage))
            self.ui.label.setScaledContents(True)
            # cv2.destroyAllWindows()
        # 因为最后一张画面会显示在GUI中，此处实现清除
        self.ui.label.clear()
        self.ui.start.setText('打开相机')
    # 创建文件夹
    def mkdir(self, path):
        # 去除首位空格
        path = path.strip()
        # 去除尾部 \ 符号
        path = path.rstrip("\\")
        # 判断路径是否存在, 存在=True; 不存在=False
        isExists = os.path.exists(path)
        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            os.makedirs(path)
            return True
    def takePhoto(self):
        if self.cap.isOpened():
            self.photos += 1
            self.filename = "dataset\\{}\\".format(self.num_text)
            self.mkdir(self.filename)
            photo_save_path = os.path.join(os.path.dirname(os.path.abspath('__file__')), '{}'.format(self.filename))
            self.showImage.save(photo_save_path + datetime.now().strftime("%Y%m%d%H%M%S") + ".png")
            # p = os.path.sep.join([output, "{}.png".format(str(total).zfill(5))])
            # cv2.imwrite(p, self.showImage)
            if self.photos == 20:
                QMessageBox.information(self, "Information", self.tr("采集成功!"), QMessageBox.Yes | QMessageBox.No)
                self.cap.release()
                self.ui.label.clear()
                self.photos = 0
                self.ui.start.setText('打开相机')
        else:
            self.warn = Ui_warn('请打开相机！')
            self.warn.setWindowModality(Qt.ApplicationModal)
            self.warn.show()
    def trainModel(self):
        Generator()
        TrainModel()
        self.warn = Ui_warn('图像提交成功！')
        self.warn.setWindowModality(Qt.ApplicationModal)
        self.warn.show()
    def show_person(self):
        self.ui.tableWidget.setRowCount(0)
        _translate = QtCore.QCoreApplication.translate
        face, cur=connectsql()
        sql = "select * from visitors"
        cur.execute(sql)
        #返回表格所有数据
        insiders = cur.fetchall()
        rows=len(insiders)
        self.ui.tableWidget.setRowCount(rows)
        for i in range(rows):
            item = QtWidgets.QTableWidgetItem()
            self.ui.tableWidget.setVerticalHeaderItem(i, item)
            item = self.ui.tableWidget.verticalHeaderItem(i)
            item.setText(_translate("visitor", str(i+1)))
        # 遍历二维元组, 显示到界面表格上
        x = 0
        for i in insiders:
            y = 0
            for j in i:
                self.ui.tableWidget.setItem(x, y, QtWidgets.QTableWidgetItem(str(insiders[x][y])))
                y = y + 1
            x = x + 1
        closesql(face, cur)
        self.ui.num_2.clear()
        self.ui.name_2.clear()
        self.ui.sex_man_2.setChecked(True)
        self.ui.dateTimeEdit_2.setDateTime(QDateTime.currentDateTime())
        self.ui.other_2.clear()
    def search(self):
        person_num = self.ui.num_2.text()
        if person_num =='':
            self.warn = Ui_warn('请输入人员编号！')
            self.warn.setWindowModality(Qt.ApplicationModal)
            self.warn.show()
        elif whether_or_not('visitors', 'number', person_num) == 1:
            face, cur = connectsql()
            sql = "select * from visitors where number='%s'" % (person_num)
            cur.execute(sql)
            person = cur.fetchone()
            closesql(face, cur)
            self.ui.name_2.setText(person[1])
            self.ui.other_2.setText(person[4])
            if person[2] == '男':
                self.ui.sex_man_2.setChecked(True)
            elif person[2] == '女':
                self.ui.sex_wo_2.setChecked(True)
            self.ui.dateTimeEdit_2.setDateTime(QDateTime.currentDateTime())
        else:
            self.warn = Ui_warn('编号不存在！')
            self.warn.setWindowModality(Qt.ApplicationModal)
            self.warn.show()
    def edit_person(self):
        person_num = self.ui.num_2.text()
        person_name = self.ui.name_2.text()
        person_other = self.ui.other_2.text()
        visit_time = self.ui.dateTimeEdit_2.dateTime().toString("yyyy-MM-dd hh:mm:ss")
        if self.ui.sex_man_2.isChecked():
            person_sex = '男'
        elif self.ui.sex_wo_2.isChecked():
            person_sex = '女'
        exists = whether_or_not('visitors', 'number', person_num)
        if person_num == '' or person_name == '' :
            self.warn = Ui_warn('请完善信息！')
            self.warn.setWindowModality(Qt.ApplicationModal)
            self.warn.show()
        elif exists == 1:
            face, cur = connectsql()
            try:
                sql = "update visitors set name='%s',sex='%s',datetime='%s',other='%s' where number='%s'"%(
                    person_name, person_sex, visit_time,person_other, person_num)
                if cur.execute(sql):
                    face.commit()
                    self.show_person()
                    self.warn = Ui_warn('修改成功！')
                    self.warn.setWindowModality(Qt.ApplicationModal)
                    self.warn.show()
            except:
                face.rollback()
                self.warn = Ui_warn('修改失败！')
                self.warn.setWindowModality(Qt.ApplicationModal)
                self.warn.show()
            closesql(face, cur)
        else:
            self.warn = Ui_warn('编号不存在！')
            self.warn.setWindowModality(Qt.ApplicationModal)
            self.warn.show()
    def del_person(self):
        person_num = self.ui.num_2.text()
        if person_num == '':
            self.warn = Ui_warn('请输入有效编号！')
            self.warn.setWindowModality(Qt.ApplicationModal)
            self.warn.show()
        elif whether_or_not('visitors', 'number', person_num) == 1:
            face, cur = connectsql()
            sql = "DELETE FROM visitors WHERE number='{condition}'".format(condition=person_num)
            try:
                if cur.execute(sql):
                    face.commit()
                    self.show_person()
                    self.warn = Ui_warn('删除成功！')
                    self.warn.setWindowModality(Qt.ApplicationModal)
                    self.warn.show()
            except:
                face.rollback()
                self.warn = Ui_warn('删除失败！')
                self.warn.setWindowModality(Qt.ApplicationModal)
                self.warn.show()
            closesql(face, cur)
        else:
            self.warn = Ui_warn('编号不存在!')
            self.warn.setWindowModality(Qt.ApplicationModal)
            self.warn.show()
    def closeEvent(self, QCloseEvent):
        self.cap.release()
        self.close()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    test_import = visitor_mod()
    test_import.show()
    sys.exit(app.exec_())
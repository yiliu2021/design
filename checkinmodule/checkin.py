from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage, QIcon, QPixmap
from PyQt5.QtCore import *
import sys, os
import cv2, imutils
from mysqlload import *
from datetime import datetime, timedelta
from checkin_ui import Ui_checkin
sys.path.append('../')
from warnning import Ui_warn
# 导入人脸识别检测包
from imutils.video import VideoStream
import numpy as np
import pickle

class checkin_mod(QWidget):
    Signal_parp = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.ui=Ui_checkin()
        self.ui.setupUi(self)
        self.Signal_parp.connect(self.checkin_over)
        # 设置日历为当天时间
        self.ui.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
        self.ui.display_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.ui.belate_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)

        # 初始化摄像头
        self.url = cv2.CAP_DSHOW
        self.cap = cv2.VideoCapture()

        self.ui.start.clicked.connect(self.checkin_fun)
    def left_time(self,end_time):
        currentTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        checkin_time = datetime.strptime(currentTime, '%Y-%m-%d %H:%M:%S')
        set_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        left_time = set_time - checkin_time
        return left_time.days,left_time.seconds
    def checkin_fun(self):
        set_checkin = self.ui.dateTimeEdit.dateTime().toString("yyyy-MM-dd hh:mm:ss")
        left_days, time_section = self.left_time(set_checkin)
        flag = self.cap.isOpened()
        if flag == True:
            self.cap.release()
            self.ui.start.setText('开始考勤')
        elif left_days == 0:
            self.ui.start.setText('退出考勤')
            self.ui.display_table.setRowCount(0)
            self.ui.belate_table.setRowCount(0)
            self.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.set_checkin = set_checkin
            self.time_section = time_section
            self.cap.open(self.url)
            self.start_checkin()
        elif left_days != 0:
            self.warn = Ui_warn('请设定考勤结束时间！')
            self.warn.setWindowModality(Qt.ApplicationModal)
            self.warn.show()
    def start_checkin(self):
        # 初始化需要记录的人名
        self.record_name = ([])
        # OpenCV深度学习人脸检测器的路径
        detector = "face_detection_model"
        # OpenCV深度学习面部嵌入模型的路径
        embedding_model = "face_detection_model/openface_nn4.small2.v1.t7"
        # 训练模型以识别面部的路径
        recognizer_path = "output/recognizer.pickle"
        # 标签编码器的路径
        le_path = "output/le.pickle"
        # 置信度
        confidence_default = 0.99
        # 从磁盘加载序列化面部检测器
        protoPath = os.path.sep.join([detector, "deploy.prototxt"])
        modelPath = os.path.sep.join([detector, "res10_300x300_ssd_iter_140000.caffemodel"])
        detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)
        # 从磁盘加载我们的序列化面嵌入模型
        embedder = cv2.dnn.readNetFromTorch(embedding_model)
        # 加载实际的人脸识别模型和标签
        recognizer = pickle.loads(open(recognizer_path, "rb").read())
        le = pickle.loads(open(le_path, "rb").read())
        # 循环来自视频文件流的帧
        while (self.cap.isOpened()):
            # 从线程视频流中抓取帧
            ret, frame = self.cap.read()
            QApplication.processEvents()
            # 调整框架的大小以使其宽度为900像素（同时保持纵横比），然后抓取图像尺寸
            frame = imutils.resize(frame, width=900)
            (h, w) = frame.shape[:2]
            # 从图像构造一个blob
            imageBlob = cv2.dnn.blobFromImage(
                cv2.resize(frame, (300, 300)), 1.0, (300, 300),
                (104.0, 177.0, 123.0), swapRB=False, crop=False)
            # 应用OpenCV的基于深度学习的人脸检测器来定位输入图像中的人脸
            detector.setInput(imageBlob)
            detections = detector.forward()
            # 保存识别到的人脸
            face_names = []
            # 循环检测
            for i in np.arange(0, detections.shape[2]):
                # 提取与预测相关的置信度（即概率）
                confidence = detections[0, 0, i, 2]
                # 过滤弱检测
                if confidence > confidence_default:
                    # 计算面部边界框的（x，y）坐标
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    # 提取面部ROI
                    face = frame[startY:endY, startX:endX]
                    (fH, fW) = face.shape[:2]
                    # 确保面部宽度和高度足够大
                    if fW < 20 or fH < 20:
                        continue
                    # 为面部ROI构造一个blob，然后通过我们的面部嵌入模型传递blob以获得面部的128-d量化
                    faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255, (96, 96), (0, 0, 0), swapRB=True, crop=False)
                    embedder.setInput(faceBlob)
                    vec = embedder.forward()
                    # 执行分类识别面部
                    preds = recognizer.predict_proba(vec)[0]
                    j = np.argmax(preds)
                    proba = preds[j]
                    name = le.classes_[j]
                    # 绘制面部的边界框以及相关的概率
                    text = "{}: {:.2f}%".format(name, proba * 100)
                    y = startY - 10 if startY - 10 > 10 else startY + 10
                    cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)
                    frame = cv2.putText(frame, text, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
                    face_names.append(name)
            show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 这里指的是显示原图
            # opencv 读取图片的样式，不能通过Qlabel进行显示，需要转换为Qimage QImage(uchar * data, int width,
            showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
            self.ui.label.setPixmap(QPixmap.fromImage(showImage))
            self.ui.label.setScaledContents(True)
            self.set_name = set(face_names)
            #self.set_names = tuple(self.set_name)
            self.recordresult()
            left_days, left_time = self.left_time(self.set_checkin)
            print(left_time,self.time_section)
            if left_time > self.time_section:
                break
        self.cap.release()
        self.ui.label.clear()
        self.ui.start.setText('开始考勤')
        self.Signal_parp.emit('发送成功')
    def checkin_over(self,a):
        face, cur = connectsql()
        _translate = QtCore.QCoreApplication.translate
        sql = '''SELECT number,name,other FROM insiders WHERE number NOT IN (
                        SELECT number FROM checkin where DATE_FORMAT(
                        datetime,'%Y-%m-%d %H:%i:%s') BETWEEN'{a}'and'{b}')'''.format(
            a=self.start_time, b=self.set_checkin)
        cur.execute(sql)
        belate_person = cur.fetchall()
        closesql(face, cur)
        rows = len(belate_person)
        self.ui.belate_table.setRowCount(rows)
        for i in range(rows):
            item = QtWidgets.QTableWidgetItem()
            self.ui.belate_table.setVerticalHeaderItem(i, item)
            item = self.ui.belate_table.verticalHeaderItem(i)
            item.setText(_translate("checkin", str(i + 1)))
        x = 0
        for i in belate_person:
            y = 0
            for j in i:
                self.ui.belate_table.setItem(x, y, QtWidgets.QTableWidgetItem(str(belate_person[x][y])))
                y = y + 1
            self.ui.belate_table.setItem(x, y, QtWidgets.QTableWidgetItem('未到'))
            x = x + 1
        all_checkperson, count = self.select_table_section('checkin', self.start_time, self.set_checkin)
        all_person=rows+count
        self.ui.display.setText('应到：%d名，实到：%d名，未到：%d名。'%(all_person, count, rows))
        self.warn = Ui_warn('考勤结束！')
        self.warn.setWindowModality(Qt.ApplicationModal)
        self.warn.show()
    def recordresult(self):
        if self.set_name.issubset(self.record_name):  # 如果self.set_names是self.record_names 的子集返回ture
            pass  # record_name是要写进数据库中的名字信息 set_name是从摄像头中读出人脸的tuple形式
        else:
            self.different_name = self.set_name.difference(self.record_name)  # 获取到self.set_name有而self.record_name无的名字
            self.record_name = self.set_name.union(self.record_name)  # 把self.record_name变成两个集合的并集
            # different_name是为了获取到之前没有捕捉到的人脸，并再次将record_name进行更新
            # 将集合变成tuple，并统计人数
            self.write_data = tuple(self.different_name)
            names_num = len(self.write_data)
            if names_num > 0:
                face, cur=connectsql()
                other = '已签到'
                checkin_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                try:
                    sql = "SELECT number,name FROM insiders WHERE number ='%s'" % (self.write_data[0])
                    cur.execute(sql)
                    checkin_person = cur.fetchone()
                    insert_sql = "insert into checkin values {condition}".format(
                        condition=(checkin_person[0], checkin_person[1], checkin_time, other))
                    cur.execute(insert_sql)
                    face.commit()
                    self.show_checkinperson()
                except:
                    face.rollback()
                    self.warn = Ui_warn('验证失败，请检查连接！')
                    self.warn.setWindowModality(Qt.ApplicationModal)
                    self.warn.show()
                closesql(face, cur)
    def show_checkinperson(self):
        self.ui.display_table.setRowCount(0)
        _translate = QtCore.QCoreApplication.translate
        face, cur = connectsql()
        all_checkperson, rows= self.select_table_section('checkin', self.start_time, self.set_checkin)
        self.ui.display_table.setRowCount(rows)
        for i in range(rows):
            item = QtWidgets.QTableWidgetItem()
            self.ui.display_table.setVerticalHeaderItem(i, item)
            item = self.ui.display_table.verticalHeaderItem(i)
            item.setText(_translate("checkin", str(i + 1)))
        # 遍历二维元组, 显示到界面表格上
        x = 0
        for i in all_checkperson:
            y = 0
            for j in i:
                self.ui.display_table.setItem(x, y, QtWidgets.QTableWidgetItem(str(all_checkperson[x][y])))
                y = y + 1
            x = x + 1
        closesql(face, cur)
    def select_table_section(self,table,start_time,end_time):
        face, cur = connectsql()
        sql = "select * from {table} where DATE_FORMAT(datetime,'%Y-%m-%d %H:%i:%s') BETWEEN'{a}'and'{b}'".format(
            table=table, a=start_time, b=end_time)
        cur.execute(sql)
        nead_table = cur.fetchall()
        logs=len(nead_table)
        closesql(face, cur)
        return nead_table, logs
    def close(self):
        self.cap.release()
        self.close()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    test_import = checkin_mod()
    test_import.show()  # 最大化显示
    sys.exit(app.exec_())
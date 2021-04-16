from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage, QIcon, QPixmap
from PyQt5.QtCore import *
global logoinuser
#设置模块在独立于主程序的文件夹，为确保主程序引入不出错误，独立模块文件夹内相互引用宜加上文件夹名称
from setmodule.setting_ui import Ui_userset
import sys
sys.path.append('../')
from warnning import Ui_warn
from mysqlload import *
from GeneratorModel import *
from datetime import datetime, timedelta
import threading

class set_mod(QWidget):
    def __init__(self):
        super().__init__()
        self.ui=Ui_userset()
        self.ui.setupUi(self)
        #self.setWindowFlags(Qt.WindowStaysOnTopHint)

        global logoinuser
        logoinuser=''
        # 初始化摄像头
        self.url = cv2.CAP_DSHOW
        self.cap = cv2.VideoCapture()
        self.photos = 0

        self.show_person()
        self.show_leaves()

        self.ui.commit.clicked.connect(self.type_in)
        self.ui.start.clicked.connect(self.openCam)
        self.ui.start_2.clicked.connect(self.takePhoto)
        self.ui.start_3.clicked.connect(self.trainModel)
        self.ui.search.clicked.connect(self.search)
        self.ui.editin.toggled.connect(self.show_person)
        self.ui.editout.toggled.connect(self.show_person)
        self.ui.edit.clicked.connect(self.edit_person)
        self.ui.delpeo.clicked.connect(self.del_person)
        self.ui.confire.clicked.connect(self.leave_person)
        self.ui.query.clicked.connect(self.edit_password)
        self.ui.addmanager.clicked.connect(self.add_manager)
        self.ui.delmanager_2.clicked.connect(self.del_manager)

    def deal_emit_slot(self, name):
        _translate = QtCore.QCoreApplication.translate
        global logoinuser
        logoinuser=name
        # 设置日历为当天时间
        self.ui.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
        # 如从登录界面启动此处可接收logoin发送的信号，可以执行下一条程序，即可跳转设置模块
        # self.show()
        if logoinuser=='admin':
            self.ui.label_12.setText(
                _translate("userset", "<html><head/><body><p align=\"center\">账户管理</p></body></html>"))
            self.ui.welcome.setText(
                _translate("userset","<html><head/><body><p align=\"center\">"+
                           logoinuser + "，你好！</p></body></html>"))
            try:
                self.show_user()
            except:
                self.warn = Ui_warn('数据加载失败！')
                self.warn.setWindowModality(Qt.ApplicationModal)
                self.warn.show()
        else:
            self.ui.welcome.setText(
                _translate("userset","<html><head/><body><p align=\"center\">"+
                           logoinuser + "，你好！</p></body></html>"))
            self.ui.tableWidget_3.setRowCount(0)
            self.ui.adduser.setEnabled(False)
            self.ui.label_12.setText(
                _translate("userset", "<html><head/><body><p align=\"center\">账户编辑需管理员权限！</p></body></html>"))

    def type_in(self):
        person_num = self.ui.num.text()
        person_name = self.ui.name.text()
        person_other= self.ui.other.text()
        if self.ui.inputin.isChecked():
            person_table='insiders'
        elif self.ui.inputout.isChecked():
            person_table = 'externals'
        if self.ui.sex_man.isChecked():
            person_sex='男'
        elif self.ui.sex_wo.isChecked():
            person_sex = '女'
        insider=whether_or_not('insiders','number',person_num)
        outsider=whether_or_not('externals','number',person_num)
        visitor=whether_or_not('visitors','number',person_num)
        if person_num == '' or person_name == '' :
            self.warn = Ui_warn('请完善信息！')
            self.warn.setWindowModality(Qt.ApplicationModal)
            self.warn.show()
        elif insider!=1 and outsider!=1 and visitor!=1:
            face, cur = connectsql()
            try:
                sql = "INSERT INTO %s VALUES ('%s','%s','%s','%s')"%(
                    person_table,person_num,person_name,person_sex,person_other)
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
            insider = whether_or_not('insiders', 'number', self.num_text)
            outsider = whether_or_not('externals', 'number', self.num_text)
            if insider==1 or outsider==1:
                self.warn = Ui_warn('开始采集编号\n'+self.num_text+'图像！')
                self.warn.setWindowModality(Qt.ApplicationModal)
                self.warn.show()
                QtCore.QTimer().singleShot(2000, self.warn.close)
                self.cap.open(self.url)
                t1 = threading.Thread(target=self.showCapture, args=())
                t1.setDaemon(True)
                t1.start()
                #self.showCapture()
            else:
                self.warn = Ui_warn('请输入有效编号！')
                self.warn.setWindowModality(Qt.ApplicationModal)
                self.warn.show()
        elif flagCam == True:
            self.cap.release()
            #self.ui.start.setText('打开相机')
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
            rects = detector.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),
                                              scaleFactor=1.02, minNeighbors=5, minSize=(30, 30))
            if len(rects) > 0: # 大于0则检测到人脸
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
        if self.ui.editin.isChecked():
            person_table = 'insiders'
        elif self.ui.editout.isChecked():
            person_table = 'externals'
        _translate = QtCore.QCoreApplication.translate
        face, cur=connectsql()
        sql = "select * from %s"%(person_table)
        cur.execute(sql)
        #返回表格所有数据
        insiders = cur.fetchall()
        rows=len(insiders)
        self.ui.tableWidget.setRowCount(rows)
        for i in range(rows):
            item = QtWidgets.QTableWidgetItem()
            self.ui.tableWidget.setVerticalHeaderItem(i, item)
            item = self.ui.tableWidget.verticalHeaderItem(i)
            item.setText(_translate("userset", str(i+1)))
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
        self.ui.other_2.clear()
    def search(self):
        person_num = self.ui.num_2.text()
        if self.ui.editin.isChecked():
            person_table = 'insiders'
            per='外单位'
        elif self.ui.editout.isChecked():
            person_table = 'externals'
            per='本单位'
        if person_num =='':
            self.warn = Ui_warn('请输入人员编号！')
            self.warn.setWindowModality(Qt.ApplicationModal)
            self.warn.show()
        else:
            exists = whether_or_not(person_table, 'number', person_num)
            if exists == 1:
                face, cur = connectsql()
                sql="select * from %s where number='%s'"%(person_table,person_num)
                cur.execute(sql)
                person = cur.fetchone()
                self.ui.name_2.setText(person[1])
                self.ui.other_2.setText(person[3])
                if person[2]=='男':
                    self.ui.sex_man_2.setChecked(True)
                elif person[2]=='女':
                    self.ui.sex_wo_2.setChecked(True)
                closesql(face, cur)
            else:
                self.warn = Ui_warn('编号：'+person_num+'\n为'+per+'人员或不存在！')
                self.warn.setWindowModality(Qt.ApplicationModal)
                self.warn.show()
    def edit_person(self):
        person_num = self.ui.num_2.text()
        person_name = self.ui.name_2.text()
        person_other = self.ui.other_2.text()
        if self.ui.editin.isChecked():
            person_table = 'insiders'
            per = '本单位'
        elif self.ui.editout.isChecked():
            person_table = 'externals'
            per = '外单位'
        if self.ui.sex_man_2.isChecked():
            person_sex = '男'
        elif self.ui.sex_wo_2.isChecked():
            person_sex = '女'
        exists = whether_or_not(person_table, 'number', person_num)
        if person_num == '' or person_name == '' :
            self.warn = Ui_warn('请完善信息！')
            self.warn.setWindowModality(Qt.ApplicationModal)
            self.warn.show()
        elif exists==1:
            face, cur = connectsql()
            try:
                sql = "update %s set name='%s',sex='%s',other='%s' where number='%s'"%(
                    person_table,person_name,person_sex,person_other,person_num)
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
            self.warn = Ui_warn('编号不存在或不在'+per+'！')
            self.warn.setWindowModality(Qt.ApplicationModal)
            self.warn.show()
    def del_person(self):
        person_num = self.ui.num_2.text()
        if self.ui.editin.isChecked():
            person_table = 'insiders'
            per = '本单位'
        elif self.ui.editout.isChecked():
            person_table = 'externals'
            per = '外单位'
        if person_num == '':
            self.warn = Ui_warn('请输入有效编号！')
            self.warn.setWindowModality(Qt.ApplicationModal)
            self.warn.show()
        elif whether_or_not(person_table, 'number', person_num)==1:
            face, cur = connectsql()
            sql = "DELETE FROM {table} WHERE number='{condition}'".format(table=person_table, condition=person_num)
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
            self.warn = Ui_warn('编号不存在!\n或用户不在'+per+'！')
            self.warn.setWindowModality(Qt.ApplicationModal)
            self.warn.show()
    def leave_person(self):
        person_num = self.ui.num_3.text()
        if person_num == '':
            self.warn = Ui_warn('请输入有效编号！')
            self.warn.setWindowModality(Qt.ApplicationModal)
            self.warn.show()
        elif whether_or_not('insiders', 'number', person_num)==1:
            confire_time = self.ui.dateTimeEdit.dateTime().toString("yyyy-MM-dd hh:mm:ss")
            face, cur = connectsql()
            sql = "select * from insiders where number='%s'"%(person_num)
            cur.execute(sql)
            per = cur.fetchone()
            if whether_or_not('gooutperson', 'number', person_num)==1:
                update_sql = "update gooutperson set datetime='%s' where number='%s'" % (
                    confire_time, person_num)
                cur.execute(update_sql)
            else:
                insert_sql = "INSERT INTO gooutperson VALUES {condition}".format(condition=(
                per[0], per[1], per[2], confire_time, per[3]))
                cur.execute(insert_sql)
            face.commit()
            closesql(face, cur)
            self.ui.name_3.setText(per[1])
            self.show_leaves()
            #python时间字符串必须格式一致，字符串和date格式转换需要格式一致，date格式运算分隔号不影响
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            now_1=datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
            confire_time_1=datetime.strptime(confire_time, '%Y-%m-%d %H:%M:%S')
            flag=confire_time_1-now_1
            if flag.days >= 0:
                self.warn = Ui_warn('批假成功！')
                self.warn.setWindowModality(Qt.ApplicationModal)
                self.warn.show()
            else:
                self.warn = Ui_warn('外出时间已过，操作无效！')
                self.warn.setWindowModality(Qt.ApplicationModal)
                self.warn.show()
        else:
            self.warn = Ui_warn('非本单位人员！')
            self.warn.setWindowModality(Qt.ApplicationModal)
            self.warn.show()
    def show_leaves(self):
        _translate = QtCore.QCoreApplication.translate
        self.ui.tableWidget_2.setRowCount(0)
        face, cur = connectsql()
        now_time = datetime.now()
        end_time = now_time + timedelta(days=30)
        a = now_time.strftime("%Y%m%d %H:%M:%S")
        b = end_time.strftime("%Y%m%d %H:%M:%S")
        sql = "select * from gooutperson where DATE_FORMAT(datetime,'%Y%m%d %H:%i:%s') BETWEEN'{a}'and'{b}'".format(
            a=a,b=b)
        cur.execute(sql)
        # 返回表格所有数据
        goout_per = cur.fetchall()
        rows = len(goout_per)
        self.ui.tableWidget_2.setRowCount(rows)
        # 根据内容重新设定第3列
        self.ui.tableWidget_2.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        for i in range(rows):
            item = QtWidgets.QTableWidgetItem()
            self.ui.tableWidget_2.setVerticalHeaderItem(i, item)
            item = self.ui.tableWidget_2.verticalHeaderItem(i)
            item.setText(_translate("userset", str(i + 1)))
        # 遍历二维元组, 显示到界面表格上
        x = 0
        for i in goout_per:
            y = 0
            for j in i:
                self.ui.tableWidget_2.setItem(x, y, QtWidgets.QTableWidgetItem(str(goout_per[x][y])))
                y = y + 1
            x = x + 1
        closesql(face, cur)
    def edit_password(self):
        old_pass = self.ui.passold.text()
        new_pass = self.ui.newpass.text()
        new_passagain = self.ui.newpass_2.text()
        global logoinuser
        face, cur = connectsql()
        sql = "select password from users where user='%s'"%(logoinuser)
        cur.execute(sql)
        user_pass = cur.fetchone()
        if old_pass=='' or new_pass==''or new_passagain=='':
            self.warn = Ui_warn('无效信息！')
            self.warn.setWindowModality(Qt.ApplicationModal)
            self.warn.show()
        elif new_pass==new_passagain and user_pass[0]==old_pass:
            try:
                edit_sql="update users set password='%s' where user='%s'"%(new_pass,logoinuser)
                if cur.execute(edit_sql):
                    face.commit()
                    self.warn = Ui_warn('密码修改成功！')
                    self.warn.setWindowModality(Qt.ApplicationModal)
                    self.warn.show()
            except:
                face.rollback()
                self.warn = Ui_warn('密码修改失败！')
                self.warn.setWindowModality(Qt.ApplicationModal)
                self.warn.show()
        else:
            self.warn = Ui_warn('重新输入密码！\n新密码两次输入要求一致')
            self.warn.setWindowModality(Qt.ApplicationModal)
            self.warn.show()
        closesql(face, cur)
        self.ui.passold.clear()
        self.ui.newpass.clear()
        self.ui.newpass_2.clear()
    def show_user(self):
        _translate = QtCore.QCoreApplication.translate
        self.ui.adduser.setEnabled(True)
        face,cur=connectsql()
        sql = "select user from users"
        cur.execute(sql)
        #返回表格所有数据
        suppass = cur.fetchall()
        user_rows=len(suppass)
        self.ui.tableWidget_3.setRowCount(user_rows)
        for i in range(user_rows):
            item = QtWidgets.QTableWidgetItem()
            self.ui.tableWidget_3.setVerticalHeaderItem(i, item)
            item = self.ui.tableWidget_3.verticalHeaderItem(i)
            item.setText(_translate("userset", str(i+1)))
        # 遍历二维元组, 将user显示到界面表格上
        x = 0
        for i in suppass:
            y = 0
            for j in i:
                self.ui.tableWidget_3.setItem(x, y, QtWidgets.QTableWidgetItem(str(suppass[x][y])))
                y = y + 1
            x = x + 1
        closesql(face, cur)
    def add_manager(self):
        ad_pass = self.ui.adminpass.text()
        user_name = self.ui.manageuser.text()
        user_pass = self.ui.userpass.text()
        user_pass2 = self.ui.userpass_2.text()
        face,cur = connectsql()
        sql = "select password from users where user='admin'"
        cur.execute(sql)
        suppass = cur.fetchone()
        if ad_pass=='' or user_name==''or user_pass==''or user_pass2=='':
            self.warn = Ui_warn('无效信息！')
            self.warn.setWindowModality(Qt.ApplicationModal)
            self.warn.show()
        elif user_pass==user_pass2 and user_name !='admin' and ad_pass == suppass[0]:
            try:
                insert_sql = "insert into users values ('%s','%s')"%(user_name,user_pass)
                if cur.execute(insert_sql):
                    face.commit()
                    self.ui.tableWidget_3.setRowCount(0)
                    self.show_user()
                    self.warn = Ui_warn('用户添加成功！')
                    self.warn.setWindowModality(Qt.ApplicationModal)
                    self.warn.show()
            except:
                face.rollback()
                self.warn = Ui_warn('用户添加失败！\n请确认用户是否存在！\n请检查数据连接！')
                self.warn.setWindowModality(Qt.ApplicationModal)
                self.warn.show()
        else:
            self.warn = Ui_warn('信息输入错误！')
            self.warn.setWindowModality(Qt.ApplicationModal)
            self.warn.show()
        closesql(face, cur)
        self.ui.adminpass.clear()
        self.ui.manageuser.clear()
        self.ui.userpass.clear()
        self.ui.userpass_2.clear()
    def del_manager(self):
        ad_pass = self.ui.adminpass.text()
        user_name = self.ui.manageuser.text()
        if ad_pass=='' or user_name=='' or user_name=='admin':
            self.warn = Ui_warn('无效信息！')
            self.warn.setWindowModality(Qt.ApplicationModal)
            self.warn.show()
        else:
            face, cur = connectsql()
            sql = "select password from users where user='admin'"
            cur.execute(sql)
            suppass = cur.fetchone()
            count=whether_or_not('users','user',user_name)
            if ad_pass == suppass[0] and count==1:
                try:
                    del_sql="DELETE FROM {table} WHERE user='{condition}'".format(
                        table = 'users', condition = user_name)
                    if cur.execute(del_sql):
                        face.commit()
                        self.ui.tableWidget_3.setRowCount(0)
                        self.show_user()
                        self.warn = Ui_warn('用户删除成功！')
                        self.warn.setWindowModality(Qt.ApplicationModal)
                        self.warn.show()
                except:
                    face.rollback()
                    self.warn = Ui_warn('用户删除失败！\n请检查数据连接！')
                    self.warn.setWindowModality(Qt.ApplicationModal)
                    self.warn.show()
            else:
                self.warn = Ui_warn('管理员密码错误!\n或用户不存在！')
                self.warn.setWindowModality(Qt.ApplicationModal)
                self.warn.show()
            closesql(face, cur)
        self.ui.adminpass.clear()
        self.ui.manageuser.clear()
        self.ui.userpass.clear()
        self.ui.userpass_2.clear()
    def closeEvent(self, QCloseEvent):
        self.cap.release()
        self.close()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    test_import = set_mod()
    test_import.show()  # 最大化显示
    sys.exit(app.exec_())
# This Python file uses the following encoding: utf-8
from PySide6.QtCore import QObject, Slot, Signal
import json
import os
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


class UserManagers(QObject):

    logoutSignal = Signal()
    successSignal = Signal(int)
    failureSignal = Signal()
    verificationFinish = Signal(int)

    def __init__(self, parent=None):
        super(UserManagers, self).__init__()
        self._filename = "users.json"
        self._from_address = "yon_gui@outlook.com"
        self._emailPassword = "1Qaz-pl,"
        self.verificationCode = ""

        # 使用 SMTP 连接 Outlook 邮箱服务器
        smtp_server = "smtp.office365.com"
        smtp_port = 587
        self._server = smtplib.SMTP(smtp_server, smtp_port)
        self._server.starttls()

        self.user = ""
        self.passwd = ""


        # 登录到 Outlook 邮箱
        self._server.login(self._from_address, self._emailPassword)

        if os.path.isfile(self._filename):
            # 文件已存在，读取文件内容
            with open(self._filename, "r") as f:
                self.userData = json.load(f)
        else:
            # 文件不存在，创建一个新文件
            data = {"users": []}
            with open(self._filename, "w") as f:
                json.dump(data, f)

    @Slot(str, str)
    def login(self, username, password):
        for i in self.userData["users"]:
            if i["username"] == username and i["password"] == password:
                self.successSignal.emit(1)
                self.user = username
                self.passwd = password
                break;
        self.failureSignal.emit()


    @Slot(str, str)
    def register(self, username, password):
        data = {"username": username, "password": password}
        self.userData["users"].append(data)

        with open(self._filename, "w") as f:
            json.dump(self.userData, f)

    @Slot()
    def logout(self):
        count = 0
        for i in self.userData["users"]:
            if i["username"] == self.user and i["password"] == self.passwd:
                self.userData["users"].pop(count)
                break
            count = count + 1
        self.logoutSignal.emit()

    @Slot(str)
    def send_verification_code(self, to_address):

        self.verificationCode = random.randint(1000, 9999)

        # 创建电子邮件消息
        message = MIMEMultipart()
        message["Subject"] = "欢迎注册咏桂"
        message["From"] = self._from_address
        message["To"] = to_address
        message.attach(MIMEText(f"验证码：{self.verificationCode}"))

        # 发送电子邮件
        self._server.sendmail(self._from_address, to_address, message.as_string())


    @Slot()
    def send_email_txt(self):
        message = MIMEMultipart()
        message["Subject"] = "咏桂的的书礼"

        # 添加邮件正文
        body = "吾是天边的一朵云，自始飘在你的天空"
        message.attach(MIMEText(body, 'plain'))
        # 添加附件
        with open('resourceFiles/you_gui.pdf', 'rb') as f:
            attachment = MIMEApplication(f.read(), _subtype='pdf')
            attachment.add_header('Content-Disposition', 'attachment', filename='you_gui.pdf')
            message.attach(attachment)

        self._server.sendmail(self._from_address, self.user, message.as_string())

    @Slot(str)
    def check_verification_code(self, code):
        if str(self.verificationCode) == code:
            self.verificationFinish.emit(2)
        else:
            self.verificationFinish.emit(1)

#    @Slot()
#    def email_quit(self):
#        self._server.quit()


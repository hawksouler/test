# !/usr/bin/env python3
# -*- coding:utf-8 -*-

# /*==========================================================
# Program:email_op.py
# Author:kouity
# mail:kouity@163.com
# Version: V1.1 First release
# Created: 2021/09/06 2022/06/23
# Explain: 电子邮件控制单元 增加附件功能
# /*==========================================================$

from smtplib import SMTP
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


class MyEmail(object):
    def __init__(self, sender='35950375@qq.com', sendersmtp='smtp.qq.com',
                 receivers=['80702265@qq.com',
                            'kouity@163.com', '35950375@qq.com'],
                 text='test', sendername='孔嵘',
                 receivername='刘敏健', emailsubject='测试', att=[]):
        self.sender = sender
        self.sendersmtp = sendersmtp
        self.pssswd = 'xpnukhkzyhyfbiaa'  # 授权码
        # self.receivers = ['80702265@qq.com', 'kouity@163.com']
        self.receivers = receivers
        self.text = text
        self.sendername = sendername
        self.receiversname = receivername
        self.emailsubject = emailsubject
        self.att = att
        self.message = MIMEMultipart()
        # self.message = MIMEText(self.text, _subtype='plain', _charset='utf-8')
        self.message['From'] = Header(self.sendername, 'utf-8')
        self.message['To'] = Header(self.receiversname, 'utf-8')
        self.message['Subject'] = Header(self.emailsubject, 'utf-8')
        self.smtper = SMTP(self.sendersmtp)

    def sendmail(self):
        if len(self.att) == 0:
            self.message.attach(
                MIMEText(self.text, _subtype='plain', _charset='utf-8'))
            self.smtper.login(self.sender, self.pssswd)
            self.smtper.sendmail(self.sender, self.receivers,
                                 self.message.as_string())
            # print('邮件发送完成!')
        else:
            # email_attanchment_address 为文件列表
            for i in range(len(self.att)):
                # 添加附件，由于定义了中文编码，所以文件可以带中文
                att1 = MIMEText(
                    open(self.att[i], 'rb').read(), 'base64', 'utf-8')
                # 数据传输类型的定义
                att1["Content-Type"] = 'application/octet-stream'
                # 定义文件在邮件中显示的文件名和后缀名，名字不可为中文
                att1["Content-Disposition"] = 'attachment;filename="BGY_{path}.csv"'.format(
                    path=i)
                # 将附件添加到邮件内容当中
                self.message.attach(att1)
            self.message.attach(
                MIMEText(self.text, _subtype='plain', _charset='utf-8'))
            self.smtper.login(self.sender, self.pssswd)
            self.smtper.sendmail(self.sender, self.receivers,
                                 self.message.as_string())


if __name__ == '__main__':
    mytest = MyEmail(text='now test', receivers=[
                     'kouity@163.com', '35950375@qq.com'], att=['F:\Pythontest\pytest_liunx\mydata\碧桂园天荟.csv'])
    # mytest.text='now test'
    mytest.sendmail()

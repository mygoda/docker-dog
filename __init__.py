# -*- coding: utf-8 -*-
# __author__ = xutao
from flask_mail import Mail
from flask import Flask

app = Flask(__name__)

app.config["MAIL_SERVER"] = "mail.yun-idc.com"
app.config["MAIL_USERNAME"] = "cds\cdsservice"
app.config["MAIL_PASSWORD"] = "yun-idc.com"
app.config["MAIL_DEFAULT_SENDER"] = "18346552658@163.com"
app.config["MAIL_PORT"] = 443

mail = Mail(app)


def send_mail(msg):
    """
        发送邮件
    """
    mail.send(msg)

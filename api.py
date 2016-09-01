# -*- coding: utf-8 -*-
# __author__ = xutao
import time
from flask import Flask
from flask import jsonify
from flask_mail import Mail
from datetime import datetime
from flask import request
from flask_mail import Message
from datetime import timedelta
from celery import Celery
from utils import request_health, handle_not_ok
from hosts import check_hosts

app = Flask(__name__)

app.config["MAIL_SERVER"] = "mail.yun-idc.com"
app.config["MAIL_USERNAME"] = "cds\cdsservice"
app.config["MAIL_PASSWORD"] = "yun-idc.com"
app.config["MAIL_DEFAULT_SENDER"] = "18346552658@163.com"
app.config["MAIL_PORT"] = 443

mail = Mail(app)

# just for config for celery
app.config['CELERY_BROKER_URL'] = 'redis://:@localhost:6379/2'
app.config['CELERY_RESULT_BACKEND'] = 'redis://:@localhost:6379/2'
app.config["CELERY_TASK_SERIALIZER"] = "json"
app.config["CELERY_RESULT_SERIALIZER"] = "json"
app.config["CELERY_ACCEPT_CONTENT"] = ["json"]
app.config["CELERYD_TASK_TIME_LIMIT"] = 1200
app.config["CELERYBEAT_SCHEDULE"] = {
    "check_health": {
        "task": "check_health",
        'schedule': timedelta(minutes=1)
    }
}
app.config["CELERY_SEND_TASK_ERROR_EMAILS"] = True


celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)



@celery.task
def check_health():
    """
        just check service
    """
    now = datetime.now()
    print("check in %s for %s" % (now, check_hosts))
    for check_host in check_hosts:
        host = check_host.get("ip")
        port = check_host.get("port")
        name = check_host.get("name")
        is_ok, result = request_health(host=host, port=port)
        if not is_ok:
            print("host %s port %s name %s is not ok %s" % (host, port, name, result))
            status = handle_not_ok(check_host, result)
            print("host %s is status %s" % (host, status))


@app.route('/test/', methods=["POST"])
def hello_test():
    msg = Message("hello", recipients=["18346552658@163,com"])
    mail.send(msg)
    return jsonify({})


@app.route('/health/', methods=["GET"])
def health():
    """
        创建种子
    :return:
    """
    return "ok"


if __name__ == '__main__':
    app.run(host="0.0.0.0")

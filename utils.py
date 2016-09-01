# -*- coding: utf-8 -*-
# __author__ = xutao

import requests
from hosts import *
from flask_mail import Message

# just for some utils in it

HEALTH_URL = "health"
TIMES = 3


def is_health(result):
    """
        是否健康
    """
    if "ok" in result or "OK" in result:
        return True
    else:
        return False


def request_health(host, port):
    """
        just for post get response
    """
    url = "http://%s:%s/%s/" % (host, port, HEALTH_URL)

    result = requests.get(url)

    if result.ok:
        if is_health(result.content):
            return True, result.content
    return False, result.content


def try_again(host):
    """
        try get again
    """
    import time

    for i in range(TIMES):
        print("try %s for host %s" % (i, host))
        status, result = request_health(host=host.get("ip"), port=host.get("port"))
        if status:
            return True
        time.sleep(3)
    return False


def handle_not_ok(host, result):
    """
        just for handle not ok service
    """
    print("this %s is not ok rresult is %s" % (host, result))
    try_status = try_again(host=host)
    if try_status:
        print("host %s try success" % host)
        return True
    title = "线上docker服务预警"
    msg = "service %s in host %s:%s fail" % (host.get("name"), host.get("ip"), host.get("port"))
    try:
        email_msg = Message("hello", recipients=["tao.xu@yun-idc.com"])
        print('错误监控邮件(%s)发送%s' % (title, '成功' if msg else '失败'))
    except Exception as e:
        print("错误监控邮件发送失败:%s" % e.message)
    return True

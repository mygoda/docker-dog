# -*- coding: utf-8 -*-
# __author__ = xutao

# hosts just like [
#   {
#       "ip": "ip地址",
#       "port": "端口",
#        "name": u"服务名称"
# }
# ]

EMAIL_HOST = "mail.yun-idc.com"
EMAIL_HOST_USER = "cds\cdsservice"
EMAIL_HOST_PASSWORD = "yun-idc.com"
EMAIL_POSTFIX = "yun-idc.com"
EMAIL_PORT = 443
BILLING_ALARM_EMAIL = ["tao.xu@yun-idc.com"]

check_hosts = [
    {
        "ip": "114.112.92.250",
        "port": 9001,
        "name": u"core task b",
    }
]

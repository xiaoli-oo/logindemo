# -*- coding: utf-8 -*-
import logging
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# 通用配置
AccessKeyId = ""
AccessKeySecret = ""
REGION = ''

# 短信模板
SMS_SIGN_NAME = ''
SMS_CODE = ""

# OSS文件路径
BUCKER_NAME = ""
BUCKER_PUBLIC_NAME = ""
END_POINT = ''  # 公网地址
INTERNAL_END_POINT = ''  # 内网地址

# 回调地址，也可以在调用接口的时候覆盖
NOTIFY_URL = 'https://***********/api/order/alipay/callback/'

# 支付成功跳回地址，也可以在调用接口的时候覆盖
RETURN_URL = 'https://***********/#/pages/index/'

# 支付宝网关地址
ALI_PAY_SERVER_URL = 'https://openapi.alipay.com/gateway.do'

# APP信息
APPID_PCWEB = ''
# 应用私钥
APP_PRIVATE_KEY = ''
# 支付宝公钥
ALIPAY_PUBLIC_KEY = ''

# 日志记录器，记录web请求和回调细节
ALIPAY_LOG_DIR = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(ALIPAY_LOG_DIR):
    os.mkdir(ALIPAY_LOG_DIR)

logging.basicConfig(filename=os.path.join(ALIPAY_LOG_DIR, 'ali.log'),
                    level=logging.DEBUG, filemode='a',
                    format='%(asctime)s - %(process)s - %(levelname)s: %(message)s')
LOGGER = logging.getLogger("ali")


USERFILE = "user/"
# -*- coding: utf-8 -*-
import logging
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# 微信支付商户号（直连模式）或服务商商户号（服务商模式，即sp_mchid)
MCHID = ''

# APPID-微信小程序
APPID_XCX = ""

# APPID-服务号
APPID_FWH = ''

# 商户证书序列号
CERT_SERIAL_NO = ""

# API v3密钥，
APIV3_KEY = ""

# 回调地址，也可以在调用接口的时候覆盖
NOTIFY_URL = ""

# 接入模式:False=直连商户模式，True=服务商模式
PARTNER_MODE = False

# 代理设置
PROXY = None

# 微信独立日志记录器，记录web请求和回调细节
WXPAY_LOG_DIR = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(WXPAY_LOG_DIR):
    os.mkdir(WXPAY_LOG_DIR)

logging.basicConfig(filename=os.path.join(WXPAY_LOG_DIR, 'wx.log'), level=logging.DEBUG, filemode='a',
                    format='%(asctime)s - %(process)s - %(levelname)s: %(message)s')
LOGGER = logging.getLogger("wx")

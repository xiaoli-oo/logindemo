import configparser
import os
from pathlib import Path

config = configparser.ConfigParser()
config.read(os.path.join(Path(__file__).resolve().parent, 'config.ini'), encoding='utf-8')

WEB_URL = "www.logindemo.com"
WEB_NAME = "登录"
WEB_COMPANY = u"登录"
WEB_DESCRIPTION = U"登录"

# 用户缓存过期时间
COOKIE_AGE = 6 * 3600
# 用户token过期时间
USER_TOKEN_EXP = 3 * 24 * 3600  # 秒
# 页面缓存时间
CACHE_PAGE_TIMEOUT = 1 * 3600
# 标识页面默认显示*条记录
LIST_SIZE = 15
# API-接口版本
VERSION = config.get('common', 'VERSION')

# 调试模式
DEBUG = eval(config.get('common', 'DEBUG'))

# Redis配置
REDIS_HOST = config.get('redis', 'REDIS_HOST')
REDIS_PORT = int(config.get('redis', 'REDIS_PORT'))
REDIS_PASSWORD = config.get('redis', 'REDIS_PASSWORD')
# mysql 配置
MYSQL_HOST = config.get('mysql', 'MYSQL_HOST')
MYSQL_USER = config.get('mysql', 'MYSQL_USER')
MYSQL_PASS = config.get('mysql', 'MYSQL_PASS')
MYSQL_PORT = config.get('mysql', 'MYSQL_PORT')
MYSQL_DB = config.get('mysql', 'MYSQL_DB')

# API: AES
AESKEY = config.get('common', 'AESKEY')
AESIV = config.get('common', 'AESIV')
TOKEN_AESKEY = config.get('common', 'TOKEN_AESKEY')

# 默认每页查询数据条目数
PER_PAGE = 15
# 更新数据阀值
DAYS_COUNT = 30
# 任务过期时间
TASK_EXPIRED_TIME = 24  # h

# 验证码超时时间
V_CODE_TIMEOUT = 60 * 5

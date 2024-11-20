import json
import os
import uuid
from math import radians, cos, sin, asin, sqrt
from PIL import Image
import re, random
import datetime
from datetime import timedelta
import time
import calendar
import hashlib
from urllib.parse import urljoin
import math
import filetype
import fake_useragent
import zipfile
import requests
import socket
import struct
from bs4 import BeautifulSoup
from django.conf import settings
from django.utils import timezone
from django.db import connections
from django.db import connection


def timebefore(d):
    import datetime
    chunks = (
        (60 * 60 * 24 * 365, u'年'),
        (60 * 60 * 24 * 30, u'月'),
        (60 * 60 * 24 * 7, u'周'),
        (60 * 60 * 24, u'天'),
        (60 * 60, u'小时'),
        (60, u'分钟'),
    )
    # 如果不是datetime类型转换后与datetime比较
    if not isinstance(d, datetime.datetime):
        d = datetime.datetime(d.year, d.month, d.day)
    now = timezone.now()
    delta = now - d
    # 忽略毫秒
    before = delta.days * 24 * 60 * 60 + delta.seconds
    # 刚刚过去的1分钟
    if before <= 60:
        return u'刚刚'
    for seconds, unit in chunks:
        count = before // seconds
        if count != 0:
            break
    return str(count) + unit + u"前"


def get_ip(request):
    if request.META.get('HTTP_X_FORWARDED_FOR'):
        return request.META['HTTP_X_FORWARDED_FOR']
    else:
        return request.META['REMOTE_ADDR']


def ip2long(ip):
    "将点分十进制 IP 地址转换成无符号的长整数"
    return struct.unpack("!I", socket.inet_aton(ip))[0]


def long2ip(lint):
    "将无符号长整形转换为点分十进制 IP 地址形式"
    return socket.inet_ntoa(struct.pack("!I", lint))
    # 因为需要的是无符号的长整形数，所以，在转换时， struct.unpack() 和 struct.pack() 中使用的是 “!I” ，而不是直接使用 “I” ，这样实际上就已经做了 network byte 到 host
    # byte 之间的处理了。


# 检测是否有可用mysql连接
def close_old_connections():
    for conn in connections.all():
        conn.close_if_unusable_or_obsolete()


def strfdate(d):
    if d:
        return d.strftime('%Y-%m-%d')
    else:
        return ''


def strftime(t):
    if t:
        return t.strftime('%Y-%m-%d %H:%M')
    else:
        return ''


def strftime_m(t):
    if t:
        return t.strftime('%H:%M')
    else:
        return ''


def strftime_s(t):
    if t:
        return t.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return ''


def strptime_s(string):
    if string:
        return datetime.datetime.strptime(string, '%Y-%m-%d %H:%M:%S')
    else:
        return None


def strptime_d(string):
    if string:
        return datetime.datetime.strptime(string, '%Y-%m-%d')
    else:
        return None


def strfshorttime(t):
    if t:
        return t.strftime('%m-%d %H:%M')
    else:
        return ''


def read_file(fn, buf_size=262144):
    f = open(fn, "rb")
    while True:
        c = f.read(buf_size)
        if c:
            yield c
        else:
            break
    f.close()


def write_file(f, path, user=None):
    userstub = ''
    if user:
        userstub = '%d_' % user.id
    filename = "%s%s%s.%s" % (path, userstub, timezone.now().strftime('%Y%m%d%H%M%S%f'), f.name.split('.')[-1])
    filename = filename.lower()
    full_filename = "%s/%s" % (settings.MEDIA_ROOT, filename)
    with open(full_filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return filename, full_filename


def number2CNY(nin=None):
    def IIf(b, s1, s2):
        if b:
            return s1
        else:
            return s2

    cs = (
        u'零', u'壹', u'贰', u'叁', u'肆', u'伍', u'陆', u'柒', u'捌', u'玖', u'◇', u'分', u'角', u'圆', u'拾', u'佰',
        u'仟', u'万',
        u'拾',
        u'佰', u'仟', u'亿', u'拾', u'佰', u'仟', u'万')
    st = ''
    st1 = ''
    s = '%0.2f' % (nin)
    sln = len(s)
    if sln > 15:
        return None

    fg = (nin < 1)
    for i in range(0, sln - 3):
        ns = ord(s[sln - i - 4]) - ord('0')
        st = IIf((ns == 0) and (fg or (i == 8) or (i == 4) or (i == 0)), '',
                 cs[ns]) + IIf((ns == 0) and ((i != 8)
                                              and (i != 4)
                                              and (i != 0) or fg and (i == 0)
                                              ), '', cs[i + 13]) + st
        fg = (ns == 0)

    fg = False
    for i in [1, 2]:
        ns = ord(s[sln - i]) - ord('0')
        st1 = IIf((ns == 0) and ((i == 1) or (i == 2) and (fg or (nin < 1))), '', cs[ns]) + IIf((ns > 0), cs[i + 10],
                                                                                                IIf((i == 2) or fg, '',
                                                                                                    u'整')) + st1
        fg = (ns == 0)
    st.replace(u'亿万', u'万')
    return IIf(nin == 0, u'零', st + st1)


def add_month_interval(dt, inter):
    def _add_month_interval(dt, inter):
        m = dt.month + inter - 1
        y = int(dt.year + math.floor(m / 12))
        m = m % 12 + 1
        return y, m

    y, m = _add_month_interval(dt, inter)
    y2, m2 = _add_month_interval(dt, inter + 1)
    maxD = (datetime.date(y2, m2, 1) - datetime.timedelta(days=1)).day
    d = dt.day <= maxD and dt.day or maxD
    return datetime.date(y, m, d)


def format_money(n, sep=','):
    s = str(abs(n))[::-1]
    groups = []
    i = 0
    while i < len(s):
        groups.append(s[i:i + 3])
        i += 3
    retval = sep.join(groups)[::-1]
    if n < 0:
        return '-%s' % retval
    else:
        return retval


def strfsecond(second):
    sec = timedelta(seconds=second)
    d = datetime.datetime(1, 1, 1) + sec
    if d.hour > 0:
        if d.minute > 0:
            retval = "%d小时%d分钟" % (d.hour, d.minute)
        else:
            retval = "%d小时" % (d.hour)
    else:
        retval = "%d分钟" % (d.minute)
    return retval


def month_delta(x, y):
    """暂不考虑day, 只根据month和year计算相差月份
    Parameters
    ----------
    x, y: 两个datetime.datetime类型的变量

    Return
    ------
    differ: x, y相差的月份
    """
    month_differ = abs((x.year - y.year) * 12 + (x.month - y.month) * 1)
    return month_differ


def year_delta(x, y):
    months = month_delta(x, y)
    return months / 12


# 获取月的第一天和最后一天
def getMonthFirstDayAndLastDay(year=None, month=None):
    """
    :param year: 年份，默认是本年，可传int或str类型
    :param month: 月份，默认是本月，可传int或str类型
    :return: firstDay: 当月的第一天，datetime.date类型
              lastDay: 当月的最后一天，datetime.date类型
    """
    if year:
        year = int(year)
    else:
        year = datetime.date.today().year

    if month:
        month = int(month)
    else:
        month = datetime.date.today().month

    # 获取当月第一天的星期和当月的总天数
    firstDayWeekDay, monthRange = calendar.monthrange(year, month)

    # 获取当月的第一天
    firstDay = datetime.date(year=year, month=month, day=1)
    lastDay = datetime.date(year=year, month=month, day=monthRange)

    first_datetime = datetime.datetime(year, month, 1, 0, 0, 0)
    last_datetime = datetime.datetime(year, month, monthRange, 11, 59, 59)
    return firstDay, lastDay, first_datetime, last_datetime


# 获取当天最大、最小时间戳
def max_min_timestamp(nowdate):
    maxtime = datetime.datetime.combine(nowdate, datetime.time.max).timestamp()
    mintime = datetime.datetime.combine(nowdate, datetime.time.min).timestamp()
    return int(mintime), int(maxtime)


# 获取指定日期的周初，周末时间戳
def get_week_start_end_timestamp(today):
    oneday = datetime.timedelta(days=1)
    start_day = today
    end_day = today
    while start_day.weekday() != calendar.MONDAY:
        start_day -= oneday
    while end_day.weekday() != calendar.SUNDAY:
        end_day += oneday
    return max_min_timestamp(start_day)[0], max_min_timestamp(end_day)[1]


# 获取指定日期的月初，月末时间戳
def get_month_startend_timestamp(date):
    year, month = date.year, date.month
    days = calendar.monthrange(int(year), int(month))[1]
    start_date = datetime.datetime.strptime('%s-%s-01' % (year, month), '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime('%s-%s-%s' % (year, month, days), '%Y-%m-%d').date()
    return int(time.mktime(start_date.timetuple())), max_min_timestamp(end_date)[1]


# 获取指定日期的年初，年末时间戳
def get_year_startend_timestamp(date):
    year = date.year
    start_date = datetime.datetime.strptime('%s-01-01' % (year,), '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime('%s-12-31' % (year,), '%Y-%m-%d').date()
    return int(time.mktime(start_date.timetuple())), max_min_timestamp(end_date)[1]


# 获取指定日期的月初，月末日期
def get_month_start_and_end(date):
    year, month = date.year, date.month
    days = calendar.monthrange(int(year), int(month))[1]
    start_date = datetime.datetime.strptime('%s-%s-01' % (year, month), '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime('%s-%s-%s' % (year, month, days), '%Y-%m-%d').date()
    return start_date, end_date


# 获取上个月第一天的日期
def get_1st_of_last_month(today):
    year = today.year
    month = today.month
    if month == 1:
        month = 12
        year -= 1
    else:
        month -= 1
    res = datetime.datetime(year, month, 1)
    return res


# 获取两个日期之间的日期列表
def get_dates_between(start_date, end_date):
    dates = []
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date.strftime("%Y-%m-%d"))  # 将日期格式化为字符串并添加到列表中
        current_date += timedelta(days=1)  # 递增日期
    return dates


# 获取下个月第一天的日期
def get_1st_of_next_month(today):
    year = today.year
    month = today.month
    if month == 12:
        month = 1
        year += 1
    else:
        month += 1
    res = datetime.datetime(year, month, 1)
    return res


# 域名转换IP
def domain_to_ip(domain):
    import socket
    ip = None
    try:
        ip = socket.gethostbyname(domain)
    except:
        pass
    if ip:
        return True, ip

    try:
        result = socket.getaddrinfo(domain, None)
        ip = result[0][4][0]
    except:
        pass

    if ip:
        return True, ip

    return False, ip


# 获取就记录id
def get_row_id():
    # return base64.b64encode(str(int(time.time() * 1000))[::-1].encode()).decode().lower()
    return "".join(str(uuid.uuid1()).split('-')).lower()[:12] + "".join(
        random.sample("abcdefighijklmnopqrstuvwxyz0123456789", 4))


# user-agent生成器
def generate_user_agents(num_agents=10):
    user_agent_list = []

    for _ in range(num_agents):
        # 使用 fake_useragent 库生成随机的User-Agent
        user_agent = fake_useragent.UserAgent().random
        user_agent_list.append(user_agent)

    return user_agent_list

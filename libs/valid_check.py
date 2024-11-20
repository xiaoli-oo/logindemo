import re
import traceback

from django.db.models import Q
from libs.httpr import JSONError


def valid_username(username):
    """
        长度为3-20个字符
        可以包含英文，数字，.@+-_符号
    """
    if re.match('^[\w.@+-_]{3,20}$', username):
        return True
    return False


def valid_password(passwd):
    """
    password need 6-20 characters length, don't cotain empty space character
    """
    if re.match(r'^[\S]{6,20}$', passwd):
        return True
    return False


def valid_email(email):
    """
    valid emaill address is a valid address
    """
    if re.match("^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$", email):
        # if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email):
        return True
    return False


def valid_telephone(telephone):
    """
    valid telephone is a valid telephone
    """
    try:
        if re.match(r'^1[3456789]\d{9}$', telephone):
            return True
    except Exception:
        traceback.print_exc()
        return False
    return False


def valid_ip(ip):
    reip = re.compile("^((?:(2[0-4]\d)|(25[0-5])|([01]?\d\d?))\.){3}(?:(2[0-4]\d)|(255[0-5])|([01]?\d\d?))$")
    # reip = re.compile(r'(([12][0-9][0-9]|[1-9][0-9]|[1-9])/.){3,3}([12][0-9][0-9]|[1-9][0-9]|[1-9])')
    # for ip in reip.findall(ip):
    #    print "ip>>>", ip
    if re.match(reip, ip):
        return True
    else:
        return False


def valid_hanzi(string):
    # 验证是否是汉字
    hanzi = re.compile(u"[\u4e00-\u9fa5]{1,2}")
    if re.match(hanzi, string):
        return True
    else:
        return False


def valid_naturalnum(string):
    ziranshu = re.compile(u"[0-9]+")
    if re.match(ziranshu, string):
        return True
    else:
        return False


def valid_phone(phone):
    """
    valid phone is a valid phone
    """
    if re.match(
            r'^(\d{11})|^(\d{4,11})|(\d{4}|\d{3})-(\d{4,11})|(\d{4}|\d{3})-(\d{4,11})-(\d{4}|\d{3}|\d{2}|\d{1})|(\d{4,11})-(\d{4}|\d{3}|\d{2}|\d{1})$',
            phone):
        return True
    return False


def valid_boolean(b):
    try:
        if int(b) != 0 and int(b) != 1:
            return False
    except Exception as e:
        return False
    return True


def valid_mac(check):
    """
    valid QQ is a valid QQ
    """
    if re.match(r'(([A-F0-9]{2}:)|([A-F0-9]{2}-)){5}[A-F0-9]{2}', check):
        return True
    return False


def valid_int(check, start, end):
    try:
        list_int = [i for i in range(start, end)]
        if int(check) not in list_int:
            return False
    except Exception as e:
        return False
    return True

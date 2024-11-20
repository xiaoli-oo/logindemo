import json
import datetime
import urllib.request
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import exception_handler
from logindemo.config import AESKEY, AESIV
from libs.ENCAES import *


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)  # 获取本来应该返回的exception的response
    if response is not None:
        response.data['status_code'] = response.status_code
        response.data['message'] = response.data.get('detail', '')
        try:
            response.data['status'] = response.data['detail'].code
        except:
            pass
    return response


def JSONError(errors, error_code=1000):
    data = {
        "error_code": error_code,
        "data": {},
        "msg": errors,
        "errors": errors,
        'success': 0,
    }
    return JsonResponse(data)


def JSONAESError(errors, error_code=1000):
    data = {
        "error_code": error_code,
        "data": {},
        "msg": errors,
        "errors": errors,
        'success': 0,
    }

    utc_time_str = datetime.datetime.utcnow().replace(second=0, microsecond=0).strftime("%Y%m%d%H")
    data = aes_CBC_Encrypt(json.dumps(data), AESKEY+utc_time_str, AESIV)
    return JsonResponse({"data": data})


def JSONResponse(data, pager=None, msg=''):
    """

    :param data:
    :param pager:  {
        "page": page, 当前页
        "page_size": page_size, 每页多少数据
        "count": count，一共多少条数据
        "page_nums":page_nums 一共多少页
    }
    :param msg:
    :return:
    """

    data = {
        "error_code": 0,
        "data": data,
        "msg": msg,
        'success': 1,
    }
    if pager:
        data["pager"] = pager

    return JsonResponse(data)


def JSONAESResponse(data, pager=None, msg=''):
    # api对称加密

    data = {
        "error_code": 0,
        "data": data,
        "msg": msg,
        'success': 1,
    }
    if pager:
        data["pager"] = pager

    utc_time_str = datetime.datetime.utcnow().replace(second=0, microsecond=0).strftime("%Y%m%d%H")
    data = aes_CBC_Encrypt(json.dumps(data), AESKEY+utc_time_str, AESIV)
    return JsonResponse({"data": data})
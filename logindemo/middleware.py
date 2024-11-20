import re
import datetime
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import caches

from libs.httpr import JSONResponse, JSONError, JSONAESError
import traceback
import logging
import json

logger_error = logging.getLogger("api_error")
from libs.encrypt import analysis_jwttoken
from logindemo import config
from user.models import User
from libs.ENCAES import *
from libs import utils

from logindemo import config
from logindemo.config import WEB_URL
from libs.ENCAES import *

cache_user = caches['user']
cache_token = caches['token']
cache_api = caches['api']


class MyException(MiddlewareMixin):
    def process_exception(self, request, exception):
        api = request.get_full_path()
        logger_error.info("API: %s\n 异常信息:%s " % (api, exception))
        traceback.print_exc()
        return JSONError(exception.args[0])


class JwtAuthorizationMiddleware(MiddlewareMixin):
    """
    用户需要通过请求头的方式来进行传输token，例如：
    Authorization:jwt eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1NzM1NTU1NzksInVzZXJuYW1lIjoid3VwZWlxaSIsInVzZXJfaWQiOjF9.xj-7qSts6Yg5Ui55-aUOHJS4KSaeLq5weXMui2IIEJU
    """

    def process_request(self, request):
        # 防爬虫
        ip = utils.get_ip(request)
        # todo 增加ip合法验证, 如请求频繁等操作

        if not str(request.path_info).startswith(f'/api/'):
            return

        # 设置不需要验证token的url
        path_list = [
            '/api/user/login/wxxcx/',
            '/api/user/login/passwd/',
            '/api/user/login/vcode/',
            '/api/user/send/vcode/',
            '/',
        ]
        if request.path_info in path_list:
            return

        # 非登录页面需要校验token
        authorization = request.META.get('HTTP_AUTHORIZATION', '')
        auth = authorization.split()
        # 验证头信息的token信息是否合法
        if not auth:
            return JSONError('请先登录', error_code=1006)
        if auth[0].lower() != 'jwt':
            return JSONError('认证方式错误', error_code=1006)
        if len(auth) == 1 or len(auth) > 2:
            return JSONError('认证方式错误', error_code=1006)
        token = auth[1]

        # 解密
        result = analysis_jwttoken(token)
        if not result['status']:
            return JSONError(result['msg'], error_code=1004)
        payload = result['payload']
        uid = payload["uid"]
        username = payload["username"]
        client_type = payload["client_type"]

        tmp_token = cache_token.get('user-token-{0}-{1}'.format(uid, client_type))
        if tmp_token != token:
            return JSONError('您登录状态失效，请重新登录', error_code=1004)
        cache_token.set('user-token-{0}-{1}'.format(uid, client_type), token, config.USER_TOKEN_EXP)

        # 解析个人信息
        user_info = cache_user.get(uid)
        if not user_info:
            user_obj = User.objects.filter(id=uid, status__in=[1]).first()
            if not user_obj:
                return JSONError("账号无法使用", error_code=1003)
            user_info = user_obj.get_dict()
            cache_user.set(uid, user_info, config.COOKIE_AGE)
        if user_info.get('status') not in [1]:
            cache_user.delete(uid)
            return JSONError("账号无法使用", error_code=1003)

        # 将解密后数据赋值给user_info
        request.user_info = user_info
        request.session['uid'] = uid
        request.session['client_type'] = client_type


class DataDecryption(MiddlewareMixin):
    def process_request(self, request):
        # 只加密api
        if not str(request.path_info).startswith(f'/api/'):
            return

        data = request.POST.get("data")
        if not data:
            try:
                data = json.loads(request.body)['data']
            except Exception as e:
                print(e)

        if data:
            try:
                # 是否启用加密数据
                utc_time_str = datetime.datetime.utcnow().replace(second=0, microsecond=0).strftime("%Y%m%d%H")
                data = json.loads(aes_CBC_Decrypt(data, config.AESKEY + utc_time_str, config.AESIV))
                request.POST._mutable = True
                request.POST["data"] = data
                request.POST._mutable = False

            except Exception as e:
                return JSONAESError('请求被拒绝', error_code=1006)
        else:
            return JSONAESError('请求被拒绝', error_code=1006)

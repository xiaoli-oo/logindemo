import json
import math
import os
import time
import uuid
import requests
import random
from django.forms import model_to_dict
import datetime
from django.db.models import Q
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import caches
from libs.ENCAES import aes_CBC_Encrypt, aes_CBC_Decrypt
from libs.aliyun.OSS import OssServer
from libs.httpr import JSONResponse, JSONError
from libs.encrypt import create_jwttoken
from django.db.models import Sum
from logindemo.config import USER_TOKEN_EXP, V_CODE_TIMEOUT
from .models import User, SMSCodeLog, UserWX
from system.models import SerialNumberPool, ThirdPartyApps
from libs.weixin import wxxcx
from logindemo import config_ali
from libs import utils
from libs.sms import Sample
from logindemo import config, config_wx, settings

# Create your views here.
cache_token = caches['token']
cache_user = caches['user']

from user.tasks import add_login_log, add_op_log, add_sms_code_log, update_user_wx


@csrf_exempt
def login_passwd(request):
    try:
        username = request.POST.get('username')
        password = request.POST.get('password')
        client_type = request.POST['client_type']  # web, wx, app, zfb
    except:
        return JSONError("参数错误", error_code=1005)

    if client_type not in ('web', 'wx', 'app', 'zfb'):
        return JSONError("不支持的客户端类型")

    if not username or not password:
        return JSONError("请输入用户名或密码", error_code=1002)

    ip = utils.get_ip(request)

    user_obj = User.objects.filter(username=username).first()
    if not user_obj or not check_password(password, user_obj.password):
        add_login_log(ip, "账号{0}或密码{1}错误".format(username, password), user_obj.id, 0, 1, client_type)
        return JSONError("账号或密码错误", error_code=1002)

    if user_obj.status != 1:
        add_login_log(ip, "账号被禁用status{0}".format(user_obj.status), user_obj.id, 0, 1, client_type)
        return JSONError("账号无法使用")

    user_obj.last_login_time = timezone.now()
    user_obj.last_ip = ip
    user_obj.save(using="db_write")

    # 构造payload exp务必选择UTC时间
    payload = {
        'uid': user_obj.id,
        'username': user_obj.username,
        'client_type': client_type,
    }
    token = create_jwttoken(payload)
    data = user_obj.get_dict()
    data['token'] = token
    cache_token.set('user-token-{0}-{1}'.format(user_obj.id, client_type), token, USER_TOKEN_EXP)
    add_login_log(ip, "登录成功", user_obj.id, 1, 1, client_type)

    return JSONResponse(data, msg="成功")


@csrf_exempt
def send_vcode(request):
    try:
        data = request.POST['data']
        type = int(data.get('type', '1'))  # 类型 1手机, 2电子邮箱
        code_type = int(data.get('code_type', 1))  # 类型 1注册/登录, 2变更信息, 3认证, 4其他
        country_code = data.get('country_code', 'CN')
        phone = data.get('phone')
        email = data.get('email', "wx")  # web, wx, app
    except:
        return JSONError("参数错误", error_code=1005)

    if type == 1 and phone:

        phone = phone.replace(' ', '').replace('-', '')

        if cache_user.get('v_code_{0}'.format(phone)):
            return JSONError("您的验证码还在{0}分钟内，可以正常使用".format(int(V_CODE_TIMEOUT / 60)))
        v_code = random.randint(100000, 999999)
        try:
            result = Sample.main(phone, v_code, config_ali.SMS_CODE)
        except:
            return JSONError("短信发送失败")

        if not result[0]:
            add_sms_code_log(type, phone, v_code, code_type, 0, V_CODE_TIMEOUT, None, result[1])
            return JSONError(result[1])
        cache_user.set('v_code_{0}'.format(phone), v_code, V_CODE_TIMEOUT)
        add_sms_code_log(type, phone, v_code, code_type, 1, V_CODE_TIMEOUT)
        return JSONResponse({}, msg="已发送")
    elif type == 2 and email:
        email = email.replace(' ', '')
        return JSONError("暂不支持的类型")

    else:
        return JSONError("不支持的类型")


@csrf_exempt
def send2_vcode(request):
    user_info = request.user_info
    uid = user_info['uid']

    try:
        data = request.POST['data']
        type = int(data.get('type', '1'))  # 类型 1手机, 2电子邮箱
        code_type = int(data.get('code_type'))  # 类型 1注册/登录, 2变更信息, 3认证, 4其他
        country_code = user_info.get('country_code', 'CN')
        phone = user_info.get('phone')
        email = user_info.get('email')  # web, wx, app
    except:
        return JSONError("参数错误", error_code=1005)

    if type == 1 and phone:
        phone = phone.replace(' ', '').replace('-', '')
        if cache_user.get('v_code_{0}'.format(phone)):
            return JSONError("您的验证码还在{0}分钟内，可以正常使用".format(int(V_CODE_TIMEOUT / 60)))
        v_code = random.randint(100000, 999999)
        try:

            result = Sample.main(phone, v_code, config_ali.SMS_CODE)
        except:
            return JSONError("发送短信失败")
        if not result[0]:
            add_sms_code_log(type, phone, v_code, code_type, 0, V_CODE_TIMEOUT, None, result[1])
            return JSONError(result[1])
        cache_user.set('v_code_{0}'.format(phone), v_code, V_CODE_TIMEOUT)
        add_sms_code_log(type, phone, v_code, code_type, 1, V_CODE_TIMEOUT)
        return JSONResponse({}, msg="已发送")

    elif type == 2 and email:
        email = email.replace(' ', '')
        return JSONError("暂不支持的类型")

    elif type == 1 and not phone:
        return JSONError("请先绑定手机号！")

    else:
        return JSONError("不支持的类型")


@csrf_exempt
def login_vcode(request):
    try:
        data = request.POST['data']
        phone = data['phone']
        v_code = data['v_code']
        phone = phone.replace(' ', '').replace('-', '')
        v_code = int(v_code.replace(' ', '').replace('-', ''))
        client_type = data['client_type']  # web, wx, app
    except:
        return JSONError("参数错误", error_code=1005)

    tmp_v_code = cache_user.get('v_code_{0}'.format(phone))
    if v_code != tmp_v_code:
        return JSONError("验证码错误", error_code=1003)

    ip = utils.get_ip(request)

    user_obj = User.objects.filter(phone=phone).first()
    if not user_obj:
        uid = SerialNumberPool.objects.get(name='用户uid').generate_serial()
        user_obj = User.objects.using('db_write').create(
            id=uid,
            phone=phone,
            username=phone,
            last_login_time=timezone.now(),
            last_ip=ip,
            status=1
        )
    else:
        if user_obj.status != 1:
            add_login_log(ip, "账号被禁用status{0}".format(user_obj.status), user_obj.id, 0, 2, client_type)
            return JSONError("账号无法使用")
        user_obj.last_login_time = timezone.now()
        user_obj.last_ip = ip
        user_obj.save(using="db_write")

    # 构造payload exp务必选择UTC时间
    payload = {
        'uid': user_obj.id,
        'username': user_obj.username,
        'client_type': client_type,
    }
    token = create_jwttoken(payload)
    data = user_obj.get_dict()
    data['token'] = token
    cache_token.set('user-token-{0}-{1}'.format(user_obj.id, client_type), token, USER_TOKEN_EXP)
    cache_user.delete('v_code_{0}'.format(phone))
    add_login_log(ip, "登录成功", user_obj.id, 1, 2, client_type)

    return JSONResponse(data, msg="成功")


@csrf_exempt
def login_wxxcx(request):
    try:
        data = request.POST['data']
        js_code = data['code']  # 登录时获取的 code
        ip = utils.get_ip(request)
        language = data.get('language', 'zh-CN')
        client_type = data['client_type']  # web, wx, app
        nickname = data.get('nickname', '')
        gender = data.get('gender', 0)  # 0未知 1为男  2为女
        # head_img = request.FILES.get('head_img')
        head_img_url = data.get('head_img_url')
        reference = data.get("reference")
    except:
        return JSONError("参数错误", error_code=1005)

    t_app_obj = ThirdPartyApps.objects.filter(name="登录demo", type='WXXCX', status__in=[1, 2]).first()
    if not t_app_obj:
        return JSONError(u"微信小程序APPID不存在")

    wx_xcx = wxxcx.WeChatXCXLogin(t_app_obj.appid, t_app_obj.secret)
    code, result = wx_xcx.code2Session(js_code)
    if not code:
        return JSONError(result)

    openid = result.get('openid')
    session_key = result.get('session_key', '')
    unionid = result.get('unionid', '')
    user_wx_info = {"head_img": head_img_url, "nickname": nickname, "open_id": openid, "union_id": unionid,
                    "session_key": session_key}

    if not unionid and not openid:
        return JSONError('openid或unionid获取失败')

    if unionid:
        user_wx_obj = UserWX.objects.filter(union_id=unionid).first()
    elif openid:
        user_wx_obj = UserWX.objects.filter(open_id=openid).first()
    else:
        return JSONError('openid或unionid获取失败')

    if not user_wx_obj:  # 新用户
        uid = SerialNumberPool.objects.get(name='用户uid').generate_serial()
        user_obj = User.objects.using('db_write').create(
            id=uid,
            role='customer',
            last_login_time=timezone.now(),
            last_ip=ip,
            status=1,
            sex=gender,
            nickname=nickname,
            head_img=head_img_url,
        )
    else:  # 登录用户
        user_obj = user_wx_obj.uid

        if user_obj.status != 1:
            add_login_log(ip, "账号被禁用status{0}".format(user_obj.status), user_obj.id, 0, 3, client_type)
            return JSONError("账号无法使用", error_code=1003)
        user_obj.last_login_time = timezone.now()
        user_obj.last_ip = ip
        if not user_obj.nickname:
            user_obj.nickname = nickname
        if not user_obj.sex:
            user_obj.sex = gender
        if not user_obj.head_img:
            user_obj.head_img = head_img_url
        user_obj.save(using="db_write")

    # 构造payload exp务必选择UTC时间
    payload = {
        'uid': user_obj.id,
        'username': user_obj.username or "",
        'client_type': client_type,
    }
    token = create_jwttoken(payload)
    data = user_obj.get_dict()
    data['user_wx_info'] = user_wx_info
    data['token'] = token
    cache_token.set('user-token-{0}-{1}'.format(user_obj.id, client_type), token, USER_TOKEN_EXP)
    update_user_wx(user_obj.id, t_app_obj.id, user_wx_info, reference)
    add_login_log(ip, "微信小程序登录成功", user_obj.id, 1, 3, client_type)

    return JSONResponse(data, msg="成功")


@csrf_exempt
def logout(request):
    uid = request.session.get('uid')
    client_type = request.session.get('client_type')
    last_token = cache_token.get('user-token-{0}-{1}'.format(uid, client_type))
    cache_token.delete('user-token-{0}-{1}'.format(uid, client_type))
    cache_token.delete(last_token)
    cache_user.delete(uid)
    request.session.clear()

    return JSONResponse({})


@csrf_exempt
def set_phone(request):
    try:
        data = request.POST['data']
        type = int(data['type'])  # 1绑定2修改
        phone = data['phone']
        v_code = data['v_code']
        phone = phone.replace(' ', '').replace('-', '')
        v_code = int(v_code.replace(' ', '').replace('-', ''))
        paypwd = data['paypwd']
    except:
        return JSONError("参数错误", error_code=1005)

    user_info = request.user_info
    uid = user_info['uid']

    user_obj = User.objects.using('db_write').filter(id=uid, status__gte=0).first()
    if user_obj.status < 1:
        return JSONError("账号已被禁用")

    if type not in (1, 2):
        return JSONError("操作类型不支持")
    if type == 1 and user_info.get('phone'):
        return JSONError("手机号已经绑定，请勿重复操作")
    if type == 2 and not user_info.get('has_pay_pwd'):
        return JSONError("请先设置支付密码！")
    if type == 2 and not check_password(paypwd, user_obj.pay_pwd):
        return JSONError("支付密码错误！")

    old_phone = user_info.get('phone')

    tmp_v_code = cache_user.get('v_code_{0}'.format(phone))
    if v_code != tmp_v_code:
        return JSONError("验证码错误", error_code=1003)

    user_obj.phone = phone
    user_obj.save()
    data = user_obj.get_dict()

    cache_user.delete(uid)
    add_op_log(utils.get_ip(request), "设置手机号", user_obj.id, 1, 'update',
               {'tb_name': 'user', 'tb_desc': '设置手机号', 'tb_id': user_obj.id,
                'tb_befor': old_phone, 'tb_after': phone})

    return JSONResponse(data, msg="成功")


@csrf_exempt
def myinfo(request):
    user_info = request.user_info
    uid = user_info['uid']

    user_obj = User.objects.filter(id=uid).first()
    if not user_obj:
        return JSONError('用户不存在')

    data = user_obj.get_dict()
    cache_user.set(uid, user_info, config.COOKIE_AGE)
    return JSONResponse(data, msg="成功")

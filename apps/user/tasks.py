from __future__ import absolute_import, unicode_literals
import json
from django.db.models import Q
from django.utils import timezone
from django_q.tasks import async_task, Task, result
from django_q.tasks import schedule, Schedule

# 增加登陆日志
def add_login_log(ip, remark, uid=0, status=0, login_type=None, client_type=None, token=None):
    from user.models import UserLoginLog
    login_log = UserLoginLog()
    login_log.uid = uid
    login_log.login_type = login_type
    login_log.client_type = client_type
    login_log.ip = ip
    login_log.status = status
    login_log.remark = remark
    login_log.token = token
    login_log.save(using="db_write")
    return login_log.id


# 增加操作日志
async def add_op_log(ip, remark, uid=0, status=0, action='other', tb_dict=None):
    if tb_dict is None:
        tb_dict = {}
    from user.models import UserOpLog
    op_log = UserOpLog()

    op_log.uid = uid
    op_log.ip = ip
    op_log.action_type = action
    op_log.remark = remark
    op_log.status = status
    op_log.tb_name = tb_dict.get('tb_name')
    op_log.tb_desc = tb_dict.get('tb_desc')
    op_log.tb_id = tb_dict.get('tb_id')
    op_log.tb_befor = tb_dict.get('tb_befor')
    op_log.tb_after = tb_dict.get('tb_after')
    op_log.save(using="db_write")
    return op_log.id


# 增加验证码日志
async def add_sms_code_log(type, rec_number, code, code_type, status, effective_time, uid=None, remark=None):
    from user.models import SMSCodeLog
    op_log = SMSCodeLog.objects.using("db_write").create(
        type=type,
        rec_number=rec_number,
        code=code,
        code_type=code_type,
        uid=uid,
        effective_time=effective_time,
        remark=remark,
        status=status
    )
    return op_log.id


def update_user_wx(uid, third_apps_id, data, reference=None):
    from user.models import UserWX

    if data.get('union_id'):
        user_wx_obj = UserWX.objects.filter(third_apps_id=third_apps_id, union_id=data.get('union_id')).first()
    elif data.get('open_id'):
        user_wx_obj = UserWX.objects.filter(third_apps_id=third_apps_id, open_id=data.get('open_id')).first()

    if not user_wx_obj:
        UserWX.objects.using('db_write').create(
            uid_id=uid,
            third_apps_id=third_apps_id,
            head_img=data.get('head_img'),
            nickname=data.get('nickname'),
            open_id=data.get('open_id'),
            union_id=data.get('union_id'),
            session_key=data.get('session_key'),
            access_token=data.get('access_token'),
            refresh_token=data.get('refresh_token'),
            reference=reference
        )
    else:
        user_wx_obj.head_img = data.get('headimgurl')
        user_wx_obj.nickname = data.get('nickname')
        user_wx_obj.access_token = data.get('access_token')
        user_wx_obj.refresh_token = data.get('refresh_token')
        user_wx_obj.save(using="db_write")

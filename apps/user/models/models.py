import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from libs import valid_error
from system.models import Country, Address, SerialNumberPool, ThirdPartyApps


class User(models.Model):
    STATUE_CHIOCE = (
        (-1, "删除"),
        (0, "禁用"),
        (1, "正常"))

    ROLE = [
        ('customer', '消费者'),
        ('agent', '商家'),
    ]

    id = models.CharField(verbose_name=u'UID', max_length=32, unique=True, editable=False, primary_key=True)
    role = models.CharField(verbose_name='角色', null=True, max_length=25, choices=ROLE)

    created_at = models.DateTimeField(verbose_name=u'创建时间', null=False, auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(verbose_name=u'更新时间', null=False, auto_now=True, editable=False,
                                      db_index=True)
    nickname = models.CharField(verbose_name='昵称', max_length=50, blank=True, null=True)

    username = models.CharField(verbose_name='账号', max_length=50, unique=True, null=True, blank=True,
                                validators=[valid_error.valid_username], db_index=True)
    password = models.CharField(verbose_name=u'密码', max_length=256, null=True, blank=True)

    name = models.CharField(verbose_name='真实姓名', max_length=20, blank=True, null=True)
    sex = models.SmallIntegerField(default=0, choices=((2, "女"), (1, "男"), (0, "待定")), verbose_name="性别")
    email = models.EmailField(verbose_name='电子邮箱', blank=True, null=True)
    head_img = models.CharField(verbose_name='头像', max_length=150, null=True)

    phone_code = models.CharField(max_length=15, null=True, default='+86')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="电话", db_index=True)
    idcard = models.CharField(max_length=20, blank=True, null=True, verbose_name="身份证号码", unique=True)
    country = models.ForeignKey(verbose_name="国家", to=Country, null=True, on_delete=models.DO_NOTHING)

    last_login_time = models.DateTimeField(verbose_name=u'登录时间', blank=True, null=True, editable=False)
    join_time = models.DateTimeField(verbose_name=u'注册时间', default=timezone.now)
    last_ip = models.GenericIPAddressField(blank=True, null=True, verbose_name="最后登录IP", editable=False)
    is_staff = models.BooleanField(verbose_name=u'内部员工', null=False, default=False)

    status = models.SmallIntegerField(default=1, choices=STATUE_CHIOCE, verbose_name='状态')
    real_person_certification = models.BooleanField(default=0, verbose_name="是否实人认证")
    pay_pwd = models.CharField(verbose_name='交易密码', max_length=6, null=True)
    objects = models.Manager()

    def __str__(self):
        return '[%s]%s' % (self.id, self.username or self.nickname)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = SerialNumberPool.objects.get(name='用户uid').generate_serial()
        super(User, self).save(*args, **kwargs)

    def set_password(self, raw_password):
        return make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def get_detail_dict(self):
        bind_wx = {}
        user_wx_obj = self.bind_wx.filter(third_apps__type__icontains=['WXAPP', 'WXXCX']).first()
        if user_wx_obj:
            bind_wx = {
                'head_img': user_wx_obj.head_img,
                'nickname': user_wx_obj.nickname
            }

        data = {
            'uid': self.id,
            'username': self.username,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'country_code': self.country.code2 if self.country else 'CN',
            'idcard': self.idcard,
            'sex': self.sex,
            'last_ip': self.last_ip,
            'last_login_time': self.last_login_time,
            'is_staff': self.is_staff,
            'status': self.status,
            'pay_pwd': self.pay_pwd,
            'bind_wx': bind_wx,
        }
        return data

    def get_dict(self):
        user_wx_info = {}
        user_wx_obj = self.bind_wx.filter(third_apps__type__icontains=['WXAPP', 'WXXCX']).first()
        if user_wx_obj:
            user_wx_info = {
                'head_img': user_wx_obj.head_img,
                'nickname': user_wx_obj.nickname
            }

        data = {
            'uid': self.id,
            'username': self.username or '',
            "name": self.name[0] + "*" + self.name[-1] if self.name else "",
            'idcard': str(self.idcard)[0:5] + "*" * 8 + str(self.idcard)[-4:] if self.idcard else "",
            'phone': str(self.phone)[0:3] + "*" * 4 + str(self.phone)[-4:] if self.phone else "",
            'sex': self.sex,
            'has_pay_pwd': True if self.pay_pwd else False,
            'user_wx_info': user_wx_info,
            'last_login_time': self.last_login_time,
            'status': self.status,
        }
        return data

    class Meta:
        ordering = ['id']
        verbose_name = u"用户"
        verbose_name_plural = verbose_name


class UserWX(models.Model):
    uid = models.ForeignKey(verbose_name='用户id', to=User, db_index=True, on_delete=models.CASCADE,
                            related_name='bind_wx')
    third_apps = models.ForeignKey(verbose_name="应用id", to=ThirdPartyApps, null=True, on_delete=models.PROTECT)
    reference = models.CharField(verbose_name="推荐人id", max_length=25, null=True)
    head_img = models.CharField(verbose_name='微信头像', max_length=150, null=True)
    nickname = models.CharField(verbose_name='微信昵称', max_length=50, blank=True, null=True)

    open_id = models.CharField(verbose_name="openid", max_length=50, db_index=True, null=True)
    union_id = models.CharField(verbose_name="unionid", max_length=50, db_index=True, null=True)
    session_key = models.CharField(verbose_name="session_key", max_length=50, db_index=True, null=True)

    access_token = models.CharField(verbose_name='access_token', max_length=150, null=True)
    refresh_token = models.CharField(verbose_name='refresh_token', max_length=150, null=True)

    created_at = models.DateTimeField(verbose_name=u'创建时间', null=False, auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(verbose_name=u'更新时间', null=False, auto_now=True, editable=False,
                                      db_index=True)
    objects = models.Manager()

    def __str__(self):
        return '%s' % (self.open_id)

    def get_detail_dict(self):
        data = {
            'id': self.id,
            "uid": self.uid,
            "third_apps": self.third_apps,
            "head_img": self.head_img,
            "nickname": self.nickname,
            "open_id": self.open_id,
            "union_id": self.union_id,
            "session_key": self.session_key,
            "access_token": self.access_token,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
        return data

    def get_dict(self):
        data = {
            'id': self.id,
            "uid": self.uid,
            "third_apps": self.third_apps.name if self.third_apps else '',
            "third_apps_appid": self.third_apps.appid if self.third_apps else '',
            "head_img": self.head_img,
            "nickname": self.nickname,
            "open_id": self.open_id,
            "union_id": self.union_id
        }
        return data

    class Meta:
        verbose_name = u"用户微信"
        verbose_name_plural = verbose_name


class UserAddress(models.Model):
    STATUS = [
        (0, '删除'),
        (1, '正常')
    ]

    uid = models.ForeignKey(verbose_name=u'UID', to=User, max_length=32, db_index=True, on_delete=models.PROTECT)

    name = models.CharField(verbose_name='收件人姓名', max_length=50)
    phone = models.CharField(verbose_name='收件人电话', max_length=15)
    country = models.ForeignKey(verbose_name="国家", to=Country, null=True, on_delete=models.PROTECT)
    address = models.ForeignKey(verbose_name="地址", to=Address, on_delete=models.PROTECT,
                                help_text="点击放大镜选择地址")
    detail_address = models.CharField(verbose_name="详细地址", max_length=225)
    zipcode = models.CharField(verbose_name='邮政编码', null=True, max_length=50)

    is_default = models.BooleanField(verbose_name='是否默认地址', default=False, db_index=True)
    sort = models.PositiveIntegerField(verbose_name='排序', default=5, db_index=True)
    status = models.PositiveSmallIntegerField(verbose_name='状态', default=1, db_index=True, choices=STATUS)

    created_at = models.DateTimeField(verbose_name=u'创建时间', null=False, auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(verbose_name=u'更新时间', null=False, auto_now=True, editable=False,
                                      db_index=True)
    objects = models.Manager()

    def __str__(self):
        return '[%s]%s' % (self.uid, self.city or '')

    def get_detail_dict(self):
        data = {
            'id': self.id,
            "uid": self.uid,
            "name": self.name,
            "phone": self.phone,
            "country": self.country.code2 if self.country else '',
            "state": self.state,
            "city": self.city,
            "county": self.county,
            "detail_address": self.detail_address,
            "is_default": self.is_default,
            "sort": self.sort,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
        return data

    def get_dict(self):
        data = {
            'id': self.id,
            "uid": self.uid,
            "name": self.name[0] + "*" + self.name[-1] if self.name else "",
            'phone': str(self.phone)[0:3] + "*" * 4 + str(self.phone)[-4:] if self.phone else "",
            "country": self.country.code2 if self.country else '',
            "state": self.state,
            "city": self.city,
            "county": self.county,
            "detail_address": self.detail_address,
            "is_default": self.is_default,
            "sort": self.sort,
            "status": self.status,
        }
        return data

    class Meta:
        verbose_name = u"用户地址"
        verbose_name_plural = verbose_name

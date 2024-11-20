import json
import datetime
from django.db import models
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field


# Create your models here.

# Create your models here.
class Country(models.Model):
    code2 = models.CharField(max_length=150, verbose_name='2字母代码', null=False, blank=False, primary_key=True)

    name = models.CharField(max_length=50, verbose_name='名称', null=True, blank=True, db_index=True)
    cn_name = models.CharField(max_length=150, verbose_name='中文名称', null=True, blank=True)
    flag = models.CharField(max_length=150, verbose_name='国旗', null=True, blank=True)
    local_name = models.CharField(max_length=250, verbose_name='本地名称', null=True, blank=True)
    code3 = models.CharField(max_length=150, verbose_name='3字母代码', null=True, blank=True)
    lang_code = models.CharField(max_length=50, verbose_name='官方语言代码', null=True, blank=True, db_index=True)
    language = models.CharField(max_length=150, verbose_name='官方语言', null=True, blank=True)
    continents = models.CharField(max_length=150, verbose_name='归属洲', null=True, blank=True)
    phone_code = models.CharField(max_length=150, verbose_name='国际电话区号', null=True, blank=True)

    objects = models.Manager()

    def get_dict(self):
        data = {
            "name": self.name,
            "cn_name": self.cn_name,
            "flag": self.flag,
            "local_name": self.local_name,
            "code3": self.code3,
            "code2": self.code2,
            "language": self.language,
            "continents": self.continents,
            "phone_code": self.phone_code,
            "lang_code": self.lang_code,
        }
        return data

    def __str__(self):
        return f"{self.code2} / {self.name or self.local_name} / {self.cn_name}"

    class Meta:
        ordering = ['code2']
        verbose_name = '国家'
        verbose_name_plural = verbose_name


class Address(models.Model):
    country = models.ForeignKey(verbose_name="国家", to=Country, on_delete=models.CASCADE, related_name='address',
                                db_index=True)
    code = models.CharField(verbose_name="编码", max_length=15, db_index=True, null=True, blank=True)
    province = models.CharField(verbose_name="省", max_length=50, db_index=True)
    city = models.CharField(verbose_name="市", max_length=50, db_index=True, null=True, blank=True)
    district = models.CharField(verbose_name="区/县", max_length=50, db_index=True, null=True, blank=True)

    class Meta:
        unique_together = ('country', 'province', 'city', 'district')
        ordering = ['code']
        verbose_name = u'省/市/区'
        verbose_name_plural = verbose_name

    def __str__(self):
        str_name = f"[{self.country.local_name}]"
        if self.province:
            str_name += f"{self.province}"
        if self.city and self.city != '市辖区':
            str_name += f"/{self.city}"
        if self.district:
            str_name += f"/{self.district}"

        return str_name


class SystemParam(models.Model):
    VALUE_TYPE = (
        ('int', u'整数'),
        ('float', u'浮点型'),
        ('str', u'字符串'),
        ('json', u'JSON'),
    )

    name = models.CharField(max_length=50, db_index=True, verbose_name='参数名称')
    key = models.CharField(max_length=50, db_index=True, verbose_name='键')
    value = models.CharField(max_length=150, verbose_name='值')
    value_type = models.CharField(verbose_name=u'值类型', default='str', max_length=15, choices=VALUE_TYPE)
    created_at = models.DateTimeField(verbose_name=u'创建时间', null=True, auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(verbose_name=u'编辑时间', null=True, auto_now=True, editable=False)
    note = models.CharField(verbose_name="备注", null=True, blank=True, max_length=225)
    status = models.BooleanField(verbose_name=u'状态', default=True, db_index=True)
    lock_status = models.BooleanField(verbose_name=u'锁定状态', default=False, db_index=True)

    objects = models.Manager()

    def get_dict(self):
        value = self.value
        if self.value_type == 'int':
            value = int(self.value)
        elif self.value_type == 'float':
            value = float(self.value)
        elif self.value_type == 'json':
            value = json.loads(self.value)
        data = {
            'key': self.key,
            'name': self.name,
            'value': value,
            'value_type': self.value_type,
            'value_type_name': self.get_value_type_display(),
            'created_at': datetime.datetime.strftime(self.created_at, '%Y-%m-%d %H:%M:%S'),
            'updated_at': datetime.datetime.strftime(self.updated_at, '%Y-%m-%d %H:%M:%S'),
            'status': self.status,
            'lock_status': self.lock_status,
        }
        return data

    def get_simple_dict(self):
        value = self.value
        if self.value_type == 'int':
            value = int(self.value)
        elif self.value_type == 'float':
            value = float(self.value)
        elif self.value_type == 'json':
            value = json.loads(self.value)
        data = {
            'key': self.key,
            'name': self.name,
            'value': value,
            'value_type': self.value_type,
            'status': self.status,
            'lock_status': self.lock_status,
        }
        return data

    def get_value(self, key):
        param = SystemParam.objects.filter(key=key, status=True).first()
        if param:
            return param.get_dict()["value"]
        else:
            return None

    def __str__(self):
        return "参数:{0}".format(self.name)

    class Meta:
        verbose_name = u'系统参数'
        unique_together = [('name', 'key')]
        ordering = ['name', 'key']
        verbose_name_plural = verbose_name


class SerialNumberPool(models.Model):
    name = models.CharField(verbose_name="序列号池名称", max_length=50, unique=True)  # 序列号池名称
    description = models.CharField(verbose_name="序列号池描述", blank=True, null=True, max_length=225)  # 序列号池描述
    prefix = models.CharField(verbose_name="序列号前缀", max_length=10, blank=True)  # 序列号前缀，可选
    suffix = models.CharField(verbose_name="序列号后缀", max_length=10, blank=True)  # 序列号后缀，可选
    year = models.BooleanField(verbose_name="年", default=False)
    month = models.BooleanField(verbose_name="月", default=False)
    day = models.BooleanField(verbose_name="日", default=False)
    digit = models.PositiveSmallIntegerField(verbose_name="位数", default=5)
    step = models.PositiveIntegerField(verbose_name="序列号步长", default=1)  # 序列号步长
    next_number = models.PositiveIntegerField(verbose_name="下一个序列号的数字部分", default=1)  # 下一个序列号的数字部分

    def __str__(self):
        return self.name

    def generate_serial(self):
        """生成下一个序列号"""
        date_str = ''
        if self.year:
            date_str += timezone.now().strftime('%Y')
        if self.month:
            date_str += timezone.now().strftime('%m')
        if self.day:
            date_str += timezone.now().strftime('%d')

        number_str = str(self.next_number).zfill(self.digit)
        serial_number = f"{self.prefix or ''}{date_str}{number_str}{self.suffix or ''}"

        self.next_number += self.step
        self.save()
        return serial_number

    class Meta:
        verbose_name = "序列号池"
        verbose_name_plural = "序列号池"

    # # 创建一个序列号池，步长为 10
    # product_serial_pool = SerialNumberPool.objects.create(
    #     name='Product Serial Numbers',
    #     description='Serial numbers for products',
    #     prefix='PROD-',
    #     suffix='',
    #     next_number=1,
    #     step=10
    # )


class ThirdPartyApps(models.Model):
    TYPE = [
        ('WXH5', '微信H5'),
        ('WXXCX', '微信小程序'),
        ('WXAPP', '移动应用APP'),
        ('WXDYH', '微信订阅号'),
        ('WXFWH', '微信服务号'),
        ('ZFBXCX', '支付宝小程序'),
        ('DYXCX', '抖音小程序'),
        ('QQ', 'QQ'),
        ('YSFXCX', '云闪付小程序'),
        ('WXZF', '微信支付'),
        ('QYWX', '企业微信'),
    ]

    STATUS = [
        (0, '禁用'),
        (1, '测试'),
        (2, '正式'),
    ]

    name = models.CharField(verbose_name="应用名称", max_length=150)
    type = models.CharField(verbose_name="应用类型", max_length=15, choices=TYPE)

    mchid = models.CharField(verbose_name="商户id", max_length=150, null=True, blank=True)
    appid = models.CharField(verbose_name="Appid", max_length=50, db_index=True, unique=True)
    original_id = models.CharField(verbose_name='原始id', max_length=150, null=True, blank=True)
    secret = models.CharField(verbose_name="Secret", max_length=150, null=True, blank=True)
    public_key = models.CharField(verbose_name="公钥", max_length=150, null=True, blank=True)

    qrcode = models.ImageField(verbose_name="二维码", max_length=225, null=True, upload_to="apps/", blank=True)

    company = models.CharField(verbose_name="应用所属公司", max_length=150, null=True, blank=True)

    qywx_token = models.CharField(verbose_name="企业微信应用token", max_length=150, null=True, blank=True)
    qywx_aeskey = models.CharField(verbose_name="企业微信应用aeskey", max_length=150, null=True, blank=True)
    qywx_agent_id = models.CharField(verbose_name="企业微信应用id", max_length=150, null=True, blank=True)
    qywx_agent_secret = models.CharField(verbose_name="企业微信应用密钥", max_length=150, null=True, blank=True)
    qywx_agent_name = models.CharField(verbose_name="企业微信应用名称", max_length=150, null=True, blank=True)

    notyfy_url = models.URLField(verbose_name="回调地址", null=True, blank=True)

    welcome = models.CharField(verbose_name="企业微信应用欢迎语", max_length=150, null=True, blank=True)

    created_at = models.DateTimeField(verbose_name=u'创建时间', null=False, auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(verbose_name=u'更新时间', null=False, auto_now=True, editable=False,
                                      db_index=True)
    status = models.PositiveSmallIntegerField(verbose_name="状态", db_index=True, default=1, choices=STATUS)

    def __str__(self):
        return "[{0}]{1}".format(self.get_type_display(), self.name)

    class Meta:
        unique_together = [('name', 'type')]
        verbose_name = u'第三方应用配置'
        verbose_name_plural = verbose_name

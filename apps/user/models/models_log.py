from django.db import models
from django.utils import timezone


class UserLoginLog(models.Model):
    LOGIN_TYPE = (
        (1, u'密码'),
        (2, u'手机短信'),
        (3, u'微信'),
        (4, u'支付宝'),
    )

    CLIENT_TYPE = (
        ('web', u'web端'),
        ('wx', u'微信'),
        ('app', u'app'),
        ('zfb', u'支付宝'),
    )

    uid = models.CharField(verbose_name=u'UID', max_length=32, db_index=True)
    login_type = models.SmallIntegerField(verbose_name=u'登录类型', default=1, choices=LOGIN_TYPE)
    client_type = models.CharField(verbose_name=u'客户端类型', null=True, choices=CLIENT_TYPE, max_length=15)

    ip = models.CharField(max_length=50, blank=True, null=True, verbose_name='IP')
    lon = models.FloatField(verbose_name=u"经度", default=0.0)
    lat = models.FloatField(verbose_name=u"维度", default=0.0)
    address = models.CharField(max_length=225, verbose_name='地址', blank=True, null=True)
    status = models.BooleanField(default=True, verbose_name='状态')
    remark = models.CharField(max_length=50, blank=True, null=True, verbose_name='备注')

    token = models.CharField(verbose_name=u'token串', null=True, max_length=255)

    created_at = models.DateTimeField(default=timezone.now, verbose_name="创建时间", db_index=True)

    objects = models.Manager()

    def __str__(self):
        return "uid：%s" % self.uid

    class Meta:
        ordering = ['-id']
        verbose_name = '用户登录日志'
        verbose_name_plural = verbose_name


class UserOpLog(models.Model):
    CODE_CHOICES = (
        ('read', '读'),
        ('add', '增'),
        ('update', '改'),
        ('delete', '删'),
        ('other', '其他'),
    )

    uid = models.CharField(verbose_name=u'UID', max_length=32, db_index=True)

    ip = models.CharField(max_length=50, blank=True, null=True, verbose_name='IP')
    action_type = models.CharField(max_length=32, choices=CODE_CHOICES, verbose_name="操作类型")
    remark = models.CharField(max_length=255, blank=True, null=True, verbose_name='备注')
    status = models.BooleanField(default=True, verbose_name='状态')
    lon = models.FloatField(verbose_name=u"经度", default=0.0)
    lat = models.FloatField(verbose_name=u"维度", default=0.0)
    address = models.CharField(max_length=225, verbose_name='地址', blank=True, null=True)

    tb_name = models.CharField(max_length=150, blank=True, null=True, verbose_name='模型表名')
    tb_desc = models.CharField(max_length=150, blank=True, null=True, verbose_name='模型表描述')
    tb_id = models.CharField(max_length=250, blank=True, null=True, verbose_name='记录id')
    tb_befor = models.CharField(max_length=250, blank=True, null=True, verbose_name='记录id')
    tb_after = models.CharField(max_length=250, blank=True, null=True, verbose_name='记录id')

    created_at = models.DateTimeField(default=timezone.now, verbose_name="操作时间")

    objects = models.Manager()

    def __str__(self):
        return "uid：%s" % self.uid

    class Meta:
        ordering = ['-id']
        verbose_name = '用户操作日志'
        verbose_name_plural = verbose_name


class SMSCodeLog(models.Model):
    TYPE = [
        (1, "手机号"),
        (2, "电子邮箱")
    ]

    CODE_TYPE = [
        (1, "注册/登录"),
        (2, "变更信息"),
        (3, "认证"),
        (4, "其他"),
    ]

    STATUS = [
        (0, "发送失败"),
        (2, "发送成功"),
        (3, "已使用"),
        (4, "已过期"),
    ]

    type = models.PositiveSmallIntegerField(verbose_name=u'类型', default=1, choices=TYPE)
    rec_number = models.CharField(max_length=50, blank=True, null=True, verbose_name='接收号码', db_index=True)
    code = models.PositiveIntegerField(verbose_name="验证码")
    code_type = models.PositiveSmallIntegerField(verbose_name='验证码类型', null=True, choices=CODE_TYPE)

    uid = models.CharField(verbose_name=u'UID', max_length=32, null=True, db_index=True)
    effective_time = models.PositiveIntegerField(verbose_name="有效期(s)", default=0)

    status = models.PositiveSmallIntegerField(verbose_name="状态", default=1, choices=STATUS, db_index=True)
    remark = models.CharField(max_length=50, blank=True, null=True, verbose_name='备注')
    created_at = models.DateTimeField(default=timezone.now, verbose_name="创建时间", db_index=True)
    updated_at = models.DateTimeField(verbose_name=u'更新时间', null=False, auto_now=True, editable=False,
                                      db_index=True)

    objects = models.Manager()

    def __str__(self):
        return "uid：%s" % self.uid

    class Meta:
        ordering = ['-id']
        verbose_name = '验证码记录'
        verbose_name_plural = verbose_name

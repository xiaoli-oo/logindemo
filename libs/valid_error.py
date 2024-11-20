# -*- coding: utf-8 -*-
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def valid_username(username):
    """
        长度为3-20个字符
        可以包含英文，数字，.@+-_符号
    """
    if not re.match('^[\w.@+-_]{2,30}$', username):
        raise ValidationError(
            _('%(value)s 要求3-30个字符,可以包含英文、数字、.@+-_等符号！'),
            params={'value': '用户名'},
        )


# 验证代码类型字段值是否合法
def validate_code(value):
    """
        长度为2-30个字符
        可以包含英文，数字，.@+-_符号
    """
    if not re.match('^[\w.@+-_]{2,30}$', value):
        raise ValidationError(
            _('%(value)s 要求2-30个字符,可以包含英文、数字、.@+-_等符号！'),
            params={'value': '代码值'},
        )


def validate_even(value):
    if value % 2 != 0:
        raise ValidationError(
            _('%(value)s is not an even number'),
            params={'value': value},
        )


def validate_nickname(value):
    if not re.match('^.{0,25}$', value):
        raise ValidationError(
            _('%(value)s 要求1-25个字符！'),
            params={'value': '昵称'},
        )


def validate_telephone(value):
    if not re.match(r'^1[3456789]\d{9}$', value):
        raise ValidationError(
            _('%(value)s 不合法！'),
            params={'value': '手机号'},
        )


def validate_phone(value):
    if not re.match(
            r'^(\d{11})|^(\d{4,11})|(\d{4}|\d{3})-(\d{4,11})|(\d{4}|\d{3})-(\d{4,11})-(\d{4}|\d{3}|\d{2}|\d{1})|(\d{'
            r'4,11})-(\d{4}|\d{3}|\d{2}|\d{1})$',
            value):
        raise ValidationError(
            _('%(value)s 不合法！'),
            params={'value': '电话号码'},
        )
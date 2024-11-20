from django.contrib import admin, messages
from django.utils import timezone
from django.core.exceptions import ValidationError, PermissionDenied, SuspiciousOperation
from import_export.fields import Field
from import_export import resources
from import_export import widgets
from user.models import User, UserWX, UserAddress
from user.models import UserLoginLog, UserOpLog, SMSCodeLog
from django.core.cache import caches

cache_user = caches['user']


class UserResource(resources.ModelResource):
    class Meta:
        model = User


class UserAddressResource(resources.ModelResource):
    class Meta:
        model = UserAddress
from django.contrib import admin, messages
from django.contrib.admin.models import LogEntry
from libs.utils import timebefore
from django.core.exceptions import ValidationError
from import_export.admin import ImportExportModelAdmin
from django import forms
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.forms import ClearableFileInput
from system.models import Country, Address, SystemParam, SerialNumberPool, ThirdPartyApps


# Register your models here.


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = (
        "code2", "name", "cn_name", "flag", "local_name", "code3", "lang_code", "language", "continents", "phone_code")
    search_fields = ('code2', 'name', 'cn_name', "language")
    list_per_page = 10


# Register your models here.
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("country", "province", "city", "district", "code",)
    list_filter = ('country',)
    search_fields = ("country__code2", "province", "city", "district", "code")
    list_per_page = 10


@admin.register(SystemParam)
class SystemParamAdmin(admin.ModelAdmin):
    list_display = ("name", "key", "value", "value_type", "note", "status", "lock_status", "last_logs")
    list_filter = ('value_type', 'status')
    search_fields = ('name', "key", "value",)
    list_per_page = 10

    def last_logs(self, obj):
        log_entry = LogEntry.objects.filter(object_id=obj.id,
                                            content_type__model=obj._meta.model_name).order_by(
            "-action_time").first()
        if log_entry:
            url = f"/admin/{log_entry.content_type.app_label}/{log_entry.content_type.model}/{obj.id}/history/"
            return format_html('<a href="{}" target="_blank">{}</a>', url,
                               f"【{log_entry.user.username}】-{timebefore(log_entry.action_time)}-{log_entry.get_action_flag_display()}")
        else:
            return timebefore(obj.updated_at)


@admin.register(SerialNumberPool)
class SerialNumberPoolAdmin(admin.ModelAdmin):
    list_display = (
        "name", "prefix", "suffix", "year", "month", "day", "year", "digit", "next_number", "description", "last_logs")
    search_fields = ("name", "prefix", "suffix",)
    list_per_page = 10

    def last_logs(self, obj):
        log_entry = LogEntry.objects.filter(object_id=obj.id,
                                            content_type__model=obj._meta.model_name).order_by(
            "-action_time").first()
        if log_entry:
            url = f"/admin/{log_entry.content_type.app_label}/{log_entry.content_type.model}/{obj.id}/history/"
            return format_html('<a href="{}" target="_blank">{}</a>', url,
                               f"【{log_entry.user.username}】-{timebefore(log_entry.action_time)}-{log_entry.get_action_flag_display()}")
        else:
            return timebefore(obj.updated_at)

    last_logs.short_description = '操作记录'  # 设置列标题


@admin.register(ThirdPartyApps)
class ThirdPartyAppsAdmin(admin.ModelAdmin):
    list_display = (
        "name", "type", "mchid", "appid", "original_id", "status", "public_key", "pre_qrcode", "company", "qywx_token",
        "qywx_aeskey", "qywx_agent_id", "qywx_agent_secret", "qywx_agent_name", "welcome", "created_at", "last_logs")
    search_fields = ("name", "mchid", "appid", "original_id", "public_key", "appid",)
    list_filter = ('type', 'status', 'created_at')
    list_per_page = 10

    def last_logs(self, obj):
        log_entry = LogEntry.objects.filter(object_id=obj.id,
                                            content_type__model=obj._meta.model_name).order_by(
            "-action_time").first()
        if log_entry:
            url = f"/admin/{log_entry.content_type.app_label}/{log_entry.content_type.model}/{obj.id}/history/"
            return format_html('<a href="{}" target="_blank">{}</a>', url,
                               f"【{log_entry.user.username}】-{timebefore(log_entry.action_time)}-{log_entry.get_action_flag_display()}")
        else:
            return timebefore(obj.updated_at)

    last_logs.short_description = '操作记录'  # 设置列标题

    def pre_qrcode(self, obj):
        if obj.qrcode:
            return format_html('<a href="{}" target="_blank"><img src="{}" height="30"/></a>', obj.qrcode.url,
                               obj.qrcode.url)
        else:
            return ""

    pre_qrcode.short_description = '二维码'  # 设置列标题

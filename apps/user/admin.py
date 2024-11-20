from django.contrib import admin
from django.contrib.admin.models import LogEntry
from libs.utils import timebefore
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from user.models import User, UserWX, UserAddress
from user.models import UserLoginLog, UserOpLog, SMSCodeLog
from user.resources import UserResource


class UserWXInline(admin.TabularInline):
    model = UserWX
    extra = 0  # 控制额外显示多少个空的Book表单
    fields = ('third_apps', 'head_img', 'nickname', 'open_id', 'union_id')
    exclude = ('session_key', 'access_token', 'refresh_token')  # 不显示字段


class UserAddressInline(admin.TabularInline):
    model = UserAddress
    extra = 0  # 控制额外显示多少个空的Book表单
    raw_id_fields = ["address"]


# Register your models here.
@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    resource_class = UserResource

    list_display = (
        "id", "role", "nickname", "username", "name", "sex", "pre_head_img", "email", "phone", "country",
        "last_ip", "is_staff", "status", "last_login_time", "join_time", "last_logs")
    list_filter = ('role', 'is_staff', "status", "created_at", "last_login_time",)
    list_editable = ('status',)
    search_fields = ("id", "nickname", "username", "name", "phone")
    list_per_page = 10
    inlines = [UserWXInline, UserAddressInline]

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

    def pre_head_img(self, obj):
        if obj.head_img:
            return format_html('<a href="{}" target="_blank"><img src="{}" height="30"/></a>', obj.head_img,
                               obj.head_img)
        else:
            return ""

    pre_head_img.short_description = '用户头像'  # 设置列标题

    def save_model(self, request, obj, form, change):
        '''
        :param request: 保存时本次的请求对象
        :param obj: 本次要保存的模型对象
        :param form: admin中表单
        :param change: 是否改变
        '''
        user_obj = User.objects.filter(id=obj.id).first()
        if not user_obj.check_password(obj.password) or obj.password != user_obj.password:
            obj.password = user_obj.set_password(obj.password)
        obj.save()


# Register your models here.
@admin.register(UserLoginLog)
class UserLoginLogAdmin(admin.ModelAdmin):
    list_display = (
        "uid", "login_type", "client_type", "ip", "lon", "lat", "address", "remark", "token", "created_at", "status")
    list_filter = ('login_type', 'client_type', "status", "created_at")
    search_fields = ("uid", "ip", "remark",)
    list_per_page = 10


# Register your models here.
@admin.register(UserOpLog)
class UserOpLogAdmin(admin.ModelAdmin):
    list_display = (
        "uid", "ip", "action_type", "lon", "lat", "address", "remark", "tb_name", "tb_desc", "tb_id",
        "tb_befor", "tb_after", "remark", "created_at", "status")
    list_filter = ('action_type', 'status', "created_at")
    search_fields = ("uid", "ip", "remark",)
    list_per_page = 10


# Register your models here.
@admin.register(SMSCodeLog)
class SMSCodeLogAdmin(admin.ModelAdmin):
    list_display = (
        "id", "type", "rec_number", "code", "code_type", "uid", "effective_time", "status", "remark", "created_at",
        "last_logs")
    list_filter = ('type', 'code_type', 'status', "created_at")
    search_fields = ("code", "rec_number", "remark",)
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

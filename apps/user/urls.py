from django.urls import path, re_path, include
from user import views

app_name = 'user'

urlpatterns = [

    # 登录
    path(r'login/passwd/', views.login_passwd, name=u'账号密码登录'),
    path(r'login/vcode/', views.login_vcode, name=u'手机验证码登录'),
    path(r'login/wxxcx/', views.login_wxxcx, name=u'微信快捷登录'),
    path(r'logout/', views.logout, name=u'退出登录'),
    # 发送验证码
    path(r'send/vcode/', views.send_vcode, name=u'发送验证码'),
    path(r'send2/vcode/', views.send2_vcode, name=u'(登录状态)发送验证码'),
    # 个人中心
    path(r'set/phone/', views.set_phone, name=u'绑定&换绑手机号'),
    path(r'myinfo/', views.myinfo, name=u'用户信息'),

]

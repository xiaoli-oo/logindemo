## 技术栈
```
web框架：uwsgi+django  --最后搭配nginx
数据库：mysql+redis
消息队列：django_Q
api接口：post请求，数据包以密文传输
token: 头部jwt方式
django中间件：防抖/频繁请求限制
定时任务cron: 同步服务器时钟等
操作日志：记录在数据
系统日志：采用logging.handlers，保留最近7份
添加robots文件
首次登录失败：弹出滑块验证
```

## 功能
```
登录：账号密码登录，手机短信登录，微信快捷登录，退出登录

```

## 启动程序命令
```
sh start.sh
```

## 启动消息队列
```
nohup python3 manage.py qcluster > django_q.log 2>&1 &
监控cluster执行情况：python manage.py qmonitor
监控内容：python manage.py qmemory
查看当前状态信息：python manage.py qinfo

```

## 收集静态文件
```
python manage.py collectstatic
python manage.py createcachetable sys_cache_table
```

## 同步数据库
```

1. python manage.py makemigrations [app_name] #生成迁移文件
2. python manage.py migrate #执行同步
```


# 创建超级管理员
```
python manage.py createsuperuser
```
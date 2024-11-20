"""
URL configuration for logindemo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.static import serve
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page
from logindemo.config import WEB_NAME

from . import views

admin.site.site_header = f"{WEB_NAME}-demo"
admin.site.site_title = f"{WEB_NAME}-demo"
admin.site.index_title = f"欢迎使用，{WEB_NAME}-demo"

urlpatterns = [
    path(r'robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path(r'favicon.ico', RedirectView.as_view(url='/static/img/favicon.png')),

    path(f'admin/', admin.site.urls),

    # <editor-fold desc="API">
    path(r'api/user/', include('user.urls', namespace='user')),
    # </editor-fold>

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += [
                   path("ckeditor5/", include('django_ckeditor_5.urls')),
               ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if not settings.DEBUG:
    urlpatterns += [
        path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
        path('static/<path:path>', serve, {'document_root': settings.STATIC_ROOT}),
    ]

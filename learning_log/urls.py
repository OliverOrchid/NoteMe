"""
定义 项目learning_log 的URL模式
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'',include('learning_logs.urls'
        ,namespace='learning_logs')),

    url(r'^users/',include('users.urls'
        ,namespace='users')),
    ]

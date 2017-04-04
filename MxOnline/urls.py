#-*- coding:utf-8 -*-
"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView
from users import views
import xadmin

urlpatterns = [
    url(r'^admin/', admin.site.urls),  #原生admin后台
    url(r'^xadmin/', xadmin.site.urls),  #xadmin后台
    #TemplateView.as_view相当为我们创建了view，可以传递TemplateView，直接渲染
    url(r'^$', TemplateView.as_view(template_name="index.html"),name="index"),
    #url(r'^login/$', views.user_login,name="login"), #调用函数定义的view
    url(r'^login/$', views.LoginView.as_view(),name="login"), #调用类定义的view（登陆）
    url(r'^register/$', views.RegisterView.as_view(),name="register"), #调用类定义的view（注册）
    url(r'^captcha/', include('captcha.urls')), #调用第三方验证码函数（pip install django-simple-captcha==0.4.6）
    url(r'^active/(?P<active_code>.*)/$',views.ActiveUserView.as_view(),name="active"), #激活链接
    url(r'^reset/(?P<reset_code>.*)/$',views.ResetView.as_view(),name="reset"), #重置密码链接
    url(r'^modify_pwd/$', views.ModifyPwdView.as_view(),name="modify_pwd"), #重置密码
    url(r'^forget/$', views.ForgetPwdView.as_view(),name="forget_pwd"), #找回密码
]

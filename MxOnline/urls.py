#-*- coding:utf-8 -*-
from django.conf.urls import url,include
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.static import serve  #处理静态文件的模块

from users import views
from organization import views as views1
import xadmin
from MxOnline.settings import MEDIA_ROOT

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
    url(r'^org_list/$', views1.OrgView.as_view(),name="org_list"), #课程机构首页
    #因为打开图片http://localhost:8000/media/org/2017/04/imooc_logo.png,所有要定义media的url，
    # serve是处理静态文件的，把静态资源的绝对路径传给它，就可以正常打印我们的图片
    url(r'^media/(?P<path>.*)/$',serve,{"document_root":MEDIA_ROOT}),
]

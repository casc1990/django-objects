#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Author:pengbo
__date__ = '2017/3/21 12:29'

from extra_apps import xadmin
from xadmin import views
from .models import UserProfile,EmailVerifyRecord,Banner

'''
class UserProfileAdmin(object):
    list_display = ['nick_name', 'birday', 'gender', 'address','mobile','image']  # 显示字段   定义要在admin后台显示的字段
    search_fields = ['nick_name', 'gender', 'address','mobile','image']   # 搜索变量   定义在admin后台搜索框里可以搜索的字段
    list_filter = ['nick_name', 'birday', 'gender', 'address','mobile','image']   # 筛选变量  指定要筛选的字段
'''
class BaseSetting(object):
    enable_themes = True   #开启主题功能
    use_bootswatch = True #使用主题

class GlobalSettings(object):
    site_title = u'京东技术后台管理系统' #页头
    site_footer = u'京东技术学院'  #页脚
    menu_style = "accordion"


class EmailVerifyRecordAdmin(object):   #定义mode的基本功能
    list_display = ['code','email','send_type','send_time']   #显示字段   定义要在admin后台显示的字段
    search_fields = ['code','email','send_type']  #搜索变量   定义在admin后台搜索框里可以搜索的字段
    list_filter = ['code','email','send_type','send_time'] #筛选变量  指定要筛选的字段

class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index','add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index','add_time']


#xadmin.site.register(UserProfile,UserProfileAdmin)
xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)  #注册时将值传递给我们定义的model（字符串名==字段名）
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)  #注册BaseSetting的model
xadmin.site.register(views.CommAdminView,GlobalSettings) #注册全局配置的model
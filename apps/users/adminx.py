#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Author:pengbo
__date__ = '2017/3/21 12:29'

from extra_apps import xadmin
from .models import EmailVerifyRecord

class EmailVerifyRecordAdmin(object):
    list_display = ['code','email','send_type','send_time']   #显示字段   定义要在admin后台显示的字段
    search_fields = ['code','email','send_type']  #搜索变量   定义在admin后台搜索框里可以搜索的字段
    list_filter = ['code','email','send_type','send_time'] #筛选变量  指定要筛选的字段

xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)  #注册时将值传递给我们定义的model（字符串名==字段名）
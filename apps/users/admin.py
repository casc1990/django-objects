#-*- coding:utf-8 -*-
from django.contrib import admin
from users.models import  UserProfile

#model的管理器
class UserProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile,UserProfileAdmin) #注册model
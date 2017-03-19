#-*- coding:utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

#AbstractUser就是定义django的user表的函数
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserProfile(AbstractUser):
    ''' 用户model，继承django的user表，重写了user表，并添加了user的更多属性
        定义昵称、生日、性别、地址、手机号、图像存储位置
        null=True：orm操作允许为空，blank=True：admin后台操作允许为空；default：默认值
        verbose_name：后台显示的名称；max_length：长度 (图片类型也是以字符存储的，也需要指定长度)'''
    nick_name = models.CharField(max_length=50,verbose_name=u'昵称',default='')
    birday = models.DateField(verbose_name=u'生日',null=True,blank=True)
    gender = models.CharField(choices=(("male",u'男'),("female",u'女')),verbose_name=u'性别',max_length=1,default='female')
    address = models.CharField(max_length=100,verbose_name=u'地址',default=u"")
    mobile = models.CharField(max_length=11,verbose_name=u'手机号',null=True,blank=True)
    image = models.ImageField(upload_to="image/%Y/%m",default=u'image/default.png',max_length=500)

    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):  #__unicode__类似于python3中的__str__,打印这个类，就执行这个方法
        return self.username  #打印AbstractUser类里的username值  因为UserProfile继承了AbstractUser

class EmailVerifyRecord(models.Model):
    ''' 邮箱验证码model'''
    code = models.CharField(max_length=20,verbose_name=u'验证码')
    email = models.CharField(max_length=50,verbose_name=u'邮箱')
    send_type = models.CharField(max_length=10,choices=(('forget',u'密码找回'),('register',u'注册')))
    send_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u'邮箱验证码'
        verbose_name_plural = verbose_name

class Banner(models.Model):
    title = models.CharField(max_length=100,verbose_name=u'标题')
    image = models.ImageField(upload_to='banner/%Y/%m',verbose_name=u'轮播图',max_length=500)
    url = models.URLField(max_length=200,verbose_name=u'访问地址')
    index = models.IntegerField(default=100,verbose_name=u'顺序')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'轮播图'
        verbose_name_plural = verbose_name
#-*- coding:utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.db import models


from users.models import UserProfile   #导入user app的model
from courses.models import Course  #导入courses app的model


class UserAsk(models.Model):
    ''' 用户咨询相关'''
    name = models.CharField(max_length=20, verbose_name=u'姓名')
    mobile = models.CharField(max_length=11,verbose_name=u'手机号')
    course_name = models.CharField(max_length=50,verbose_name=u'课程名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'用户咨询'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseComments(models.Model):
    ''' 课程评论'''
    name = models.ForeignKey(UserProfile,verbose_name=u'用户')
    course = models.ForeignKey(Course,verbose_name=u'课程')
    comments = models.CharField(max_length=200,verbose_name=u'评论')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程评论'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class UserFavorite(models.Model):
    ''' 用户收藏'''
    user  = models.ForeignKey(UserProfile,verbose_name=u'用户')
    fav_id = models.IntegerField(default=0,verbose_name=u'数据id')
    fav_type = models.IntegerField(choices=((1,u'课程'),(2,u'课程机构'),(3,u'讲师')),default=1,verbose_name=u'收藏类型')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'用户收藏'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.user


class UserMessage(models.Model):
    ''' 用户消息  default=0发送给所有人，user接受user id，发送给指定id的用户   '''
    user = models.IntegerField(default=0,verbose_name=u'接受用户')
    message = models.CharField(max_length=500,verbose_name=u'消息内容')
    has_read = models.BooleanField(default=False,verbose_name=u'是否已读')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'用户消息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.user


class UserCourse(models.Model):
    name = models.ForeignKey(UserProfile, verbose_name=u'用户')
    course = models.ForeignKey(Course, verbose_name=u'课程')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'用户课程'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name





#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Author:pengbo
__date__ = '2017/3/26 0:22'
from django import forms

class LoginForm(forms.Form):
    #username一定要和html里的定义的表单名字一致，required=True：这个表单是必须填写的，max_length=20最大长度
    username = forms.CharField(required=True,max_length=20) #username是字符串类型
    password = forms.CharField(required=True,min_length=6)
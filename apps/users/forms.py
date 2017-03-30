#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Author:pengbo
__date__ = '2017/3/26 0:22'
from django import forms
from captcha.fields import CaptchaField

class LoginForm(forms.Form):
    #username一定要和html里的定义的表单名字一致，required=True：这个表单是必须填写的，max_length=20最大长度
    username = forms.CharField(required=True,max_length=20) #username是字符串类型
    password = forms.CharField(required=True,min_length=6)

class RegisterForm(forms.Form):
    email = forms.EmailField(required=True) #验证邮箱
    password = forms.CharField(required=True, min_length=6) #验证密码
    captcha = CaptchaField()  #验证码（调用第三方模块）
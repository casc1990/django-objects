#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Author:pengbo
__date__ = '2017/3/26 0:22'
from django import forms

from captcha.fields import CaptchaField


class LoginForm(forms.Form): #用户登陆时验证用户名、密码的form
    #username一定要和html里的定义的表单名字一致，required=True：这个表单是必须填写的，max_length=20最大长度
    username = forms.CharField(required=True,max_length=20) #username是字符串类型
    password = forms.CharField(required=True,min_length=6)

class RegisterForm(forms.Form): #注册时验证邮箱、密码、验证码的form
    email = forms.EmailField(required=True) #验证邮箱
    password = forms.CharField(required=True, min_length=6) #验证密码
    #验证码（调用第三方模块,error_messages指定错误信息，captcha是字典对象，对象invalid的value(u'验证码错误')会被错误接受）
    captcha = CaptchaField(error_messages={'invalid':u'验证码错误'})

class ForgetForm(forms.Form): #找回密码时验证邮箱、验证码的form
    email = forms.EmailField(required=True) #验证邮箱
    captcha = CaptchaField(error_messages={'invalid':u'验证码错误'})


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True,min_length=6)
    password2 = forms.CharField(required=True,min_length=6)
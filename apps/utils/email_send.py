#!/usr/bin/env python
# -*- coding:utf-8 -*-
#Author:pengbo
__date__ = '2017/4/2 23:46'
from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from MxOnline import settings

import random

def random_str(randomlength=8):
    '''生成验证码函数'''
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) -1
    for i in range(randomlength):
        str += chars[random.randint(0,length)]
    return str

def send_register_email(email,send_type='register'):
    ''' 发送验证码函数 '''
    code = random_str(16)
    email_record = EmailVerifyRecord()
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()
    if send_type == 'register':
        email_title = u'京东技术网注册激活链接'
        email_body = u'请点击下面的链接激活你的账户：http://localhost:8000/active/{0}'.format(code)
        send_status = send_mail(email_title,email_body,settings.EMAIL_FROM,[email])
        if send_status:
            pass
    elif send_type == 'forget':
        email_title = u'京东技术网密码重置链接'
        email_body = u'请点击下面的链接重置你的密码：http://localhost:8000/reset/{0}'.format(code)
        send_status = send_mail(email_title, email_body, settings.EMAIL_FROM, [email])
        if send_status:
            pass




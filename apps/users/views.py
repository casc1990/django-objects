#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.contrib.auth import authenticate,login #验证模块
from django.contrib.auth.backends import ModelBackend #验证模块
from django.db.models import Q  #支持并集、交集查询
from django.views.generic.base import View #view模块
from django.contrib.auth.hashers import make_password #加密密码模块

from .models import UserProfile
from .models import EmailVerifyRecord
from .forms import LoginForm,RegisterForm,ForgetForm,ModifyPwdForm
from utils.email_send import send_register_email

class CustomBackend(ModelBackend): #定义自定义的认证方法
    '''继承ModelBackend类，使用这个类的authenticate方法验证
     思路：并集查询数据库，找到查询结果后，验证用户密码，有异常，就返回none，没有异常，返回对象'''
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # 查询数据库里username等于调用传入的username的数据（密码是密文的，无法比对，get方法取的是唯一值）
            user = UserProfile.objects.get(Q(username=username)|Q(email=username)) #查询username=username或者email=username
            #user_active = UserProfile.objects.get(Q(username=username),Q(is_active=1))
            #Q查询并集，|表示或；','表示 and关系
            #user = UserProfile.objects.get(Q(username=username) | Q(email=username),Q(password=password))
            if user.check_password(password): #比对查询到的用户密码
                return user
        except Exception as e:
            return None  #异常，返回None

class ActiveUserView(View): #用户激活view
    ''' 用户点击激活链接。查询验证码表，找到发送的验证码，如果找到，修改用户为激活，没有找到验证码，返回验证失效页面'''
    def get(self,request,active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')

class RegisterView(View): #注册view
    '''如果是get方法，返回注册页面，register_form实例化验证表单，并传给模板文件，模板文件使用register_form.captcha显示验证码
    思路：验证用户注册时的输入，验证通过，查询数据库，邮箱是否已存在，存在返回提示信息，不存在，插入用户数据；
         调用发送验证码函数并返回登陆页面'''
    def get(self,request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form':register_form})
    def post(self,request):
    #如果是post请求，验证表单，取出用户输入的内容，写入数据库，调用send_register_email函数发邮件
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():  #表单验证通过后，检查数据库email，修改数据库
            email = request.POST.get("email","")
            if UserProfile.objects.filter(email=email): #数据库email存在，提示错误
                return render(request, 'register.html', {'register_form': register_form,'msg':u'用户邮箱已注册'})
            pass_word = request.POST.get("password","")
            user_profile = UserProfile()
            user_profile.email = email
            user_profile.is_active = False
            user_profile.username = email
            #make_password(pass_word)加密明文密码
            user_profile.password = make_password(pass_word)
            user_profile.save()

            send_register_email(email,'register')  #发送邮件，send_type='register'
            return render(request, 'login.html', {}) #注册完成跳转到登陆页面

        else:
            return render(request, 'register.html', {'register_form': register_form})


class LoginView(View): #登陆验证view（使用类定义view）
    def get(self,request):  #使用View类里的get方法（等同于if request.method == 'GET': ）
        return render(request, 'login.html', {})
    def post(self,request): #等同于if request.method == 'POST':
        # 实例化表单对象,把请求的post对象传递过去，post对象里有username和password信息，然后验证这些字段的表单
        login_form = LoginForm(request.POST)
        if login_form.is_valid(): #验证request.POST里的username和password是否有错误
            user_name = request.POST.get("username", '')  # 获取输入的用户名
            pass_word = request.POST.get("password", '')  # 获取密码
            # 调用上面我们自定义（CustomBackend）的authenticate方法验证用户名和密码
            user = authenticate(username=user_name, password=pass_word)
            if user is not None: #验证通过
                if user.is_active == True: #判断是否是激活状态
                    login(request, user)  # 调用login方法登陆
                    return render(request, "index.html")  # 并把首页返回给用户
                else: #如果未激活
                    return render(request, 'login.html', {'msg': u'用户未激活'})
            else: #验证不通过
                return render(request, 'login.html', {'msg': u'用户名或者密码错误'})  #返回登陆页面，提示用户名或者密码错误
        else:  #表单验证不通过
            return render(request, 'login.html', {'login_form':login_form})  # 返回登陆页面，提示表单验证错误


class ForgetPwdView(View):
    ''' 找回密码
    思路：验证用户填写的表单，表单验证通过，在判断数据库里是否有这个邮箱，都通过，发送重置邮件'''
    def get(self,request):
        forget_form = ForgetForm()
        return render(request,"forgetpwd.html",{'forget_form': forget_form})
    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email","")
            if UserProfile.objects.filter(email=email): #数据库email存在，提示错误
                send_register_email(email,'forget')
                return render(request, "send_success.html")
            else:
                return render(request, "forgetpwd.html", {'msg': u'账户不存在'})

        else:
            return render(request, "forgetpwd.html", {'forget_form': forget_form})


class ResetView(View):
    ''' 接收重置密码的url请求
    思路：取到重置密码的验证码（reset_code）,查找数据库是否有这个验证码，都通过，返回重置密码的页面并将邮箱传递'''
    def get(self,request,reset_code):
        all_records = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_records:
            for record in all_records:
                email = record.email
                #把验证码对应的email信息传递到模板。(记录是哪个用户修改的密码)
                return render(request,'password_reset.html',{'email':email})
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class ModifyPwdView(View):
    ''' 接收用户重置密码的表单（用户填完重置密码的表单后，会被定向到这个view）
    思路：验证表单，取到隐藏的email、密码，两次输入的密码一致，修改密码，返回登录页面'''
    def post(self,request):
        modifypwd_from = ModifyPwdForm(request.POST)
        if modifypwd_from.is_valid():
            email = request.POST.get("email", "")
            pwd1 = request.POST.get("password1","")
            pwd2 = request.POST.get("password2", "")
            if pwd1 == pwd2:
                user = UserProfile.objects.get(email=email)
                user.password = make_password(pwd1)
                user.save()
                return render(request, 'login.html')
            else:
                return render(request,'password_reset.html',{'email':email,'msg':u'密码不一致'})
        else:
            email = request.POST.get("email", "")
            return render(request, 'password_reset.html', {'email': email,'modifypwd_from':modifypwd_from})


def user_login(request):  #用户登陆（使用函数的view）
    if request.method == 'POST': #如果用户请求的方法是post
        user_name = request.POST.get("username",'')  #获取输入的用户名
        pass_word = request.POST.get("password",'')  #获取密码
        # 调用上面我们自定义（CustomBackend）的authenticate方法验证用户名和密码
        user = authenticate(username=user_name,password=pass_word)
        if user is not None: #验证通过
            login(request, user)  # 调用login方法登陆
            return render(request, "index.html")  # 并把首页返回给用户
        else:  #验证不通过
            return render(request, 'login.html', {'msg': u'用户名或者密码错误'})  # 验证不通过，返回登陆页面
    elif request.method == 'GET':  #get方法也返回登陆页面
        return render(request,'login.html',{})
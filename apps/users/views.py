#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q  #支持并集、交集查询
from django.views.generic.base import View

from .models import UserProfile
from .forms import LoginForm,RegisterForm

class CustomBackend(ModelBackend): #定义自定义的认证方法
    #继承ModelBackend类，使用这个类的authenticate方法验证
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # 查询数据库里username等于调用传入的username的数据（密码是密文的，无法比对，get方法取的是唯一值）
            user = UserProfile.objects.get(Q(username=username)|Q(email=username)) #查询username=username或者email=username
            #user_active = UserProfile.objects.get(Q(username=username),Q(is_active=1))
            #Q查询并集，|表示或；','表示 and关系
            #user = UserProfile.objects.get(Q(username=username) | Q(email=username),Q(password=password))
            if user.check_password(password): #比对查询到的用户密码
                if user.is_active:
                    return user
                else:
                    pass
        except Exception as e:
            return None  #异常，返回None

class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form':register_form})
    def post(self,request):
        pass

class LoginView(View): #使用类定义view
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
                login(request, user)  # 调用login方法登陆
                return render(request, "index.html")  # 并把首页返回给用户
            else: #验证不通过
                return render(request, 'login.html', {'msg': u'用户名或者密码错误'})  #返回登陆页面，提示用户名或者密码错误
        else:  #表单验证不通过
            return render(request, 'login.html', {'login_form':login_form})  # 返回登陆页面，提示表单验证错误

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
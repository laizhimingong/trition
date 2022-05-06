from django.contrib import auth
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from user import models


# Create your views here.

# 自定义登录验证装饰器
def check_login(func):
    # print("check_login")
    def warpper(request, *args, **kwargs):
        is_login = request.session.get('is_login', False)
        if is_login:
            return func(request, *args, **kwargs)
        else:
            return render(request, 'login.html')
    return warpper


def login(request):
    # print('login')
    return render(request, 'login.html')


@csrf_exempt
def getlogin(request):
    # print('getlogin')
    if request.method == 'POST':
        csrfmiddlewaretoken = request.POST.get('csrfmiddlewaretoken')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email and password:
            user = models.UserInfo.objects.filter(email=email, password=password).first()
            if user:
                request.session['is_login'] = True  # 设置session的随机字段值
                request.session['email'] = user.email  # 设置username字段为登录用户
                # return redirect( '/v1/home',{'email': email})
                return redirect('/v1/home/')
            else:
                print("账户或密码错误")
    return redirect("/")


# 用户退出
def logout(request):
    # print("logout")
    auth.logout(request)
    return redirect("/")

#用户密码更新
def updatePassword(request):
    # print("updatePassword")
    return render(request,'update_password.html')
#修改密码接口\
def getUpdatePassword(request):
    # print("getUpdatePassword")
    if request.method == 'POST':
        csrfmiddlewaretoken = request.POST.get('csrfmiddlewaretoken')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('val-password')
        password2 = request.POST.get('val-confirm-password')
        if email and password and password1 and password2:
            user = models.UserInfo.objects.filter(email=email,password=password).first()
            if user:
                if password1 == password2:
                    models.UserInfo.objects.filter(email=email).update(password=password1)
                    return redirect('/')
                else:
                    print("两次输入密码不一致,请重新输入")
                    # data = {"code": 1001, "msg": "两次输入密码不一致,请重新输入"}
                    # return HttpResponse(json.dumps(data))
                    return redirect('/update_password/')
            else:
                print("用户邮箱不存在或密码错误,请重新输入")
                return redirect('/update_password/')
    return redirect("/")
# def getUpdatePassword(request):
#     print("getUpdatePassword")
#     if request.method == 'POST':
#         csrfmiddlewaretoken = request.POST.get('csrfmiddlewaretoken')
#         email = request.POST.get('email')
#         password1 = request.POST.get('val-password')
#         password2 = request.POST.get('val-confirm-password')
#         if email and password1 and password2:
#             user = models.UserInfo.objects.filter(email=email,).first()
#             if user:
#                 if password1 == password2:
#                     models.UserInfo.objects.filter(email=email).update(password=password1)
#                     return redirect('/')
#                 else:
#                     print("两次输入密码不一致,请重新输入")
#                     return redirect('/update_password/')
#             else:
#                 print("用户邮箱不存在,请重新输入")
#                 return redirect('/update_password/')
#     return redirect("/")
# Django异常处理对象
def page_not_find(request, exception):
    """全局404页面处理"""
    # print("全局404页面处理")
    return render(request, '404.html')


def page_error(request):
    """全局500页面处理"""
    # print("全局500页面处理")
    return render(request, '500.html')


def resources_not_available(request, exception):
    """全局403页面处理"""
    # print("全局403页面处理")
    return render(request, '403.html')

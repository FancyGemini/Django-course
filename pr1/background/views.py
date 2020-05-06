# coding:utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from background import models
from django.core.exceptions import ObjectDoesNotExist


def teacher(request):
    pass


def student(request):
    pass


def home(request):
    return render(request, 'home.html')


def check_cookies(request):
    is_stu = True
    v = request.COOKIES.get('log_id_s')
    if not v:
        v = request.COOKIES.get('log_id_t')
        if not v:
            return False
        else:
            is_stu = False
    return True



def signin(request):
    if check_cookies(request):
        v = request.COOKIES.get('log_id_s')
        if not v:
            v = request.COOKIES.get('log_id_t')
            return redirect('/index', log_id_t=str(v))
        else:
            return redirect('/index', log_id_s=str(v))
    else:
        return render(request, 'Sign In.html')



def waiting(request):
    request.encoding = 'utf-8'
    id = request.GET.get('log_id')
    pwd = request.GET.get('log_pwd')
    id = str(id)
    pwd = str(pwd)
    if not id.strip():
        messages.error(request, '请输入你的ID！')
        return redirect('/')
    if not pwd.strip():
        messages.error(request, '请输入你的密码！')
        return redirect('/')
    try:
        info = models.Student.objects.get(sid=id)
        corr = info
        corr_pwd = str(corr.spasswd)
        if corr_pwd == pwd:
            re = redirect('/index')
            if request.COOKIES.get('log_id_s'):
                re.delete_cookie('log_id_s')
            if request.COOKIES.get('log_id_t'):
                re.delete_cookie('log_id_t')
            re.set_cookie('log_id_s', id)
            return re
    except ObjectDoesNotExist:
        try:
            info = models.Teacher.objects.get(tid=id)
            corr = info
            corr_pwd = str(corr.tpasswd)
            if corr_pwd == pwd:
                re = redirect('/index')
                if request.COOKIES.get('log_id_s'):
                    re.delete_cookie('log_id_s')
                if request.COOKIES.get('log_id_t'):
                    re.delete_cookie('log_id_t')
                re.set_cookie('log_id_t', id)
                return re
        except ObjectDoesNotExist:
            messages.error(request, '你输入的账户或密码错误！')
            return redirect('/')
    pass



def index(request):
    return render(request, 'AdminLTE/index.html')


def index2(request):
    return render(request, 'AdminLTE/index2.html')


def index3(request):
    return render(request, 'AdminLTE/index3.html')


def starter(request):
    return render(request, 'AdminLTE/starter.html')

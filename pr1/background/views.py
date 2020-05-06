# coding:utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from background import models
from django.core.exceptions import ObjectDoesNotExist



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
            return redirect('/student', log_id_s=str(v))
    else:
        return render(request, 'Sign In.html')



def waiting(request):
    request.encoding = 'utf-8'
    id = request.POST.get('log_id')
    pwd = request.POST.get('log_pwd')
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
            re = redirect('/student')
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
                re = redirect('/teacher')
                if request.COOKIES.get('log_id_s'):
                    re.delete_cookie('log_id_s')
                if request.COOKIES.get('log_id_t'):
                    re.delete_cookie('log_id_t')
                re.set_cookie('log_id_t', id)
                return re
        except ObjectDoesNotExist:
            messages.error(request, '你输入的账户不存在！')
            return redirect('/')
    messages.error(request, '你输入的密码不正确！')
    return redirect('/')


def student(request):
    return render(request, 'AdminLTE/student.html')


def teacher(request):
    return render(request, 'AdminLTE/teacher.html')


def super(request):
    return render(request, 'AdminLTE/super.html')

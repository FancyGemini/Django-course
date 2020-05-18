# coding:utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib import messages
from django.core import exceptions
from django.db.models import Q
from django.utils import timezone
from io import BytesIO
from background import models
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize
import json
import qrcode
import arrow
import datetime, time
import uuid
from background import utils as u
# import pyzbar.pyzbar as pyzbar
# import cv2

def page_not_found(request, exception, template_name='404.html'):
    return render(request, '404.html')

def page_error(request, template_name='500.html'):
    return render(request, '500.html')

def home(request):
    return render(request, 'home.html')


def signin(request):
    if u.check_cookies(request):
        v = request.COOKIES.get('log_s')
        if not v:
            v = request.COOKIES.get('log_t')
            return redirect('/teacher', log_t=str(v))
        else:
            return redirect('/student', log_s=str(v))
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
            #if request.POST.get('sign')
            re = redirect('/student')
            re.set_cookie('log_s', str(info.sid))
            return re
    except ObjectDoesNotExist:
        try:
            info = models.Teacher.objects.get(tid=id)
            corr = info
            corr_pwd = str(corr.tpasswd)
            if corr_pwd == pwd:
                re = redirect('/teacher')
                re.set_cookie('log_t', str(info.tid))
                return re
        except ObjectDoesNotExist:
            messages.error(request, '你输入的账户不存在！')
            return redirect('/')
    messages.error(request, '你输入的密码不正确！')
    return redirect('/')


def logout(request):
    re = redirect('/')
    re.delete_cookie('log_s')
    re.delete_cookie('log_t')
    return re

# 测试用
def class_test(request):
    class_list = models.Course.objects.all().values('cid', 'cname', 'tid__tname')
    context = {
        'all_class' : class_list,
    }
    return render(request, 'class.html', context)

# 测试用
def qianndao_test(request, cid):
    #sid = str(request.COOKIES.get('log_s'))
    context = {
        'cid' : cid,
    }
    return render(request, 'qiandao.html', context)

def classform(request, cid):
    context = { 'cid' : cid }
    return render(request, 'class_form.html', context)

# 获取对应签到二维码
def get_qrcode(request, cousign):
    cousignid = u.parse_UUID(cousign)
    try:
        cou = models.CouSignInfo.objects.get(id = cousignid)
        img = qrcode.make('http://' + request.get_host() + '/student/sign/' + str(cou.id))
        buf = BytesIO()
        img.save(buf)
        img_stream = buf.getvalue()
        return HttpResponse(img_stream, content_type='image/png')
    except Exception:
        return HttpResponse('')

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
import qrcode
import arrow
import datetime
from background import utils as u
# import pyzbar.pyzbar as pyzbar
# import cv2


def home(request):
    return render(request, 'home.html')


def signin(request):
    if u.check_cookies(request):
        v = request.COOKIES.get('log_s')
        if not v:
            v = request.COOKIES.get('log_t')
            return redirect('/index', log_t=str(v))
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


# 教师发布签到页面
# 还需要加入权限判断 只有老师能访问该页面 目前测试阶段暂不加
def publish_sign(request, cid):
    context = {}
    request.encoding = 'utf-8'
    tfmt = "YYYY-MM-DD[T]hh:mm:ss-ZZZ"
    if request.POST:
        utc = arrow.get(request.POST['start']+":00-Asia/Shanghai", tfmt)
        context['starttime'] = utc.datetime
        utc = arrow.get(request.POST['end']+":00-Asia/Shanghai", tfmt)
        context['endtime'] = utc.datetime
        context['cousign'] = u.set_sign(cid, context['starttime'], context['endtime'])
        context['host'] = request.get_host()
    return render(request, 'publish_test.html', context)


# 学生签到界面
def sign_page(request, cousign):
    sid = str(request.COOKIES.get('log_s'))
    cou = u.parse_UUID(cousign)
    context = {}
    try:
        stu = models.Student.objects.get(sid = sid)
        cousignid = models.CouSignInfo.objects.get(id = cou)
        context = u.student_sign(str(sid), cousignid.cid.cid, cou)
        request.session['signinfo'] = context
        request.session['signflag'] = True
        print(request.session['signflag'])
        return redirect('/student')
    except Exception:
        context['cousign'] = cou
        request.session['signinfo'] = context
        re = redirect('/')
        return re
        
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


def student(request):
    v = request.COOKIES.get('log_s')
    id = str(v)
    info = models.Student.objects.get(sid=id)
    courses = models.StuToCourse.objects.filter(sid=id)
    # context = {'info':info, 'courses':[], 'locations':[]}
    context = {'info':info, 'courses':[]}
    request.session.setdefault('signflag', False)
    signinfo = request.session.get('signinfo')
    request.session.set_expiry(5)
    request.session.clear_expired()
    if signinfo:
        context.update(signinfo)
    for cou in courses:
        cou_id = cou.cid
        cou_id = str(cou_id)
        print(cou_id)
        cou_name = models.Course.objects.get(cid=cou_id).cname
        cou_name = str(cou_name)
        context['courses'].append(cou_name)
    return render(request, 'AdminLTE/student.html', context)


def student_course(request):
    v = request.COOKIES.get('log_s')
    id = str(v)
    info = models.Student.objects.get(sid=id)
    course = models.StuToCourse.objects.filter(sid__sid=id).values('cid__cid', 'cid__cname')
    for cou in course:
        print(cou)
    context = {
        'info' : info,
        'course' : course,
    }
    return render(request, 'AdminLTE/student_course.html', context)



def teacher(request):
    v = request.COOKIES.get('log_t')
    id = str(v)
    info = models.Teacher.objects.get(tid=id)
    courses = models.Course.objects.filter(tid=id)
    # context = {'info':info, 'courses':[], 'locations':[]}
    context = {'info':info, 'auth':info.tauth, 'courses':[]}
    for cou in courses:
        cou_id = cou.cid
        cou_id = str(cou_id)
        print(cou_id)
        cou_name = models.Course.objects.get(cid=cou_id).cname
        cou_name = str(cou_name)
        context['courses'].append(cou_name)
    return render(request, 'AdminLTE/teacher.html', context)


def teacher_course(request):
    v = request.COOKIES.get('log_t')
    info = models.Teacher.objects.get(tid=str(v))
    course = models.Course.objects.filter(tid=info).values('cid', 'cname')
    for cou in course:
        print(cou)
    context = {
        'info' : info,
        'course' : course,
    }
    return render(request, 'AdminLTE/teacher_course.html', context)


def super(request):
    return render(request, 'AdminLTE/super.html')

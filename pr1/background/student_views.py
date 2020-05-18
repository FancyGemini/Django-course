from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.core import exceptions

from background import models
from background import utils as u

import arrow
import datetime, time
import uuid

def student(request):
    v = request.COOKIES.get('log_s')
    id = str(v)
    info = models.Student.objects.get(sid=id)
    courses = models.StuToCourse.objects.filter(sid=id)
    # context = {'info':info, 'courses':[], 'locations':[]}
    context = {'info':info, 'courses':[]}
    request.session.setdefault('signflag', False)
    signinfo = request.session.get('signinfo')
    sign_after_login = request.session.get('cousign')
    # 如果是直接进入签到链接的 登陆后再重定向至签到链接
    if sign_after_login:
        del request.session['cousign']
        return redirect('/student/sign/' + sign_after_login)
    request.session.set_expiry(5)
    request.session.clear_expired()
    
    stu_cous = models.StuToCourse.objects.filter(sid__sid=id).values('cid__cid', 'cid__cname')
    cid = []
    rloc = []
    cname = []
    ctime = []
    for cou in stu_cous:
        time_loc = models.CouOnClass.objects.filter(cid__cid=cou['cid__cid']).values('ctime', 'rid__rloc', 'cday')
        for t_l in time_loc:
            class_day = (int(t_l['cday']))
            now_time = datetime.datetime.now()
            # print(str(class_day) + ' / ' + now_time.strftime("%w"))
            today = now_time.strftime("%w")
            if today == '0':
                today = '7'
            if str(class_day) == today:
                cid.append(cou['cid__cid'])
                cname.append(cou['cid__cname'])
                ctime.append(t_l['ctime'])
                rloc.append(t_l['rid__rloc'])
    stoday_obj = u.TodayCourse(cid=cid, cname=cname, ctime=ctime, rloc=rloc)
    
    if signinfo:
        context.update(signinfo)
    for cou in courses:
        cou_id = cou.cid
        cou_id = str(cou_id)
        print(cou_id)
        cou_name = models.Course.objects.get(cid=cou_id).cname
        cou_name = str(cou_name)
        context['courses'].append(cou_name)
    context['stoday_obj'] = stoday_obj
    return render(request, 'AdminLTE/student.html', context)


def student_course(request):
    v = request.COOKIES.get('log_s')
    id = str(v)
    info = models.Student.objects.get(sid=id)
    course = models.StuToCourse.objects.filter(sid__sid=id).values('cid__cid', 'cid__cname')
    rlocs = []
    cids = []
    cnames = []
    cdays = []
    ctimes = []
    for cou in course:
        c_rdts = models.CouOnClass.objects.filter(cid__cid=cou['cid__cid']).values('rid__rloc', 'cday', 'ctime')
        for c_rdt in c_rdts:
            cids.append(cou['cid__cid'])
            cnames.append(cou['cid__cname'])
            rlocs.append(c_rdt['rid__rloc'])
            cdays.append(c_rdt['cday'])
            ctimes.append(c_rdt['ctime'])
    scourse_obj = u.CourseTable(rloc=rlocs, cid=cids, cname=cnames, cday=cdays, ctime=ctimes)
    for cou in course:
        print(cou)
    context = {
        'info' : info,
        'scourse_obj' : scourse_obj,
    }
    return render(request, 'AdminLTE/student_course.html', context)

# 学生签到界面
def sign_page(request, cousign):
    sid = str(request.COOKIES.get('log_s'))
    context = {}
    try:
        stu = models.Student.objects.get(sid = sid)
        cousignid = models.CouSignInfo.objects.get(id = uuid.UUID(cousign))
        context = u.student_sign(str(sid), cousignid.cid.cid, cousignid)
        #print(context)
        request.session['signinfo'] = context
        request.session['signflag'] = True
        #print(request.session['signflag'])
        return redirect('/student')
    except Exception as e:
        print(e)
        context['cousign'] = cousign
        request.session['signinfo'] = context
        request.session['cousign'] = cousign
        re = redirect('/')
        return re
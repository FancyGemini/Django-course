from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.core import exceptions

from background import models
from background import utils as u

import arrow
import datetime, time
import uuid

def teacher(request):
    v = request.COOKIES.get('log_t')
    id = str(v)
    info = models.Teacher.objects.get(tid=id)
    courses = models.Course.objects.filter(tid__tid=id).values('cid', 'cname')
    cid = []
    rloc = []
    cname = []
    ctime = []
    for cou in courses:
        time_loc = models.CouOnClass.objects.filter(cid__cid=cou['cid']).values('ctime', 'rid__rloc', 'cday')
        for t_l in time_loc:
            class_day = (int(t_l['cday']))
            now_time = datetime.datetime.now()
            # print(str(class_day) + ' / ' + now_time.strftime("%w"))
            today = now_time.strftime("%w")
            if today == '0':
                today = '7'
            if str(class_day) == today:
                cid.append(cou['cid'])
                cname.append(cou['cname'])
                ctime.append(t_l['ctime'])
                rloc.append(t_l['rid__rloc'])
    ttoday_obj = u.TodayCourse(cid=cid, cname=cname, ctime=ctime, rloc=rloc)
    # print(ttoday_obj.ttoday_html())
    context = {
        'info':info,
        'ttoday_obj':ttoday_obj,
    }
    return render(request, 'AdminLTE/teacher.html', context)


def teacher_course(request):
    v = request.COOKIES.get('log_t')
    info = models.Teacher.objects.get(tid=str(v))
    course = models.Course.objects.filter(tid__tid=str(v)).values('cid', 'cname')
    # c_info = []
    rlocs = []
    cids = []
    cnames = []
    cdays = []
    ctimes = []
    for cou in course:
        c_rdts = models.CouOnClass.objects.filter(cid__cid=cou['cid']).values('rid__rloc', 'cday', 'ctime')
        for c_rdt in c_rdts:
            cids.append(cou['cid'])
            cnames.append(cou['cname'])
            rlocs.append(c_rdt['rid__rloc'])
            cdays.append(c_rdt['cday'])
            ctimes.append(c_rdt['ctime'])
    tcourse_obj = u.CourseTable(rloc=rlocs, cid=cids, cname=cnames, cday=cdays, ctime=ctimes)
    # print(tcourse_obj.tcourse_html())
    context = {
        'info' : info,
        'tcourse_obj' : tcourse_obj,
    }
    return render(request, 'AdminLTE/teacher_course.html', context)

# 签到发布记录
def sign_info(request):
    v = request.COOKIES.get('log_t')
    tinfo = models.Teacher.objects.get(tid=str(v))
    signs = models.CouSignInfo.objects.filter(cid__tid__tid=str(v)).order_by('-timestart').values('cid__cid', 'cid__cname', 'id')
    for s in signs:
        signed_num = len(models.SignInfo.objects.filter(cid__cid__cid=s['cid__cid'], cid__id=s['id']))
        unsigned_num = len(models.StuToCourse.objects.filter(cid__cid=s['cid__cid']))
        if unsigned_num <= 0:
            unsigned_num = 0
            signed_num = 0
        s['allsign_num'] = unsigned_num
        s['signed_num'] = signed_num
        s['id'] = str(s['id'])
    
    counts = len(signs)
    page = request.GET.get('page', 1)
    search = request.GET.get('search', '')
    page_obj = u.Pagination(current_page=page, all_count=counts, per_page_num=8, search_str=search)
    context = {
        'info' : tinfo,
        'signed' : signs[page_obj.start:page_obj.end],
        'page_obj' : page_obj,
        'current_page' : page,
        'search' : search,
        'counts' : counts
    }
    context['host'] = request.get_host()
    return render(request, 'AdminLTE/signed_info.html', context)

# 签到详情
def signed_info_detail(request, cousignid):
    v = request.COOKIES.get('log_t')
    t_id = models.Teacher.objects.get(tid=str(v))
    signed = []
    cid = models.CouSignInfo.objects.get(id=uuid.UUID(cousignid))
    courses = models.Course.objects.filter(tid=t_id, cid=cid.cid.cid)
    # print(courses)
    #cnt = 0
    for course_0 in courses:
        course_id = str(course_0.cid)
        course_name = models.Course.objects.get(cid=course_id).cname
        # print(course_name)
        signeds = models.SignInfo.objects.filter(cid__id=uuid.UUID(cousignid)).values('sid__sid', 'sid__sname', 'signtime')
        print(signeds)
        # print(signeds)
        for signed_0 in signeds:
            s_id = signed_0
            s_name = s_id['sid__sname']
            s_tump = [course_name + course_id, s_id['signtime'], s_id['sid__sid'], s_name]
            # print(s_tump)
            # for debug:
            # for i in range(1, 20):
            #     s_tump[3] = s_name + str(cnt)
            #     cnt += 1
            signed.append(s_tump)
    counts = len(signed)
    # print(signed[0])
    page = request.GET.get('page', 1)
    search = request.GET.get('search', '')
    signed_filt = []
    if len(search.strip()) != 0:
        for si in signed:
            for i in range(0, 4):
                if search.strip() in str(si[i]):
                    signed_filt.append(si)
                    break
        counts = len(signed_filt)
    else:
        signed_filt = signed
    page_obj = u.Pagination(per_page_num=8, current_page=page, all_count=counts, search_str=search)
    context = {
        'info' : t_id,
        'signed' : signed_filt,
        'counts' : counts,
        'page_obj' : page_obj,
        'current_page' : page,
        'search' : search,
        'uuid' : cousignid
    }
    context["signed"] = context["signed"][page_obj.start:page_obj.end]
    # print(context["signed"])
    return render(request, 'AdminLTE/signed_info_detail.html', context)

# 未签到详情
def unsigned_detail(request, cousignid):
    v = request.COOKIES.get('log_t')
    t_id = models.Teacher.objects.get(tid=str(v))
    cousign = models.CouSignInfo.objects.get(id=uuid.UUID(cousignid))
    sign_info = models.SignInfo.objects.filter(cid__id=uuid.UUID(cousignid)).values('sid__sid')
    stu_to_cou = models.StuToCourse.objects.filter(cid__cid=cousign.cid.cid).values('sid__sid')
    unsign_stu = models.Student.objects.filter(sid__in=stu_to_cou).exclude(sid__in=sign_info).values('sid', 'sname')
    
    context = {
        'info' : t_id,
        'uuid' : cousignid,
        'stu' : unsign_stu,
        'cname' : cousign.cid.cname + cousign.cid.cid
    }
        
    return render(request, 'AdminLTE/unsigned_info_detail.html', context)

# 教师发布签到页面
def publish_sign(request):
    v = request.COOKIES.get('log_t')
    info = models.Teacher.objects.get(tid=str(v))
    cou = models.Course.objects.filter(tid__tid=str(v))
    context = {
        'info' : info,
        'cou' : cou
    }
    return render(request, 'AdminLTE/publish_sign.html', context)

# 发布签到页面表单
def publish_form(request, cid):
    v = request.COOKIES.get('log_t')
    info = models.Teacher.objects.get(tid=str(v))
    context = {
        'info' : info,
        'cid' : cid
    }
    return render(request, 'AdminLTE/class_form.html', context)

# 教师发布签到页面
# 还需要加入权限判断 只有老师能访问该页面 目前测试阶段暂不加
def create_sign(request, cid):
    context = {}
    request.encoding = 'utf-8'
    tfmt = "YYYY-MM-DD-hh:mm:ss-ZZZ"
    if request.POST:
        utc = arrow.get(request.POST['start']+":00-Asia/Shanghai", tfmt)
        context['starttime'] = utc.datetime
        utc = arrow.get(request.POST['end']+":00-Asia/Shanghai", tfmt)
        context['endtime'] = utc.datetime
        context['cousign'] = u.set_sign(cid, context['starttime'], context['endtime'])
        context['host'] = request.get_host()
        print(context['starttime'])
        print(context['endtime'])
    return render(request, 'publish_alert.html', context)


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
import datetime
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
    return render(request, 'publish_test.html', context)


# 学生签到界面
def sign_page(request, cousign):
    sid = str(request.COOKIES.get('log_s'))
    cou = u.parse_UUID(cousign)
    context = {}
    try:
        stu = models.Student.objects.get(sid = sid)
        cousignid = models.CouSignInfo.objects.get(id = uuid.UUID(cousign))
        context = u.student_sign(str(sid), cousignid.cid.cid, cousignid)
        print(str(cousignid.id))
        print(context)
        request.session['signinfo'] = context
        request.session['signflag'] = True
        #print(request.session['signflag'])
        return redirect('/student')
    except Exception as e:
        print(e)
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
    courses = models.Course.objects.filter(tid__tid=id).values('cid', 'cname')
    cid = []
    rloc = []
    cname = []
    ctime = []
    for cou in courses:
        time_loc = models.CouOnClass.objects.filter(cid__cid=cou['cid']).values('ctime', 'rid__rloc', 'cday')
        for t_l in time_loc:
            class_time = t_l['ctime']
            print(class_time)
            print(type(class_time))
            class_day = (int(t_l['cday'])+1) % 7
            now_time = datetime.datetime.now()
            # print(str(class_day) + ' / ' + now_time.strftime("%w"))
            if str(class_day) == now_time.strftime("%w"):
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
        signeds = models.SignInfo.objects.filter(cid__cid__cid=course_id).values('sid__sid', 'sid__sname', 'signtime')
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
    print(search)
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
    }
    context["signed"] = context["signed"][page_obj.start:page_obj.end]
    # print(context["signed"])
    return render(request, 'AdminLTE/signed_info_detail.html', context)


def super(request):
    v = request.COOKIES.get('log_t')
    info = models.Teacher.objects.get(tid=str(v))
    teachers = models.Teacher.objects.all()
    classrooms = models.Classroom.objects.all()
    courses = models.Course.objects.all()
    courses_on_class = models.CouOnClass.objects.all().values('cid__cid', 'cid__cname', 'rid__rloc', 'cid__tid__tid', 'cid__tid__tname', 'cday', 'ctime')
    times = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    has_times = [
        ("0", '周一'),
        ("1", '周二'),
        ("2", '周三'),
        ("3", '周四'),
        ("4", '周五'),
        ("5", '周六'),
        ("6", '周日'),
    ]
    print(courses_on_class.values('cday'))
    clocks = ['08:00', '09:50', '14:00', '15:50', '18:30']
    # print(courses_on_class)
    context = {
        'info': info,
        'teachers': teachers,
        'classrooms': classrooms,
        'courses': courses,
        'times': times,
        'has_times': has_times,
        'clocks': clocks,
        'courses_on_class': courses_on_class,
    }
    return render(request, 'AdminLTE/super.html', context)


def add_course(request):
    pass


def del_course(request):
    pass

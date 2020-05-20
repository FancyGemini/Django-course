from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.core import exceptions

from background import models
from background import utils as u

import datetime, time

def super(request):
    v = request.COOKIES.get('log_t')
    info = models.Teacher.objects.get(tid=str(v))
    teachers = models.Teacher.objects.all()
    classrooms = models.Classroom.objects.all()
    courses = models.Course.objects.all()
    courses_on_class = models.CouOnClass.objects.all().values('id', 'cid__cid', 'cid__cname', 'rid__rloc', 'cid__tid__tid', 'cid__tid__tname', 'cday', 'ctime').order_by('cid__cid')
    times = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    has_times = [
        ("1", '周一'),
        ("2", '周二'),
        ("3", '周三'),
        ("4", '周四'),
        ("5", '周五'),
        ("6", '周六'),
        ("7", '周日'),
    ]
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
    request.encoding = 'utf-8'
    time_dict = {
        "1" : datetime.time(8, 0, 0),
        "2" : datetime.time(9, 50, 0),
        "3" : datetime.time(14, 0, 0),
        "4" : datetime.time(15, 50, 0),
        "5" : datetime.time(18, 30, 0)
    }
    if request.POST:
        print(time_dict[request.POST['time']])
        cid = models.Course.objects.get(cid=request.POST['course'])
        rid = models.Classroom.objects.get(rid=request.POST['room'])
        models.CouOnClass.objects.create(ctime=time_dict[request.POST['time']], cid=cid, rid=rid, cday=request.POST['day'])
        return HttpResponse("<script>alert(\"添加成功！\");window.location.href=\"..\";</script>")
    return HttpResponse("<script>alert(\"添加失败！\");window.location.href=\"..\";</script>")


def edit_course(request, id):
    v = request.COOKIES.get('log_t')
    info = models.Teacher.objects.get(tid=str(v))
    cou_on_class = models.CouOnClass.objects.get(id=str(id))
    all_room = models.Classroom.objects.all()
    all_teacher = models.Teacher.objects.all()
    day = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    clock = ['08:00', '09:50', '14:00', '15:50', '18:30']
    context = {
        'cou' : cou_on_class,
        'all_room' : all_room,
        'all_teacher' : all_teacher,
        'day' : day,
        'clocks' : clock,
        'info' : info
    }
    return render(request, 'AdminLTE/edit_course.html', context)

def edit_course_detail(request):
    time_dict = {
        "1" : datetime.time(8, 0, 0),
        "2" : datetime.time(9, 50, 0),
        "3" : datetime.time(14, 0, 0),
        "4" : datetime.time(15, 50, 0),
        "5" : datetime.time(18, 30, 0)
    }
    if request.POST:
        cou_on_class = models.CouOnClass.objects.get(id=request.POST['id'])
        cou_on_class.rid = models.Classroom.objects.get(rid=request.POST['room'])
        cou_on_class.ctime = time_dict[request.POST['time']]
        cou_on_class.cday = request.POST['day']
        cou_on_class.save()
        return HttpResponse("<script>alert(\"编辑成功！\");window.location.href=\"..\";</script>")
    return HttpResponse("<script>alert(\"编辑失败！\");window.location.href=\"..\";</script>")

# 删除上课信息
def del_couonclass(request, id):
    try:
        models.CouOnClass.objects.get(id=id).delete()
        return HttpResponse("<script>alert(\"删除成功！\");window.location.href=\"../..\";</script>")
    except Exception:
        return HttpResponse("<script>alert(\"删除失败！\");window.location.href=\"../..\";</script>")

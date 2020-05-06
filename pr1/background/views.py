# coding:utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib import messages
from io import BytesIO
from background import models
from django.core.exceptions import ObjectDoesNotExist
import qrcode

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
            messages.error(request, '你输入的账户不存在！')
            return redirect('/')
    messages.error(request, '你输入的密码不正确！')
    return redirect('/')

# 测试用
def class_test(request):
    class_list = models.Course.objects.all().values('cid', 'cname', 'tid__tname')
    #print(class_list)
    context = {
        'all_class' : class_list,
    }
    
    return render(request, 'class.html', context)

# 测试用
def qianndao_test(request, cid):
    context = {
        'cid' : cid,
    }
    return render(request, 'qiandao.html', context)

# 还需要添加过滤功能 只有存在的课程才允许生成二维码
def get_qrcode(request, cid):
    cou = models.Course.objects.filter(cid = str(cid))
    if cou.exists():
        img = qrcode.make(str(cid))
        buf = BytesIO()
        img.save(buf)
        img_stream = buf.getvalue()
        return HttpResponse(img_stream, content_type='image/png')
    else:
        return HttpResponse('')



def index(request):
    return render(request, 'AdminLTE/index.html')


def index2(request):
    return render(request, 'AdminLTE/index2.html')


def index3(request):
    return render(request, 'AdminLTE/index3.html')


def starter(request):
    return render(request, 'AdminLTE/starter.html')

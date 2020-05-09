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
# import pyzbar.pyzbar as pyzbar
# import cv2


def home(request):
    return render(request, 'home.html')


def check_cookies(request):
    is_stu = True
    v = request.COOKIES.get('log_s')
    if not v:
        v = request.COOKIES.get('log_t')
        if not v:
            return False
        else:
            is_stu = False
    return True



def signin(request):
    if check_cookies(request):
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


# 拟在这里实现利用摄像头扫描并识别二维码的功能
# 注释部分为网上找到的相关模板（未运行过）
def call_camera(request):
    pass
'''    def decodeDisplay(img):
        barcodes = pyzbar.decode(image)
        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            cv2.rectangle(image, (x,y), (x + w, y + h), (0, 255, 0), 2)
            barcodeData = barcode.data.decode("UTF-8")
            barcodeType = barcode.barcodeType
            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, .5, (225, 225, 225), 2)
        return image
    def detect():
        camera = cv2.VideoCapture(0)
        whlie(True):
            ret, frame = camera.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            im = decodeDisplay(gray)
            cv2.waitKey(5)
            cv2.imshow("camera", im)
            if cv2.waitKey(1) == ord('Q'):
                break
        camera.release()
        cv2.destroyAllWindows()
    if __name__ == '__main__':
        detect()'''

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

# 创建课程签到信息函数
def set_sign(cid, time_start, time_end, debug=False):
    course = models.Course.objects.get(cid=cid)
    cousign_info = models.CouSignInfo.objects.filter(cid__cid=cid, timeend__gt=time_start)
    # 测试用
    if debug:
        return models.CouSignInfo.objects.create(cid=course, timestart=time_start, timeend=time_end)
    
    # 如果开始时间大于结束时间 或 还有正在进行中的签到 不予继续创建签到
    if time_start > time_end or cousign_info.exists():
        return None
    
    cousign = models.CouSignInfo.objects.create(cid=course, timestart=time_start, timeend=time_end)
    return cousign

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
        context['cousign'] = set_sign(cid, context['starttime'], context['endtime'])
        context['host'] = request.get_host()
    return render(request, 'publish_test.html', context)

# 学生签到函数
def student_sign(stuid, couid, cousignid, debug=False):
    stu = models.StuToCourse.objects.get(sid__sid=stuid, cid__cid=couid)
    
    # 测试用
    if debug:
        models.SignInfo.objects.create(sid=stu.sid, cid=stu.cid)
    
    if stu.exists():
        # 获取课程详细信息
        time = datetime.datetime.now()
        if time >= cousignid.timestart and time <=cousignid.timeend :
            # 写入签到信息
            models.SignInfo.objects.create(sid=stu.sid, cid=stu.cid)
            return True
    return False

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


def student(request):
    v = request.COOKIES.get('log_s')
    id = str(v)
    info = models.Student.objects.get(sid=id)
    courses = models.StuToCourse.objects.filter(sid=id)
    # context = {'info':info, 'courses':[], 'locations':[]}
    context = {'info':info, 'courses':[]}
    for cou in courses:
        cou_id = cou.cid
        cou_id = str(cou_id)
        print(cou_id)
        cou_name = models.Course.objects.get(cid=cou_id).cname
        cou_name = str(cou_name)
        context['courses'].append(cou_name)
        # today = timezone.now().date()
        # room_loc = models.CouOnClass.objects.get(Q(cid=cou_id) & Q(ctime-today=timedelta(days=0))).rid__rloc
        # room_loc = str(room_loc)
        # context['room_loc'].append(room_loc)
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
    return render(request, 'AdminLTE/teacher.html')


def super(request):
    return render(request, 'AdminLTE/super.html')


def index(request):
    return render(request, 'AdminLTE/index.html')

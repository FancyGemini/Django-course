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
    context={'info':info}
    return render(request, 'AdminLTE/student_course.html', context)



def teacher(request):
    return render(request, 'AdminLTE/teacher.html')


def super(request):
    return render(request, 'AdminLTE/super.html')


def index(request):
    return render(request, 'AdminLTE/index.html')

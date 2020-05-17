"""pr1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import re_path
from background import views as bg
from django.conf.urls import handler404
from django.conf.urls import handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', bg.home, name='home'),
    path('', bg.signin, name='login'),
    path('logout/', bg.logout, name='logout'),
    path('student/', bg.student, name='student'),
    path('student_course/', bg.student_course, name='student_course'),
    path('teacher_course/', bg.teacher_course, name='teacher_course'),
    path('sign_info/', bg.sign_info, name='signed_info'),
    re_path(r'sign_info/signed_info_detail/(\w{8}-\w{4}-\w{4}-\w{4}-\w{12})/', bg.signed_info_detail, name='signed_info_detail'),
    re_path(r'sign_info/unsigned_detail/(\w{8}-\w{4}-\w{4}-\w{4}-\w{12})/', bg.unsigned_detail, name='unsigned_detail'),
    path('teacher/', bg.teacher, name='teacher'),
    path('super/', bg.super, name='super'),
    path('super/add_course/', bg.add_course, name='add_course'),
    re_path(r'super/edit_course/(\d+)/', bg.edit_course, name='edit_course'),
    path('super/edit_course_detail/', bg.edit_course_detail, name='edit_detail'),
    re_path(r'super/del_cou_class/(\d+)/', bg.del_couonclass, name='del_cou_class'),
    path('waiting/', bg.waiting, name='waiting'),
    path('classtest/', bg.class_test, name='class'),
    path('publish_sign/', bg.publish_sign, name='publish_sign'),
    re_path(r'publish_sign/publish_form/(\d+)/', bg.publish_form, name='publish_form'),
    re_path(r'publish_sign/publish_form/publish/(\d+)/', bg.create_sign, name='publish'),
    re_path(r'qiandao/(\d+)', bg.qianndao_test),
    re_path(r'qrcode/(\w{8}-\w{4}-\w{4}-\w{4}-\w{12})', bg.get_qrcode),
    re_path(r'student/sign/(\w{8}-\w{4}-\w{4}-\w{4}-\w{12})', bg.sign_page),
]

handler404 = bg.page_not_found
handler500 = bg.page_error

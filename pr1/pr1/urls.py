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
from background import views, student_views, teacher_views, super_views
from django.conf.urls import handler404
from django.conf.urls import handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('', views.signin, name='login'),
    path('logout/', views.logout, name='logout'),
    path('student/', student_views.student, name='student'),
    path('student_course/', student_views.student_course, name='student_course'),
    path('teacher_course/', teacher_views.teacher_course, name='teacher_course'),
    path('sign_info/', teacher_views.sign_info, name='signed_info'),
    re_path(r'sign_info/signed_info_detail/(\w{8}-\w{4}-\w{4}-\w{4}-\w{12})/', teacher_views.signed_info_detail, name='signed_info_detail'),
    re_path(r'sign_info/unsigned_detail/(\w{8}-\w{4}-\w{4}-\w{4}-\w{12})/', teacher_views.unsigned_detail, name='unsigned_detail'),
    path('teacher/', teacher_views.teacher, name='teacher'),
    path('super/', super_views.super, name='super'),
    path('super/add_course/', super_views.add_course, name='add_course'),
    re_path(r'super/edit_course/(\d+)/', super_views.edit_course, name='edit_course'),
    path('super/edit_course_detail/', super_views.edit_course_detail, name='edit_detail'),
    re_path(r'super/del_cou_class/(\d+)/', super_views.del_couonclass, name='del_cou_class'),
    path('waiting/', views.waiting, name='waiting'),
    path('classtest/', views.class_test, name='class'),
    path('publish_sign/', teacher_views.publish_sign, name='publish_sign'),
    re_path(r'publish_sign/publish_form/(\d+)/', teacher_views.publish_form, name='publish_form'),
    re_path(r'publish_sign/publish_form/publish/(\d+)/', teacher_views.create_sign, name='publish'),
    re_path(r'qiandao/(\d+)', views.qianndao_test),
    re_path(r'qrcode/(\w{8}-\w{4}-\w{4}-\w{4}-\w{12}).png', views.get_qrcode, name='get_qrcode'),
    re_path(r'student/sign/(\w{8}-\w{4}-\w{4}-\w{4}-\w{12})', student_views.sign_page),
]

handler404 = views.page_not_found
handler500 = views.page_error

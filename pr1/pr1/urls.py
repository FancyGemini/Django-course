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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', bg.home, name='home'),
    path('', bg.signin, name='login'),
    path('logout/', bg.logout, name='logout'),
    path('index/', bg.index, name='index'),
    path('student/', bg.student, name='student'),
    path('student_course/', bg.student_course, name='student_course'),
    path('teacher/', bg.teacher, name='teacher'),
    path('super/', bg.super, name='super'),
    path('waiting/', bg.waiting, name='waiting'),
    path('classtest/', bg.class_test, name='class'),
    re_path(r'class_form/(\d+)', bg.classform),
    re_path(r'publish/(\d+)', bg.publish_sign),
    re_path(r'qiandao/(\d+)', bg.qianndao_test),
    re_path(r'qrcode/(\d+)', bg.get_qrcode),
]

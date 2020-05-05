# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse


def teacher(request):
    pass


def student(request):
    pass


def home(request):
    return render(request, 'home.html')


def signin(request):
    return render(request, 'Sign In.html')


def index(request):
    return render(request, 'AdminLTE/index.html')


def index2(request):
    return render(request, 'AdminLTE/index2.html')


def index3(request):
    return render(request, 'AdminLTE/index3.html')


def starter(request):
    return render(request, 'AdminLTE/starter.html')

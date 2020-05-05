from django.contrib import admin
from background.models import Student, Teacher, Course, Classroom

# Register your models here.

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # 显示哪些属性
    list_display = ('sid', 'sname', 'age', 'gender')
    # 哪些可以点进去
    list_display_links = ('sid', 'sname')
    
# 注册其他模型
admin.site.register([Teacher, Course, Classroom])

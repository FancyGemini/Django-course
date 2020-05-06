from django.contrib import admin
from background.models import Student, Teacher, Course, Classroom, StuToCourse, CouOnClass, SignInfo

# Register your models here.

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # 显示哪些属性
    list_display = ('sid', 'sname', 'age', 'gender')
    # 哪些可以点进去
    list_display_links = ('sid', 'sname')
    
@admin.register(CouOnClass)
class CouOnClassAdmin(admin.ModelAdmin):
    list_display = ('cid', 'rid', 'cday', 'ctime')
    
@admin.register(StuToCourse)
class StuToCouAdmin(admin.ModelAdmin):
    list_display = ('sid', 'cid')
    
@admin.register(SignInfo)
class SignInfoAdmin(admin.ModelAdmin):
    list_display = ('sid', 'cid', 'signtime')
    
# 注册其他模型
admin.site.register([Teacher, Course, Classroom])

from django.db import models
from django.utils import timezone

# Create your models here.

# ------------------------
# student table

class Student(models.Model):
    objects = models.Manager()

    GENDER = {
        ('male', '男'),
        ('female', '女'),
        ('secret', '保密')
    }

    sid = models.CharField('学生id', max_length=13, unique=True, blank=False)
    sname = models.CharField('学生姓名', max_length=50, blank=False)
    age = models.IntegerField('年龄', default=0)
    gender = models.CharField('性别', choices=GENDER, max_length=6, default='secret')
    spasswd = models.CharField('登陆密码', max_length=50, blank=False, default='123456')


    class Meta:
        verbose_name = '学生信息'
        verbose_name_plural = '学生信息'

    def __str__(self):
        return self.sname

# --------------------------
# teacher table

class Teacher(models.Model):
    objects = models.Manager()

    tid = models.CharField('教师id', max_length=13, unique=True, blank=False)
    tname = models.CharField('教师姓名', max_length=50, blank=False)
    tpasswd = models.CharField('登陆密码', max_length=50, blank=False, default='123456')


    class Meta:
        verbose_name = '教师信息'
        verbose_name_plural = '教师信息'

    def __str__(self):
        return self.tname

# --------------------------
# course table

class Course(models.Model):
    objects = models.Manager()

    cid = models.CharField('课程id', max_length=13, unique=True, blank=False)
    cname = models.CharField('课程名称', max_length=50, blank=True)
    credit = models.IntegerField('学分', blank=False, default=0)
    tid = models.ForeignKey('Teacher', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '课程信息'
        verbose_name_plural = '课程信息'

    def __str__(self):
        return self.cname

# --------------------------
# courses student chosen table

class StuToCourse(models.Model):
    objects = models.Manager()

    sid = models.ForeignKey('Student', on_delete=models.CASCADE)
    cid = models.ForeignKey('Course', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '选课信息'
        verbose_name_plural = '选课信息'

    def __str__(self):
        return self.sid.sname

# --------------------------
# classroom table

class Classroom(models.Model):
    objects = models.Manager()

    rid = models.CharField('教室id', max_length=13, blank=False)
    rloc = models.CharField('教室位置', max_length=50, blank=False)

    class Meta:
        verbose_name = '教室信息'
        verbose_name_plural = '教室信息'

    def __str__(self):
        return self.rloc

# --------------------------
# courses on class table

class CouOnClass(models.Model):
    objects = models.Manager()

    cid = models.ForeignKey('Course', on_delete=models.CASCADE)
    rid = models.ForeignKey('Classroom', on_delete=models.CASCADE)
    ctime = models.TimeField('上课时间', blank=False, default=timezone.now)

    class Meta:
        verbose_name = '上课信息'
        verbose_name_plural = '上课信息'

    def __str__(self):
        return self.cid.cname


# --------------------------
# sign info table

class SignInfo(models.Model):
    objects = models.Manager()
    
    sid = models.ForeignKey('Student', on_delete=models.CASCADE)
    cid = models.ForeignKey('CouOnClass', on_delete=models.CASCADE)
    # 签到时间 默认空 说明没进行签到 如果签到成功 则修改其值
    signtime = models.DateTimeField('签到时间', null=True, blank=True)
    
    class Meta:
        verbose_name = '签到信息'
        verbose_name_plural = '签到信息'
        
    def __str__(self):
        return self.sid.sname
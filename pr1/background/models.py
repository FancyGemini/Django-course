from django.db import models

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
    sname = models.CharField('学生姓名', max_length=50, blank=True)
    age = models.IntegerField('年龄', default=0)
    gender = models.CharField('性别', choices=GENDER, max_length=6, default='secret')
    spasswd = models.CharField('登陆密码', max_length=50, blank=False)

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
    tname = models.CharField('教师姓名', max_length=50, blank=True)
    tpasswd = models.CharField('登录密码', max_length=50, blank=False)

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
    credit = models.IntegerField('学分', default=0)
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
        return self.cid

# --------------------------
# classroom table

class Classroom(models.Model):
    objects = models.Manager()

    rloc = models.CharField('教室位置', max_length=50, blank=False)
    rid = models.CharField('教室id', max_length=50, blank=False)

    class Meta:
        verbose_name = '上课信息'
        verbose_name_plural = '上课信息'

    def __str__(self):
        return self.rid

# --------------------------
# courses on class table

class CouOnClass(models.Model):
    objects = models.Manager()

    rid = models.ForeignKey('Classroom', on_delete=models.CASCADE)
    ctime = models.CharField('上课时间', max_length=30, blank=False)
    cid = models.ForeignKey('Course', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '上课信息'
        verbose_name_plural = '上课信息'

    def __str__(self):
        return self.cid

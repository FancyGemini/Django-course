from django.db import models

# Create your models here.
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
    
    
    class Meta:
        verbose_name = '学生信息'
        verbose_name_plural = '学生信息'

    def __str__(self):
        return self.sname
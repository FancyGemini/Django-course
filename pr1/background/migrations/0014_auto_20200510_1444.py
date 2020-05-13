# Generated by Django 3.0.6 on 2020-05-10 06:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('background', '0013_auto_20200510_0050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='couonclass',
            name='cday',
            field=models.CharField(choices=[('1', '周一'), ('5', '周五'), ('3', '周三'), ('4', '周四'), ('2', '周二'), ('6', '周六'), ('0', '周日')], default='Mon', max_length=5, verbose_name='上课星期'),
        ),
        migrations.AlterField(
            model_name='cousigninfo',
            name='id',
            field=models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='student',
            name='gender',
            field=models.CharField(choices=[('secret', '保密'), ('female', '女'), ('male', '男')], default='secret', max_length=6, verbose_name='性别'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='tauth',
            field=models.CharField(choices=[('normal', '普通教师'), ('admin', '管理员')], default='normal', max_length=7, verbose_name='教师权限'),
        ),
    ]
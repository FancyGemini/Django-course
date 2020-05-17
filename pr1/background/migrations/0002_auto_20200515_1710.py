# Generated by Django 3.0.6 on 2020-05-15 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('background', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='couonclass',
            name='cday',
            field=models.CharField(choices=[('4', '周四'), ('1', '周一'), ('7', '周日'), ('2', '周二'), ('6', '周六'), ('3', '周三'), ('5', '周五')], default='Mon', max_length=5, verbose_name='上课星期'),
        ),
        migrations.AlterField(
            model_name='student',
            name='gender',
            field=models.CharField(choices=[('male', '男'), ('female', '女'), ('secret', '保密')], default='secret', max_length=6, verbose_name='性别'),
        ),
    ]

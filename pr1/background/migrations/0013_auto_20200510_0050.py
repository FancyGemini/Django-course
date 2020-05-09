# Generated by Django 3.0 on 2020-05-09 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('background', '0012_auto_20200509_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='couonclass',
            name='cday',
            field=models.CharField(choices=[('0', '周日'), ('2', '周二'), ('6', '周六'), ('5', '周五'), ('4', '周四'), ('1', '周一'), ('3', '周三')], default='Mon', max_length=5, verbose_name='上课星期'),
        ),
    ]

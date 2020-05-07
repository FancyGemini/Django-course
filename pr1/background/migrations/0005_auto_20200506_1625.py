# Generated by Django 3.0.5 on 2020-05-06 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('background', '0004_auto_20200506_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signinfo',
            name='signtime',
            field=models.DateTimeField(blank=True, null=True, verbose_name='签到时间'),
        ),
        migrations.AlterField(
            model_name='student',
            name='gender',
            field=models.CharField(choices=[('secret', '保密'), ('female', '女'), ('male', '男')], default='secret', max_length=6, verbose_name='性别'),
        ),
    ]
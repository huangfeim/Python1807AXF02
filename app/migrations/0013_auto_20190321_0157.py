# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-03-21 01:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20190319_0714'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='age',
            field=models.CharField(default='-1', max_length=50),
        ),
        migrations.AddField(
            model_name='user',
            name='birthday',
            field=models.CharField(default='-1', max_length=50),
        ),
        migrations.AddField(
            model_name='user',
            name='sex',
            field=models.CharField(default='-1', max_length=50),
        ),
        migrations.AddField(
            model_name='user',
            name='xingzuo',
            field=models.CharField(default='-1', max_length=50),
        ),
        migrations.AddField(
            model_name='user',
            name='xuexing',
            field=models.CharField(default='-1', max_length=50),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-30 11:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hoteltable',
            name='roomtypes',
        ),
    ]

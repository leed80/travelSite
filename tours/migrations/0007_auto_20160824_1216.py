# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-24 12:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tours', '0006_auto_20160824_1209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tourtable',
            name='travelClass',
            field=models.CharField(max_length=40),
        ),
    ]

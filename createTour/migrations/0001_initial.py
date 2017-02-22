# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('countryid', models.IntegerField(default=0)),
                ('name', models.CharField(default='unknown', max_length=100)),
                ('description', models.TextField(max_length=10000)),
                ('lat', models.FloatField(default=11.111, max_length=10000)),
                ('lng', models.FloatField(default=111.111, max_length=10000)),
                ('zoom', models.IntegerField(default=4, max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='destination',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('destinationid', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=100)),
                ('countryid', models.IntegerField(default=1)),
                ('description', models.TextField(max_length=10000)),
                ('lat', models.FloatField(default=11.111, max_length=10000)),
                ('lng', models.FloatField(default=111.111, max_length=10000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='hotel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=10000)),
                ('destinationid', models.IntegerField(default=1)),
                ('rating', models.IntegerField(default=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='activities',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('refNumber', models.CharField(max_length=40)),
                ('title', models.CharField(max_length=40)),
                ('description', models.TextField(max_length=10000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='hotelRoomTypes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('refNumber', models.CharField(max_length=40)),
                ('title', models.CharField(max_length=100)),
                ('beds', models.CharField(max_length=100)),
                ('amenities', models.TextField(max_length=10000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='hotelTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('refNumber', models.CharField(max_length=40)),
                ('title', models.CharField(max_length=40)),
                ('description', models.TextField(max_length=10000)),
                ('stop', models.CharField(max_length=40)),
                ('travelClass', models.CharField(max_length=40)),
                ('eanhotelid', models.IntegerField()),
                ('address', models.CharField(max_length=40)),
                ('location', models.CharField(max_length=40)),
                ('amenities', models.TextField(max_length=10000)),
                ('policies', models.TextField(max_length=10000)),
                ('roomtypecode', models.IntegerField()),
                ('ratecode', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='stopTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('refNumber', models.CharField(max_length=40)),
                ('title', models.CharField(max_length=40)),
                ('description', models.TextField(max_length=10000)),
                ('lengthofstay', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='tourTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('refNumber', models.CharField(max_length=40)),
                ('title', models.CharField(max_length=40)),
                ('description', models.TextField(max_length=10000)),
                ('country', models.CharField(max_length=40)),
                ('travelClass', models.CharField(max_length=40)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='stoptable',
            name='tour',
            field=models.ForeignKey(to='createTour.tourTable'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hotelroomtypes',
            name='hotel',
            field=models.ForeignKey(to='createTour.hotelTable'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='activities',
            name='stop',
            field=models.ForeignKey(to='createTour.stopTable'),
            preserve_default=True,
        ),
    ]

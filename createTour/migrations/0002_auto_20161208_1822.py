# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('createTour', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', django_countries.fields.CountryField(max_length=2)),
                ('description', models.TextField(max_length=10000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='destination',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=10000)),
                ('countryid', models.ForeignKey(to='createTour.country')),
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
                ('destinationid', models.ForeignKey(to='createTour.destination')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='activities',
            name='stop',
        ),
        migrations.DeleteModel(
            name='activities',
        ),
        migrations.RemoveField(
            model_name='hotelroomtypes',
            name='hotel',
        ),
        migrations.DeleteModel(
            name='hotelRoomTypes',
        ),
        migrations.DeleteModel(
            name='hotelTable',
        ),
        migrations.RemoveField(
            model_name='stoptable',
            name='tour',
        ),
        migrations.DeleteModel(
            name='stopTable',
        ),
        migrations.DeleteModel(
            name='tourTable',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-21 08:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country_test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_id', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=200)),
                ('maproute', models.CharField(max_length=500)),
                ('description', models.CharField(max_length=10000)),
                ('author', models.CharField(default=b'nothing here', max_length=10000)),
                ('author_website', models.CharField(default=b'nothing here', max_length=10000)),
                ('author_url', models.CharField(default=b'nothing here', max_length=10000)),
                ('latitude', models.FloatField(default=1.0)),
                ('longitude', models.FloatField(default=1.0)),
            ],
        ),
        migrations.CreateModel(
            name='Regions_test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region_id', models.IntegerField(blank=True, null=True)),
                ('country_id', models.IntegerField()),
                ('regionname', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Towns_test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region_id', models.IntegerField()),
                ('townname', models.CharField(max_length=500)),
                ('latitude', models.FloatField(default=1.0)),
                ('longitude', models.FloatField(default=1.0)),
            ],
        ),
        migrations.CreateModel(
            name='Towns_test_desc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('townname', models.CharField(max_length=500)),
                ('description', models.CharField(max_length=10000)),
                ('author', models.CharField(max_length=10000)),
                ('author_website', models.CharField(default=b'nothing here', max_length=10000)),
                ('author_url', models.CharField(default=b'nothing here', max_length=10000)),
            ],
        ),
    ]
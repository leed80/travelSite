# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-31 14:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activation_key', models.CharField(blank=True, max_length=40)),
                ('status', models.CharField(max_length=200)),
                ('country', django_countries.fields.CountryField(default=b'gb', max_length=2)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
                'verbose_name_plural': 'User profiles',
            },
        ),
    ]

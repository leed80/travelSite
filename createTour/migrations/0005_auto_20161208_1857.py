# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('createTour', '0004_auto_20161208_1855'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='countryid',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='destination',
            name='destinationid',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('createTour', '0003_hotel_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destination',
            name='countryid',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='destinationid',
            field=models.IntegerField(default=1),
        ),
    ]

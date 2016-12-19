# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('createTour', '0002_auto_20161208_1822'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='rating',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]

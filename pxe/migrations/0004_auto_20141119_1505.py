# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pxe', '0003_auto_20141119_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='install',
            name='day',
            field=models.DateField(default=datetime.datetime(2014, 11, 19, 15, 5, 39, 176000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='online',
            name='status',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]

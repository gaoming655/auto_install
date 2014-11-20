# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pxe', '0004_auto_20141119_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disk_sotl',
            name='sotl',
            field=models.IntegerField(max_length=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='install',
            name='day',
            field=models.DateField(default=datetime.datetime(2014, 11, 19, 15, 40, 33, 437000)),
            preserve_default=True,
        ),
    ]

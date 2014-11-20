# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pxe', '0002_auto_20141119_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='install',
            name='day',
            field=models.DateField(default=datetime.datetime(2014, 11, 19, 15, 4, 14, 695000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='online',
            name='sn',
            field=models.CharField(unique=True, max_length=100),
            preserve_default=True,
        ),
    ]

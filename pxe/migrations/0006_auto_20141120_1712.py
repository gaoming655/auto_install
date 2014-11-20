# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pxe', '0005_auto_20141119_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='online',
            name='stripe',
            field=models.IntegerField(default=b'1024', max_length=10, choices=[(1024, b'1M'), (64, b'64K'), (512, b'512K')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='install',
            name='day',
            field=models.DateField(default=datetime.datetime(2014, 11, 20, 17, 12, 9, 289000)),
            preserve_default=True,
        ),
    ]

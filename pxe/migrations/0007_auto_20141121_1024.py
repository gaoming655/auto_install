# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pxe', '0006_auto_20141120_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='install',
            name='day',
            field=models.DateField(default=datetime.datetime(2014, 11, 21, 10, 24, 26, 76000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='online',
            name='level',
            field=models.IntegerField(default=1, max_length=2, choices=[(1, b'raid1'), (0, b'raid0'), (5, b'raid5')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='online',
            name='stripe',
            field=models.IntegerField(default=b'1024', max_length=10, choices=[(1024, b'1M'), (512, b'512K'), (128, b'128K'), (64, b'64K')]),
            preserve_default=True,
        ),
    ]

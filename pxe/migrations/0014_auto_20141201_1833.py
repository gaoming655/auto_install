# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pxe', '0013_auto_20141127_1659'),
    ]

    operations = [
        migrations.AddField(
            model_name='online',
            name='jindu',
            field=models.IntegerField(default=0, max_length=3),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='install',
            name='day',
            field=models.DateField(default=datetime.datetime(2014, 12, 1, 18, 33, 0, 339000)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='online',
            name='service_netmask',
            field=models.CharField(default=b'255.255.255.0', max_length=30, choices=[(b'255.255.255.0', b'24\xe4\xbd\x8d'), (b'255.255.0.0', b'16\xe4\xbd\x8d')]),
            preserve_default=True,
        ),
    ]

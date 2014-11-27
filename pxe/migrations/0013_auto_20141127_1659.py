# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pxe', '0012_auto_20141127_1302'),
    ]

    operations = [
        migrations.AddField(
            model_name='online',
            name='service_gw',
            field=models.IPAddressField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='online',
            name='service_ip',
            field=models.IPAddressField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='online',
            name='service_netmask',
            field=models.CharField(default=b'255.255.255.0', max_length=30, choices=[(b'255.255.255.0', b'24'), (b'255.255.0.0', b'16')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='install',
            name='day',
            field=models.DateField(default=datetime.datetime(2014, 11, 27, 16, 59, 41, 595000)),
            preserve_default=True,
        ),
    ]

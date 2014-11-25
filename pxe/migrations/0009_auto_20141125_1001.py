# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pxe', '0008_auto_20141124_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='install',
            name='ilo_ip',
            field=models.IPAddressField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='install',
            name='day',
            field=models.DateField(default=datetime.datetime(2014, 11, 25, 10, 1, 58, 877000)),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pxe', '0010_auto_20141125_1353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='install',
            name='day',
            field=models.DateField(default=datetime.datetime(2014, 11, 25, 13, 55, 2, 463000)),
            preserve_default=True,
        ),
    ]

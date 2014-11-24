# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pxe', '0007_auto_20141121_1024'),
    ]

    operations = [
        migrations.CreateModel(
            name='ilo_table',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('maunfacturer', models.CharField(max_length=100)),
                ('lan_num', models.IntegerField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='install',
            name='day',
            field=models.DateField(default=datetime.datetime(2014, 11, 24, 15, 20, 33, 155000)),
            preserve_default=True,
        ),
    ]

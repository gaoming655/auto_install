# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pxe', '0011_auto_20141125_1355'),
    ]

    operations = [
        migrations.CreateModel(
            name='disk_hp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sotl', models.CharField(max_length=20)),
                ('size', models.CharField(max_length=20)),
                ('host_id', models.IntegerField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='install',
            name='cpu',
            field=models.CharField(max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='install',
            name='day',
            field=models.DateField(default=datetime.datetime(2014, 11, 27, 13, 2, 54, 270000)),
            preserve_default=True,
        ),
    ]

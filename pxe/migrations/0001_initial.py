# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='disk_sotl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sotl', models.CharField(max_length=2)),
                ('size', models.CharField(max_length=10)),
                ('host_id', models.IntegerField(max_length=20)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='install',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('inc', models.CharField(max_length=30)),
                ('ipaddr', models.IPAddressField()),
                ('sn', models.CharField(max_length=20)),
                ('status', models.BooleanField(default=True, choices=[(False, b'\xe4\xb8\x8d\xe5\x8f\xaf\xe5\xae\x89\xe8\xa3\x85'), (True, b'\xe5\x8f\xaf\xe5\xae\x89\xe8\xa3\x85')])),
                ('day', models.DateField(default=datetime.datetime(2014, 11, 19, 14, 55, 23, 712000))),
                ('cpu', models.CharField(max_length=40)),
                ('mem', models.CharField(max_length=20)),
                ('sotl', models.CharField(max_length=5)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='online',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.CharField(default=b'1', max_length=2, choices=[(1, b'raid1'), (0, b'raid0'), (5, b'raid5')])),
                ('ip', models.IPAddressField()),
                ('ilo_ip', models.IPAddressField(null=True, blank=True)),
                ('status', models.BooleanField(default=True)),
                ('inc', models.CharField(max_length=30)),
                ('sn', models.CharField(unique=True, max_length=20)),
                ('sotl_total', models.IntegerField(max_length=3)),
                ('raid_zh', models.CharField(max_length=200)),
                ('kickstart', models.CharField(default=b'conf.ks', max_length=30, choices=[(b'conf.ks', b'Centos6')])),
                ('finish_status', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

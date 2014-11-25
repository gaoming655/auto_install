#coding=utf-8
from django.db import models
import datetime
# Create your models here.
raid_chose = ((False,'不可安装'),(True,'可安装'))
raid_level = ((1,'raid1'),(0,'raid0'),(5,'raid5'))
ks_choices = (('conf.ks','Centos6'),)
stripe_choices = ((1024,'1M'),(512,'512K'),(128,'128K'),(64,'64K'))
class disk_sotl(models.Model):
    sotl = models.IntegerField(max_length=2)
    size = models.CharField(max_length=10)
    host_id = models.IntegerField(max_length=20)
    
class install(models.Model):
    inc = models.CharField(max_length=30)
    ilo_ip = models.IPAddressField(null=True,blank=True)
    ipaddr = models.IPAddressField()
    sn = models.CharField(max_length=100,unique=True)
    status = models.BooleanField(default=True,choices=raid_chose)
    day = models.DateField(default=datetime.datetime.now())
    cpu = models.CharField(max_length=100,)
    mem = models.CharField(max_length=20,)
    sotl = models.CharField(max_length=5)
    def __unicode__(self):
        return "%s " % self.ipaddr
class online(models.Model):
    level = models.IntegerField(max_length=2,choices=raid_level,blank=False,default=1)
    ip = models.IPAddressField()
    ilo_ip = models.IPAddressField(null=True,blank=True)
    status = models.BooleanField(default=False)
    inc = models.CharField(max_length=30)
    sn = models.CharField(max_length=100,unique=True)
    sotl_total = models.IntegerField(max_length=3)
    stripe = models.IntegerField(max_length=10,default='1024',blank=False,choices=stripe_choices)
    raid_zh = models.CharField(max_length=200,)
    kickstart = models.CharField(max_length=30,blank=False,default='conf.ks',choices=ks_choices)
    finish_status = models.BooleanField(default=False)
    def __unicode__(self):
        return "%s" % self.ip
    
class ilo_table(models.Model):
    maunfacturer = models.CharField(max_length=100,)
    lan_num = models.IntegerField(max_length=10,)
    def __unicode__(self):
        return "%s" % self.maunfacturer
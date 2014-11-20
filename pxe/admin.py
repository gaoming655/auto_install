from django.contrib import admin
from models import *

# Register your models here.



class Install_admin(admin.ModelAdmin):
    list_display=('id','ipaddr','inc','sn','status')
    
class Online_admin(admin.ModelAdmin):
    list_display = ('id','ip','level','ilo_ip','status','inc','sn')

class disk_sotl_admin(admin.ModelAdmin):
    list_display = ('sotl','size','host_id')
    
admin.site.register(install,Install_admin)
admin.site.register(online,Online_admin)
admin.site.register(disk_sotl,disk_sotl_admin)
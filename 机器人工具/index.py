#coding=utf-8
import web
import subprocess
import shutil
import os
import json
urls = (
    '/raid', 'Raid',
    '/hpraid','HPraid',
    '/ipmi','ipmi',
    '/install','install',
    '/reboot','reboot'
)
global grub
grub = """default=0
timeout=5
title LeTV Linux PXE install
    root (hd0,0)
    kernel /boot/vmlinuz ks="%s" biosdevname=0 ksdevice=link 
    initrd /boot/initrd.img
"""
app = web.application(urls, globals())
class HPraid:
    def GET(self):
        data = web.input()
        lv = data.get('lv')
        disk = data.get('disk')
        tiaodai = data.get('tiaodai')
        mode = data.get('mode')
        code = os.system("/bin/sh ls")
        return json.dumps({'code':code,})
class Raid:        
    def GET(self):
        msg_dict = {0:'正在安装',10:'Raid创建失败或者Raid参数不支持'}
        data = web.input()
        lv = data.get('lv')
        disk = data.get('disk')
        tiaodai = data.get('tiaodai')
        code = os.system("/bin/sh /root/auto_install.sh --raid \"%s\" \"%s\" \"%s\" " % (disk,lv,tiaodai))
        return json.dumps({'code':code,'msg':msg_dict[code]})
class install():
    def GET(self):
        data = web.input()
        ks = data.get("ks","conf.ks")
        ksurl = "http://10.58.241.31/kickstart/%s" % ks
        grub_file = open("/mnt/boot/grub/grub.conf",'w')
        grub_file.write(grub % ksurl)
        return json.dumps({'code':0})
class reboot():
    def GET(self):
        os.system('ipmitool -l lanplus chassis bootdev disk')
        os.system('reboot')
        return json.dumps({'reboot':0})
class ipmi():
    def GET(self):
        data = web.input()
        ilo_ip = data.get('ilo_ip',None)
        if not ilo_ip:
            return json.dumps({'code':0})
        lan = data.get('lan')
        stat = os.system('/bin/sh /root/auto_install.sh --ipmi %s %s' % (ilo_ip,lan))
        return json.dumps({'code':stat})

if __name__ == "__main__":
    app.run()  

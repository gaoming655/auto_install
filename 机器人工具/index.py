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
        mode = data.get('mode')
        code = os.system("/bin/sh /root/auto_install.sh --raid \"%s\" \"%s\" \"%s\" \"%s\" " % (disk,lv,mode,tiaodai))
        return json.dumps({'code':code,'msg':msg_dict[code]})
class install():
    def GET(self):
        data = web.input()
        ks = data.get("ks","conf.ks")
        ksurl = "http://199.0.0.1/%s" % ks
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
        ip = data.get(ip,None)
        
        stat = os.system('/bin/sh /root/auto_install.sh %s %s %s' % (ip,user,pw))
        return json.dumps({'code':stat})

if __name__ == "__main__":
    app.run()  

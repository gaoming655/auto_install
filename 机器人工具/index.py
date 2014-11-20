import web
import subprocess
import shutil
import os
import json
urls = (
    '/raid', 'Raid',
    '/','Info',
    '/ipmi','ipmi',
    '/install','install',
    '/reboot','reboot'
)
global grub
grub = """default=0
timeout=5
title LeTV Linux PXE install
    root (hd0,0)
    kernel /boot/vmlinuz ks="%s" ksdevice=link 
    initrd /boot/initrd.img
"""
app = web.application(urls, globals())
class Raid:        
    def GET(self):
        data = web.input()
        lv = data.get('lv')
        disk = data.get('disk')
        tiaodai = data.get('tiaodai')
        code = os.system("/bin/sh /root/auto_install.sh --raid %s %s %s" % (disk,lv,tiaodai))
        return json.dumps({'code':code})
class Info:
    def GET(self):
        os.system('/bin/sh /root/auto_install.sh --info')
        filemesg = open("/tmp/log",'r').read()
        return filemesg
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
        os.system('reboot')
        return json.dumps({'reboot':0})
class ipmi():
    def GET(self):
        data = web.input()
        ip = data.get(ip,None)
        user = data.get(user,None)
        pw = data.get(pw,None)
        if not ip and not user and not pw:
            return json.dump({'code':1})
        stat = os.system('/bin/sh /root/auto_install.sh %s %s %s' % (ip,user,pw))
        return json.dumps({'code':stat})

if __name__ == "__main__":
    app.run()  

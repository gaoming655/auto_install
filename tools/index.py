#coding=utf-8
import web
import subprocess
import shutil
import os
import json
urls = (
    '/raid', 'Raid',
    '/install','install',
    '/reboot','reboot'
)
global grub
grub = """default=0
timeout=5
title LeTV Linux PXE install
    root (hd0,0)
    kernel /boot/vmlinuz ks="%s" biosdevname=0 ksdevice=%s
    initrd /boot/initrd.img
"""
app = web.application(urls, globals())
class Raid:        
    def GET(self):
        msg_dict = {0:'正在安装',10:'Raid创建失败或者Raid参数不支持'}
        data = web.input()
        lv = data.get('lv')
        disk = data.get('disk')
        tiaodai = data.get('tiaodai')
        ks = data.get("ks")
        ksdev = data.get("ksdev")
        ilo_ip = data.get('ilo_ip')
        lan = data.get('lan')
        code = os.system("/bin/sh /root/auto_install.sh --raid \"%s\" \"%s\" \"%s\" \"%s\" \"%s\" \"%s\" \"%s\"" % (disk,lv,tiaodai,ks,ksdev,ilo_ip,lan))
        return json.dumps({'code':code,'msg':msg_dict[code]})
class install():
    def GET(self):
        data = web.input()
        ks = data.get("ks")
        ksurl = "http://10.58.241.31:8080/ks/%s" % ks
        ksdev = data.get("ksdev")
        grub_file = open("/mnt/boot/grub/grub.conf",'w')
        grub_file.write(grub % (ksurl,ksdev))
        grub_file.close()
        return json.dumps({'code':0})
class reboot():
    def GET(self):
        os.system('ipmitool -l lanplus chassis bootdev disk')
        os.system('reboot')
        return json.dumps({'reboot':0})

if __name__ == "__main__":
    app.run()  

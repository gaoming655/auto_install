#coding=utf-8
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.contrib.auth import login,logout,authenticate
from forms import *
from django.contrib.auth.decorators import login_required
import requests
import json
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def login_view(request):
    """用户登录认证"""
    if  request.method == 'POST':
        usr = authenticate(username = request.POST['username'],password = request.POST['passwd'])
        if usr is not None:
            if usr.is_active:
                login(request, usr)
                return HttpResponseRedirect('/find/')
            else:
                raise Http404
        else:
            raise Http404
    else:
        f = login_form()
        return render(request,'login.html',{'forms':f})

def logout_page(request):
    logout(request)
    return HttpResponseRedirect("/")
#----------------------------------------------------------------------

@login_required(login_url="/")
def find_page(request):
    """发现主机"""
    if request.method == "GET":
        all_data = install.objects.all()
        total = len(all_data)
        on_total = len(online.objects.filter(finish_status=False))
        return render(request,'find.html',{'forms':all_data, "total":total, "on_total":on_total,"index":"find"})

@login_required(login_url="/")
def info(request,info_id):
    """主机详情"""
    if request.method == "GET":
        machine_info = install.objects.get(id = int(info_id))
        if "HP" not in machine_info.inc:
            disk_list = disk_sotl.objects.filter(host_id=int(info_id))
        else:
            disk_list = disk_hp.objects.filter(host_id=int(info_id))
        return render(request,"info.html",{"forms":machine_info,'dd': disk_list})

#----------------------------------------------------------------------
@login_required(login_url="/")
def exe_page(request):
    """执行装机"""
    if request.method == 'GET':
        f = online.objects.filter(finish_status=False)
        on_total = len(f)
        total = len(install.objects.all())
        return render(request,"exe.html",{'forms':f,"total":total, "on_total":on_total,"index":"exe"})



@login_required(login_url="/")
def start(request,echo_id):
    """点击开始"""
    if request.method == 'GET':
        d = online.objects.get(id=int(echo_id))
        lv = d.level
        ip = d.ip
        disk = d.raid_zh
        ks = d.kickstart
        tiaodai = d.stripe
        ilo_ip = d.ilo_ip
        inc = d.inc
        raid_url = "http://%s/raid?lv=%s&disk=%s&tiaodai=%s" % (ip,lv,disk,tiaodai)
        grub_url = "http://%s/install?ks=%s" % (ip,ks)
        ilo_list = ilo_table.objects.values('maunfacturer').iterator()
        reboot_url = "http://%s/reboot" % ip
        for i in ilo_list:
            if i['maunfacturer'] in inc:
                lan = ilo_table.objects.get(maunfacturer=i['maunfacturer']).lan_num
                break
        ipmi_url = "http://%s/ipmi?lan=%s&ilo_ip=%s" % (ip,lan,ilo_ip)
        q = requests.get(raid_url)
        j = json.loads(q.text)
        if j['code'] == 0:
            requests.get(grub_url)
            requests.get(ipmi_url)
            requests.get(reboot_url)
            return HttpResponse(json.dumps({'code':0}))
        else:
            return HttpResponse(json.dumps({'code':1}))



@login_required(login_url="/")
def del_obj(request,obj_id):
    if request.method == "GET":
        obj = install.objects.get(id=int(obj_id)).delete()
        return HttpResponseRedirect('/find/')
@login_required(login_url="/")
def lock_obj(request,obj_id,obj_code):
    if request.method == "GET":
        if eval(obj_code):
            install.objects.filter(id=int(obj_id)).update(status=False)
        else:
            install.objects.filter(id=int(obj_id)).update(status=True)
        return HttpResponseRedirect('/find/')

@login_required(login_url="/")
def online_view(request,obj_id):
    """放入装机队列"""
    install_id = int(obj_id)
    d = install.objects.get(id=install_id)
    ipd = d.ipaddr
    incd = d.inc
    snd = d.sn
    channel = d.sotl
    dilo_ip = d.ilo_ip
    obj = online(sn=snd,inc=incd,ip=ipd,sotl_total=channel,ilo_ip=dilo_ip,)
    obj.save()
    d.delete()
    if "HP" not in incd:
        disk_sotl.objects.filter(host_id=install_id).update(host_id=obj.id)
    else:
        disk_hp.objects.filter(host_id=install_id).update(host_id=obj.id)
    return HttpResponseRedirect("/find/")

@login_required(login_url="/")
def edit(request,obj_id):
    """编辑需要安装的机器"""
    if request.method == "GET":
        obj = online.objects.get(id=int(obj_id))
        f = edit_form(instance=obj)
        if "HP" not in obj.inc:
            disk_list = disk_sotl.objects.filter(host_id=obj_id).order_by("sotl")
        else:
            disk_list = disk_hp.objects.filter(host_id=obj_id).order_by("sotl")
        if not disk_list:
            disk_list=None
        return render(request,"edit.html",{"forms":f,"disk":disk_list,"id":obj_id})
    else:
        dl = []
        d = request.POST
        level = d.get("level")
        disk =  d.getlist("disk_zh")
        ilo_ip = d.get("ilo_ip",None)
        ks = d.get("kickstart")
        tiaodai = d.get("stripe")
        obj = online.objects.get(id=int(obj_id))
        obj.level = level
        sotl = obj.sotl_total
        obj.kickstart = ks
        incd = obj.inc
        if "HP" not in  incd:
            for i in disk:
                dl.append(str(sotl)+":"+str(i))
                obj.raid_zh = "[" + ",".join(dl) + "]"
        else:
            obj.raid_zh = ",".join(disk)
        obj.stripe = tiaodai
        obj.ilo_ip = ilo_ip
        obj.save()
        return HttpResponseRedirect("/exe/")
@login_required(login_url="/")
def ing(request,o_id):
    """防止重复安装"""
    if request.method == "GET":
        online.objects.filter(id=int(o_id)).update(status=True)
        return HttpResponse(json.dumps({'code':0}))
@csrf_exempt
def register_post(request):
    """内存OS注册接口"""
    if request.method == "POST":
        d = request.body
        d = json.loads(d)
        dmem = d.get('mem')
        dcpu = d.get('cpu')
        dinc = d.get('inc')
        dsn = d.get('sn')
        ip = d.get('ip')
        dsotl = d.get('sotl')
        disk = d.get('disk')
        dilo_ip = d.get('ilo_ip',None)
        obj = install(inc=dinc,ipaddr=ip,cpu=dcpu,mem=dmem,sotl=dsotl,sn=dsn,ilo_ip=dilo_ip)
        obj.save()
        install_id = obj.id
        print dinc
        if  "HP" not in dinc:
            for k,v in disk.items():
                dso = disk_sotl(sotl=int(k),size=v,host_id=install_id)
                dso.save()
                dso = None
        else:
            for k,v in disk.items():
                hpdso = disk_hp(sotl=k,size=v,host_id=install_id)
                hpdso.save()
                hpdso = None
    return HttpResponse(json.dumps({"code":0}))

@login_required(login_url="/")
def his_page(request):
    if request.method == "GET":
        f = online.objects.filter(finish_status=True)
        total = len(install.objects.all())
        on_total = len(online.objects.filter(finish_status=False))
        return render(request,"his.html",{'forms':f,'index':'succeed',"total":total, "on_total":on_total,})

@csrf_exempt
def finish_api(request):
    if request.method == "POST":
        dip = request.META['REMOTE_ADDR']
        dsn = request.POST['sn']
        online.objects.filter(ip=dip,sn=dsn).update(finish_status=True)
        return HttpResponse(json.dumps({'code':0}))

@login_required(login_url="/")
def delivery(request,obj_id):
    o = get_object_or_404(online,id=obj_id)
    o.delete()
    return HttpResponseRedirect('/his/')
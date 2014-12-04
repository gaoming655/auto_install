#coding=utf-8
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.contrib.auth import login,logout,authenticate
from forms import *
from django.contrib.auth.decorators import login_required
import requests
import json
from django.views.decorators.csrf import csrf_exempt
import os
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
    """注销用户"""
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
    """装机队列页面"""
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
        s_ip = d.service_ip
        nk = d.service_netmask
        gw = d.service_gw
        ilo_list = ilo_table.objects.values('maunfacturer').iterator()
        reboot_url = "http://%s/reboot" % ip
        for i in ilo_list:
            if i['maunfacturer'] in inc:
                get_pintan = ilo_table.objects.get(maunfacturer=i['maunfacturer'])
                lan = get_pintan.lan_num
                ksdev = get_pintan.ksdev
                break
        raid_url = "http://%s/raid?lv=%s&disk=%s&tiaodai=%s&ks=%s&ksdev=%s&ilo_ip=%s&lan=%s" % (ip,lv,disk,tiaodai,echo_id,ksdev,ilo_ip,lan)
        q = requests.get(raid_url)
        j = json.loads(q.text)
        if j['code'] == 0:
            requests.get(reboot_url)
            d.status=True
            d.save()
            return HttpResponse(json.dumps({'code':0}))
        else:
            return HttpResponse(json.dumps({'code':1}))



@login_required(login_url="/")
def del_obj(request,obj_id):
    """删除误重启的机器"""
    if request.method == "GET":
        obj = install.objects.get(id=int(obj_id)).delete()
        return HttpResponseRedirect('/find/')
@login_required(login_url="/")
def lock_obj(request,obj_id,obj_code):
    """锁定机器"""
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
    elif request.method == "POST":
        dl = []
        d = request.POST
        level = d.get("level")
        disk =  d.getlist("disk_zh")
        ilo_ip = d.get("ilo_ip",None)
        ks = d.get("kickstart")
        tiaodai = d.get("stripe")
        sip = d.get("service_ip")
        snk = d.get("service_netmask")
        sgw = d.get("service_gw")
        obj = online.objects.get(id=int(obj_id))
        obj.level = level
        obj.service_ip = sip
        obj.service_netmask = snk
        obj.service_gw = sgw
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
        online.objects.filter(service_ip=dip,sn=dsn).update(finish_status=True)
        return HttpResponse(json.dumps({'code':0}))

@login_required(login_url="/")
def delivery(request,obj_id):
    if request.method == "GET":
        o = get_object_or_404(online,id=obj_id)
        o.delete()        
        return HttpResponseRedirect('/his/')

@csrf_exempt
def jindu_post(request,get_sn):
    if request.method == "POST":
        jindu = int(request.POST.get('jindu',0))
        d = online.objects.get(sn=get_sn)
        d.jindu = jindu
        d.save()
        return HttpResponse(json.dumps({'code':0}))
    

@login_required(login_url="/")
def get_jindu_from_db(request,get_id):
    if request.method == "GET":
        d = online.objects.get(id=int(get_id))
        jindu_val = d.jindu
        return HttpResponse(json.dumps({"val":jindu_val}))
        
        

def get_eth_from_obj(f_id):
    o = online.objects.get(id=f_id)
    inc = o.inc
    ilo_list = ilo_table.objects.values('maunfacturer').iterator()
    for i in ilo_list:
        print i
        if i['maunfacturer'] in inc:
            get_pintan = ilo_table.objects.get(maunfacturer=i['maunfacturer'])
            print get_pintan
            kseth = get_pintan.ksdev
            break    
    return kseth

def kickstart_file_url(request,get_ks_id):
    o = online.objects.get(id=int(get_ks_id))
    return render(request,'ks/%s.cfg' % o.kickstart,{'server':o})
    
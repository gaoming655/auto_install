#!/bin/bash
#letv functions auto install  machine bash
#mady by G.M
#date: 2014-11-11
inc=`/usr/bin/facter manufacturer`
echo $inc|grep HP > /dev/null
code=$?
RAID (){
	disk_list=$1
	disk_lv=$2
	tiaodai=$3
	ks=$4
	ksdev=$5
	ilo_ip=$6
	lan=$7
	if [ $code -ne "0" ];then
		/opt/MegaRAID/MegaCli/MegaCli64 -CfgLdDel -Lall -a0
		/opt/MegaRAID/MegaCli/MegaCli64 -CfgLdAdd -r${disk_lv} $disk_list WB Cache -strpsz${tiaodai} -a0 
		xcode=$?
		if [ $xcode -ne "0" ];then
			/opt/MegaRAID/MegaCli/MegaCli64 -CfgLdAdd -r${disk_lv} $disk_list WB Direct -strpsz${tiaodai} -a0
		else
			exit 10
        fi
    else 
    	HP_RAID
	fi
	DISK
	IPMI ilo_ip lan
	curl "http://127.0.0.0/install?ks=$ks&ksdev=$ksdev"
}
DISK(){ 
	sdx=`fdisk -l|grep 'Disk /dev/sd'|awk '{print $2}'|tr -d : |head -n 1`
	dd  if=/dev/zero of=$sdx  count=1
	sfdisk $sdx -uM < /root/disk.data
	mkfs.ext4 ${sdx}1
	mount ${sdx}1  /mnt/
	grub-install --root-directory=/mnt/ $sdx 
	cp /root/vmlinuz  /mnt/boot/
	cp /root/initrd.img  /mnt/boot/
	ipmitool -I open  chassis bootdev disk
}

HP_RAID(){
	slot=`hpacucli ctrl all show |awk '{print $6}'`
	hpacucli ctrl slot=${slot} array A delete forced
	hpacucli ctrl slot=${slot} create type=ld drives=${disk_list} raid=${disk_lv} stripesize=${tiaodai}
}
IPMI(){
	ip=$1
	lan=$2
	gw=${ip%.*}.1
	ipmitool lan set $lan ipsrc static 
	ipmitool lan set $lan ipaddr $ip
	ipmitool lan set $lan netmask 255.255.255.0
	ipmitool lan set $lan defgw ipaddr  $gw
	if [ $code -eq "0" ];then
		ipmitool  user set   password 1 @qiugaoqs123
	fi
 
}
key=$1
case $key in
	--raid)
		shift
		RAID $1 $2 $3 $4 $5 $6 $7
		;;
	--ipmi)
		shift
		IPMI  $1 $2
		;;
esac

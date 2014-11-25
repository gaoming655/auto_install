#!/bin/bash
#letv functions auto install  machine bash
#mady by G.M
#date: 2014-11-11
RAID (){
	inc=`/usr/bin/facter manufacturer`
	echo $inc|grep HP > /dev/null
	code=$?
	disk_list=$1
	disk_lv=$2
	tiaodai=$3
	if [ $code -ne "0" ];then
		/opt/MegaRAID/MegaCli/MegaCli64 -CfgLdDel -Lall -a0
		/opt/MegaRAID/MegaCli/MegaCli64 -CfgLdAdd -r${disk_lv} $disk_list WB Cache -strpsz${tiaodai} -a0 
		code=$?
		if [ $code -ne "0" ];then
			/opt/MegaRAID/MegaCli/MegaCli64 -CfgLdAdd -r${disk_lv} $disk_list WB Direct -strpsz${tiaodai} -a0
		else
			exit 10
                fi
	fi
	DISK
}
DISK(){ 
	sdx=`fdisk -l|grep 'Disk /dev/sd'|awk '{print $2}'|tr -d :`
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
	hpacucli ctrl slot=${slot} create type=ld drives=$disk_list raid=$disk_lv stripesize=${tiaodai}
}
IPMI(){
	ip=$1
	lan=$2
	gw=${ip%.*}.1
	ipmitool lan set $lan ipsrc static 
	ipmitool lan set $lan ipaddr $ip
	ipmitool lan set $lan netmask 255.255.255.0
	ipmitool lan set $lan defgw ipaddr  $gw
 
}
key=$1
case $key in
	--raid)
		shift
		RAID $1 $2 $3
		;;
	--hpraid)
		shift
		;;
	--ipmi)
		shift
		IPMI  $1 $2
		;;
esac

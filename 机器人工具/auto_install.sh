#!/bin/bash
#letv functions auto install  machine bash
#mady by G.M
#date: 2014-11-11
RAID (){
	inc=`/usr/bin/facter manufacturer`
	echo $inc|grep HP > /dev/null
	code=$?
	disk_lv=$1
	disk_list=$2
	mode=$3
	tiaodai=$4
	if [ $code -ne "0" ];then
		/opt/MegaRAID/MegaCli/MegaCli64 -CfgLdDel -Lall -a0
		/opt/MegaRAID/MegaCli/MegaCli64 -CfgLdAdd -r${disk_lv} $disk_list WB ${mode} -strpsz${tiaodai} -a0 
		code = $?
		if [ $code -ne "0" ];then
			/opt/MegaRAID/MegaCli/MegaCli64 -CfgLdAdd -r${disk_lv} $disk_list WB Direct -strpsz${tiaodai} -a0
		else
			exit 10
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
	ipmitool -l lanplus chassis bootdev disk
}

HP_RAID(){
	slot=`hpacucli ctrl all show |awk '{print $6}'`
	hpacucli ctrl slot=${slot} array A delete forced
	hpacucli ctrl slot=${slot} create type=ld drives=$disk_list raid=$disk_lv stripesize=${tiaodai}
}
key=$1
case $key in
	--raid)
		shift
		RAID $1 $2 $3 $4
		;;
	--hpraid)
		shift
		;;
	--ipmi)
		shift
		IPMI 
esac
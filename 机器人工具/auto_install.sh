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
	tiaodai=$3
	if [ $code -ne "0" ];then
		/opt/MegaRAID/MegaCli/MegaCli64 -CfgLdDel -Lall -a0
		/opt/MegaRAID/MegaCli/MegaCli64 -CfgLdAdd -r${disk_lv} $disk_list WB Cache -strpsz${tiaodai} -a0 
	else:
		slot=`hpacucli ctrl all show |awk '{print $6}'`
		hpacucli ctrl slot=${slot} array A delete forced
		hpacucli ctrl slot=${slot} create type=ld drives=$disk_list raid=$disk_lv stripesize=${tiaodai}
	fi 
	sdx=`fdisk -l|grep 'Disk /dev/sd'|awk '{print $2}'|tr -d :`
	dd  if=/dev/zero of=$sdx  count=1
	sfdisk $sdx -uM < /root/disk.data
	mkfs.ext4 ${sdx}1
	mount ${sdx}1  /mnt/
	grub-install --root-directory=/mnt/ $sdx 
	cp /root/vmlinuz  /mnt/boot/
	cp /root/initrd.img  /mnt/boot/

}

INFO(){
	ip=`facter ipaddress`
	mac=`facter macaddress`
	mem=`facter memorysize`
	cpu=`facter processor0`
	cat > /tmp/log <<EOF
	ip:   $ip
	mac:  $mac
	mem:  $mem
	cpu:  $cpu
EOF
	/opt/MegaRAID/MegaCli/MegaCli64 -Pdlist -aall|grep Raw >>/tmp/log
	slot=`hpacucli ctrl all show |awk '{print $6}'`
	hpacucli  ctrl slot=${slot} pd all show
}
key=$1
case $key in
	--info)
		shift
		INFO 
		;;
	--raid)
		shift
		if [ $# -lt 2 ];then
			exit "1"
		fi
		RAID $1 $2 $3
		;;
esac
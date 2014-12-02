#!/bin/bash
disk="/mnt/sysimage/root/install.log"

server=$1

total=$2

if [ -f "$disk" ];then
	dangqian=`wc -l $disk`
	jindu=$(($dangqian/$total))
	curl -d "jindu=$jindu" "http://$server/jindu_post/"
else
	sleep 10
fi

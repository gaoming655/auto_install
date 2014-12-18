#!/bin/bash
ip=`facter ipaddress`
mem=`facter memorysize`
cpu=`facter processor0`
inc=`facter manufacturer`
sn=`facter serialnumber`
#add server ip
echo $inc |grep "HP" >/dev/null
code=$?
if [ $code -ne 0 ];then 
	sotl=`/opt/MegaRAID/MegaCli/MegaCli64  -pdlist -aall |grep "Enclosure Device ID"|awk '{print $NF}'|uniq`
	disk=`/opt/MegaRAID/MegaCli/MegaCli64  -pdlist -aall |grep  "Slot Number\|Raw Size"|awk '{print $3$4}'|awk 'NR%2==1{T=$0;next}{print "\""T"\""":""\""$0"\""","}'|sed '$s/,//'`
else
	sotl=`hpacucli  ctrl all show  |awk '{print $6}'|grep -v '^$'`
	disk=`hpacucli  ctrl  slot=$sotl  pd all show|awk '{print "\""$2"\"","@","\""$8$9"\"" ","}'|grep ':'|sed -e 's/,//' -e 's/@/:/'|sed '$s/,//'`
fi
ilo_ip=`ipmitool  lan print |grep  'IP Address [^Source]' |awk '{print $NF}'`
ilo_netmask=`ipmitool  lan print|grep 'Subnet Mask'|awk '{print $NF}'`
ilo_gw=`ipmitool  lan print|grep 'Default Gateway IP'|awk '{print $NF}'`
for i in eth{0..4};do facter  ipaddress_$i |grep '192.168.211' && ksdev=$i;done
echo '{' > info.json
echo "\"ip\":\"$ip\",">>info.json
echo "\"ilo_ip\":\"$ilo_ip\",">>info.json
echo "\"ilo_netmask\":\"$ilo_netmask\",">>info.json
echo "\"ilo_gw\":\"$ilo_gw\",">>info.json
echo "\"ksdev\":\"$ksdev\",">>info.json
echo "\"mem\":\"$mem\",">>info.json
echo "\"cpu\":\"$cpu\",">>info.json
echo "\"sn\":\"$sn\",">>info.json
echo "\"inc\":\"$inc\",">>info.json
echo "\"sotl\":\"$sotl\",">>info.json
echo '"disk":' >>info.json
echo '{' >> info.json
echo $disk >>info.json
echo '}' >>info.json
echo '}' >>info.json

parse_json(){
echo $1 | sed 's/.*'$2':\([^,}]*\).*/\1/'
}
while : ; do
	string=`curl -X POST  -H 'content-type:application/json' -d @info.json   http://@@server_ip@@/post/`
	val=$(parse_json $string "code")
	if [ $val == "0" ];then
		break
	else
		sleep 20
		continue
	fi
done

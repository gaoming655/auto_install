#!/bin/bash
ip=`facter ipaddress`
mem=`facter memorysize`
cpu=`facter processor0`
inc=`facter manufacturer`
sn=`facter serialnumber`
#sotl=`/opt/MegaRAID/MegaCli/MegaCli64  -pdlist -aall |grep "Enclosure Device ID"|awk '{print $NF}'|uniq`
sotl="32"
disk=`/opt/MegaRAID/MegaCli/MegaCli64  -pdlist -aall |grep  "Slot Number\|Raw Size"|awk '{print $3$4}'|awk 'NR%2==1{T=$0;next}{print "\""T"\""":""\""$0"\""","}'|sed '$s/,//'`
echo '{' > info.json
echo "\"ip\":\"$ip\",">>info.json
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

curl -X POST  -H 'content-type:application/json' -d @info.json   199.0.0.254/post/

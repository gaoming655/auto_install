# kickstart template for Fedora 8 and later.
# (includes %end blocks)
# do not use with earlier distros

#platform=x86, AMD64, or Intel EM64T
# System authorization information
auth  --useshadow  --enablemd5
# System bootloader configuration
bootloader --location=mbr
# Partition clearing information
# Use text mode install
text
# Firewall configuration
firewall --enabled
# Run the Setup Agent on first boot
firstboot --disable
# System keyboard
keyboard us
# System language
lang en_US
# Use network installation
url --url=http://10.58.241.31/cblr/links/CentOS-6.4-x86_64
# If any cobbler repo definitions were referenced in the kickstart profile, include them here.
repo --name=source-1 --baseurl=http://10.58.241.31/cobbler/ks_mirror/CentOS-6.4-x86_64

# Network information
#network --bootproto=dhcp --device=eth0 --onboot=on  
network --bootproto=static --ip=nmip --netmask=nmnm --gateway=nmgw --device=eth0 --onboot=on
# Reboot after installation
reboot

#Root password
rootpw --iscrypted $1$sdasdyau$E/7ile6IXC6VID/AutMVl.
# SELinux configuration
selinux --disabled
# Do not configure the X Window System
skipx
# System timezone
timezone  America/New_York
# Install OS instead of upgrade
install
# Clear the Master Boot Record
zerombr
# Allow anaconda to partition the system as needed
autopart

%include /tmp/part-include
%pre
#/bin/sh
for i in `ls /sys/block`
do
   if [ `cat /sys/block/$i/removable` -eq 1 ];then
      name="$i|"$name
   fi
done
[ ! -z $name ]  &&  disk=`echo "$name""mapper"` || disk="mapper"
hddisk=`fdisk  -l 2>/dev/null |egrep -vi "($disk)" |grep "^Disk /dev/"|awk 'BEGIN{m=100000;}{if($4 ~ /[GgBb]/){name[$2]=$3;n++;}} END{if(n>1){for(aa in name){if(m>name[aa]){m=name[aa];dev=aa;}}print dev;}else{for(aa in name) print aa}}'|sed -e 's/\/dev\///;s/://'`
echo "#partitioning scheme generated in %pre for 1 drive" > /tmp/part-include
echo "clearpart --all --initlabel --drives=$hddisk" >> /tmp/part-include
echo "part pv.008002 --grow --size=1 --ondisk=$hddisk" >> /tmp/part-include
echo "part /boot --fstype=ext4 --size=500 --ondisk=$hddisk" >> /tmp/part-include
echo "part swap --size=8192 --ondisk=$hddisk" >> /tmp/part-include
echo "volgroup VGSYS --pesize=4096 pv.008002" >> /tmp/part-include
echo "logvol / --fstype=ext4 --name=lv_root --vgname=VGSYS --size=10240" >> /tmp/part-include
echo "logvol /var --fstype=ext4 --name=lv_var --vgname=VGSYS --size=10240" >> /tmp/part-include
echo "logvol /letv --fstype=ext4 --name=lv_letv --vgname=VGSYS --size=10240" >> /tmp/part-include

set -x -v
exec 1>/tmp/ks-pre.log 2>&1
# Once root's homedir is there, copy over the log.
while : ; do
    sleep 10
    if [ -d /mnt/sysimage/root ]; then
        cp /tmp/ks-pre.log /mnt/sysimage/root/
        logger "Copied %pre section log to system"
        break
    fi
done &


wget "http://10.58.241.31/cblr/svc/op/trig/mode/pre/profile/CentOS-6.4-x86_64" -O /dev/null
# Add  hostprogress
sn=`dmidecode  -s system-serial-number`
total=392
server="10.58.241.31"
while : ;do
    if [ -f /mnt/sysimage/root/install.log ]; then
       dangqian=`wc -l /mnt/sysimage/root/install.log|awk '{print $1}'`
       jindu=$((${dangqian}00/$total))
       if [ $jindu  -eq "100" ];then
           curl -d "jindu=$jindu" "http://${server}:8080/jindu_post/$sn/"
           break
       else
           curl -d "jindu=$jindu" "http://${server}:8080/jindu_post/$sn/"
       fi
       sleep 5
    else
       sleep 10
    fi
done  &
# Enable installation monitoring

%end

%packages
@base

%end

%post --nochroot
set -x -v
exec 1>/mnt/sysimage/root/ks-post-nochroot.log 2>&1

%end

%post
set -x -v
exec 1>/root/ks-post.log 2>&1

# Start yum configuration
wget "http://10.58.241.31/cblr/svc/op/yum/profile/CentOS-6.4-x86_64" --output-document=/etc/yum.repos.d/cobbler-config.repo

# End yum configuration



# Start post_install_network_config generated code
# End post_install_network_config generated code




# Start download cobbler managed config files (if applicable)
# End download cobbler managed config files (if applicable)

# Start koan environment setup
echo "export COBBLER_SERVER=10.58.241.31" > /etc/profile.d/cobbler.sh
echo "setenv COBBLER_SERVER 10.58.241.31" > /etc/profile.d/cobbler.csh
# End koan environment setup

# begin Red Hat management server registration
# not configured to register to any Red Hat management server (ok)
# end Red Hat management server registration

# Begin cobbler registration
# cobbler registration is disabled in /etc/cobbler/settings
# End cobbler registration

# Enable post-install boot notification

# Start final steps
sn=`dmidecode  -s system-serial-number`
curl -d "sn=$sn" "http://10.58.241.31:8080/finish/"
wget "http://10.58.241.31/cblr/svc/op/ks/profile/CentOS-6.4-x86_64" -O /root/cobbler.ks
wget "http://10.58.241.31/cblr/svc/op/trig/mode/post/profile/CentOS-6.4-x86_64" -O /dev/null
# End final steps
%end

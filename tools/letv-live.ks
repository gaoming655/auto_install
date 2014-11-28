# centos_minimal_livecd.ks 
# Created by AndrewSerk
#part / --size 8192 --fstype ext4
lang en_US.UTF-8
keyboard us
timezone US/Eastern
auth --useshadow --enablemd5
selinux --disabled
firewall --disabled
services --enabled=ipmi,ipmievd


# Root password
rootpw  123 

repo --name=a-base --baseurl=file:///yum/mnt/Packages/

%packages
bash
kernel
syslinux
passwd
policycoreutils
python-setuptools
chkconfig
authconfig
rootfiles
comps-extras
wget
grub
# livecd bits to set up the livecd and be able to install
#anaconda
device-mapper-multipath
NetworkManager
e2fsprogs
Lib_Utils
MegaCli
OpenIPMI-libs
OpenIPMI
lm_sensors-libs
net-snmp-libs
hpacucli
ipmitool
ruby
ruby-libs
facter
%end

%post
echo 'nameserver 8.8.8.8' > /etc/resolv.conf
cat > /root/start.sh << 'EOF'
#!/bin/bash
easy_install web.py
wget http://199.0.0.1/vmlinuz -O /root/vmlinuz
wget http://199.0.0.1/initrd.img -O /root/initrd.img 
wget http://199.0.0.1/ping.sh -O /root/ping.sh
EOF
echo "RUN_FIRSTBOOT=NO" > /etc/sysconfig/firstboot
/bin/sh /root/start.sh
cat > /root/disk.data << disk_EOF
,500,
;
disk_EOF
cat > /etc/rc.d/rc.local <<'EOF_rc'
#!/bin/sh
#
# This script will be executed *after* all the other init scripts.
# You can put your own initialization stuff in here if you don't
# want to do the full Sys V style init stuff.

touch /var/lock/subsys/local
/bin/sh /root/ping.sh 199.0.0.1
wget http://199.0.0.1/post.sh -O /root/post.sh
wget http://199.0.0.1/index.py  -O /root/index.py
wget http://199.0.0.1/auto_install.sh  -O /root/auto_install.sh
sleep 2
nohup /usr/bin/python /root/index.py 0.0.0.0:80 &
/bin/sh  /root/post.sh
EOF_rc

%end
########################################################################
#
#  LiveCD post install in chroot 
#
########################################################################
########################################################################
#
#  LiveCD post no chroot install 
#
########################################################################
%post --nochroot

for rhgbfile in EFI/boot/isolinux.cfg EFI/boot/grub.conf isolinux/isolinux.cfg EFI/boot/boot.conf
do
 echo "# uglifying $LIVE_ROOT/$rhgbfile"
 echo "# uglifying $LIVE_ROOT/$rhgbfile" >> $LIVE_ROOT/$rhgbfile
 sed -i -e's/ rhgb//g' -e's/ quiet//g' -e's/ rd_NO_DM/ 3/g' $LIVE_ROOT/$rhgbfile
 echo "# uglified $LIVE_ROOT/$rhgbfile" >> $LIVE_ROOT/$rhgbfile
done
#***********************************************************************
# Create /root/postnochroot-install
# Must change "$" to "\$" and "`" to "\`" to avoid shell quoting
#***********************************************************************
%end

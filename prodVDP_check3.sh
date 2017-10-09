#/bin/bash
/usr/local/avamar/bin/mccli activity show >> /tmp/testvdp # Backup results
/usr/local/avamar/bin/mccli client show --recursive=true | grep -e Virtual\ Machine >> /tmp/VMlist # List of VMs which are supposed to backup
#sudo mccli activity show >> /tmp/testvdp1
duration=$(cat /usr/lib/nagios/plugins/VDPresult.sh | grep -m1 4927 | awk '{print $2}')
EXIT_OKAY=0
EXIT_WARNING=1
EXIT_CRITICAL=2
curryea=$(date +"%y")
currday=$(date +"%e")
currmon=$(date +"%m")
let currday=currday+1-2
if [ $currday -lt 10 ]; then
        currday=0$currday
fi
#echo -e $currday #DEV
cat /tmp/testvdp | grep "$curryea-$currmon-$currday" | grep Completed > /tmp/r.tmp && mv /tmp/r.tmp /tmp/testvdp # removes past entries
VM=$(expr $(wc -l < /tmp/VMlist)) # count of all VMs
Completed=$(expr $(wc -l < /tmp/testvdp)) # count of successful backups
res=$(expr $VM - $Completed)
rm -f /tmp/testvdp /tmp/VMlist
if [ $res -eq 0 ]; then # OUTPUT BLOCK
        echo -e "#!/bin/bash\necho Succeed $Completed/$VM, No fails\nexit $EXIT_OKAY\n#      4927" > /usr/lib/nagios/plugins/VDPresult.sh
elif [ $res -eq 1 ]; then
        if [ $duration -eq 4927 ];then
                echo -e "#!/bin/bash\necho Succeed $Completed/$VM, 1 day reserve warn\nexit $EXIT_OKAY\n#      49271" > /usr/lib/nagios/plugins/VDPresult.sh
        else
        echo -e "#!/bin/bash\necho One VM didn\'t backup\nexit $EXIT_WARNING\n#      49271" > /usr/lib/nagios/plugins/VDPresult.sh
        fi
else
         if [ $duration -eq 4927 ];then
                echo -e "#!/bin/bash\necho Succeed $Completed/$VM, 1 day reserve crit\nexit $EXIT_OKAY\n#      49271" > /usr/lib/nagios/plugins/VDPresult.sh
         else
        echo -e "#!/bin/bash\necho $res VMs failed to backup\nexit $EXIT_CRITICAL\n#      49271" > /usr/lib/nagios/plugins/VDPresult.sh
        fi
fi
chown nagios:nagios /usr/lib/nagios/plugins/VDPresult.sh
chmod +x /usr/lib/nagios/plugins/VDPresult.sh

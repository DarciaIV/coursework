#!/bin/sh # enviroment
host=$(hostname)
srv=$(cat /etc/ntp.conf | grep server)
echo $host-$srv>>remfile
sed -i 's/server//' remfile

#!/bin/bash
while read hosts_vdp
do
	ssh-keyscan $hosts_vdp >> ~/.ssh/known_hosts
done < hosts_vdp

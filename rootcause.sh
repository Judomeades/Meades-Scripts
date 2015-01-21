#!/bin/bash
# Created by Judomeades and networkant
# Root cause all in one
date=`date +'%Y%m%d'`
file=$date"rootcause.log"
#If disk space is greater than 90% 
if [[ -n $(df -h | grep 9[0-9]%) ]]; then
        echo df -h >> $file
fi
if [[ -n $(df -h | grep 100%) ]]; then
        echo df -h >> $file
fi

#Check for out of memory in /var/log/messages
grep oom /var/log/messages >> $file
grep invoked /var/log/messages >> $file

#Check to see if there is less than 1GB less in RAM
Used="$(free -m | grep Mem | awk '{print $4}';)"
if [ "$Used" -lt "1000" ]; then
        echo "Available memory is: $Used" >> $file
fi

#look forauthentication failures
grep "Authentication failed" /var/log/messages >> $file


#Run status
if [[ -n $(service mysql status | grep SUCCESS) ]]; then
        echo "mysql is fine" >> $file
else
        echo "mysql is either not installed or off" >> $file
fi

if [[ -n $(service httpd status | grep uptime) ]]; then
        echo "httpd is fine" >> $file
else
        echo "Httpd is either not installed or off" >> $file
fi

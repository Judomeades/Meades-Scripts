#!/bin/bash
#Mitchell Root cause all in one

#If disk space is greater than 90%
if [[ -n $(df -h | grep 9[0-9]%) ]]; then
        echo df -h >> rootcause.txt
fi
if [[ -n $(df -h | grep 100%) ]]; then
        echo df -h >> rootcause.txt
fi

#Check for out of memory in /var/log/messages
grep oom /var/log/messages >> rootcause.txt
grep invoked /var/log/messages >> rootcause.txt

#Check to see if there is less than 1GB less in RAM
Used="$(free -m | grep Mem | awk '{print $4}';)"
if [ "$Used" -lt "1000" ]; then
        echo "Available memory is: $Used" >> rootcause.txt
fi

#look forauthentication failures
grep "Authentication failed" /var/log/messages >> rootcause.txt


#Run status
if [[ -n $(service mysql status | grep SUCCESS) ]]; then
        echo "mysql is fine" >> rootcause.txt
else
        echo "mysql is either not installed or off" >> rootcause.txt
fi

if [[ -n $(service httpd status | grep uptime) ]]; then
        echo "httpd is fine" >> rootcause.txt
else
        echo "Httpd is either not installed or off" >> rootcause.txt
fi

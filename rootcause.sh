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
        echo $Used >> rootcause.txt
fi

#look forauthentication failures
grep "New connection" /var/log/messages >> rootcause.txt
grep "Authentication failed" /var/log/messages >> rootcause.txt


#Run status

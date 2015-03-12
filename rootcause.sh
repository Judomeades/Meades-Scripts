#!/bin/bash
# Created by Judomeades and networkant
# Root cause all in one

datesecondary=`date +'%Y%m%d'`
atopdate='date'
Month=$(date | awk {'print $2'})
Day=$(date | awk {'print $3'})
Year=$(date | awk {'print $6'})

if [ "$Month" = "Jan" ]; then
        NMonth="01"
fi
if [ "$Month" = "Feb" ]; then
        NMonth="02"
fi
if [ "$Month" = "Mar" ]; then
        NMonth="03"
fi
if [ "$Month" = "Apr" ]; then
        NMonth="04"
fi
if [ "$Month" = "May" ]; then
        NMonth="05"
fi
if [ "$Month" = "Jun" ]; then
        NMonth="06"
fi
if [ "$Month" = "Jul" ]; then
        NMonth="07"
fi
if [ "$Month" = "Aug" ]; then
        NMonth="08"
fi
if [ "$Month" = "Sep" ]; then
        NMonth="09"
fi
if [ "$Month" = "Oct" ]; then
        NMonth="10"
fi
if [ "$Month" = "Nov" ]; then
        NMonth="11"
fi
if [ "$Month" = "Dec" ]; then
        NMonth="12"
fi
file=$datesecondary"rootcause.log"

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

#Check to see if there is less than 1GB less in RAM
Used="$(free -m | grep Mem | awk '{print $4}';)"
if [ "$Used" -lt "1000" ]; then
        echo "Available memory is: $Used MB" >> $file
fi

#Determine OS ( redhat = 0; debian/other = 1)
if [[ -n $(cat /etc/*-release | grep "ent") ]]; then
        os=0
else
        os=1
fi

#Use the OS variable to determine how to look for atop, if atop is not installed, it installs it and then lets the person know.  If it is installed then it looks for high percentages.
if [ "$os" -eq 0 ]; then
    CHECKATOPRPM=`rpm -qa | grep atop`
    if [ "$CHECKATOPRPM" = "" ]; then
         wget -qO- http://198.20.70.18/~atop/atop1lnr | sh
         echo "We have installed atop now, however, there will likely not be enough information to definitely determine the cause of downtime.  We can check back in 12 hours to see if there is any activity in the atop logs between now and then though" >> $file
   else
        counter=1
        while [[ $counter -lt 2 ]]; do
                ls /var/log/atop | grep atop | grep -v log | sed 's/\.1//g'
                echo "Please choose one of these days in year month day format"
                echo "Example 20150315 for March 15, 2015"
                read date
                if [ "$date" -ne "$datesecondary" ]; then
                        atop -r /var/log/atop/atop_"$date".1 | awk '{print $4 " " $5 " " $11 " "  $12}' | grep -v "0K" |  grep -B 20 "[1-9][1-9]\{1,20\}%" | grep  -v "zombie" | grep -v "idle" | grep -v " [0-9]%" | grep -v "|" | grep -v "VGROW" >> $file
                else
                       atop -r /var/log/atop/atop_"$date" | awk '{print $4 " " $5 " " $11 " "  $12}' | grep -v "0K" |  grep -B 20 "[1-9][1-9]\{1,20\}%" | grep  -v "zombie" | grep -v "idle" | grep -v " [0-9]%" | grep -v "|" | grep -v "VGROW" >> $file
                fi
        if [ $? != 0 ]; then
                echo "Invalid choice"
                let counter=counter-1
        fi
        let counter=counter+1
        done
  fi
fi
if [ "$os" -eq 1 ]; then
    CHECKATOPDEB=`dpkg -l | grep atop`
    if [ "$CHECKATOPDEB" = "" ]; then
        wget -qO- http://198.20.70.18/~atop/atop1lnr | sh
        echo "We have installed atop now, however, there will likely not be enough information to definitely determine the cause of downtime.  We can check back in 12 hours to see if there is any activity in the atop logs between now and then though" >> $file
    else
       counter=1
        while [[ $counter -lt 2 ]]; do
                ls /var/log/atop | grep atop | grep -v log | sed 's/\.1//g'
                echo "Please choose one of these days in year month day format"
                echo "Example 20150315 for March 15, 2015"
                read date
                if [ "$date" -ne "$datesecondary" ]; then
                        atop -r /var/log/atop/atop_"$date".1 | awk '{print $4 " " $5 " " $11 " "  $12}' | grep -v "0K" |  grep -B 20 "[1-9][1-9]\{1,20\}%" | grep  -v "zombie" | grep -v "idle" | grep -v " [0-9]%" | grep -v "|" | grep -v "VGROW" >> $file
                else
                       atop -r /var/log/atop/atop_"$date" | awk '{print $4 " " $5 " " $11 " "  $12}' | grep -v "0K" |  grep -B 20 "[1-9][1-9]\{1,20\}%" | grep  -v "zombie" | grep -v "idle" | grep -v " [0-9]%" | grep -v "|" | grep -v "VGROW" >> $file
                fi
        if [ $? != 0 ]; then
                echo "Invalid choice"
                let counter=counter-1
        fi
        let counter=counter+1
        done
    fi
fi

cat $file;

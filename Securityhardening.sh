#!/bin/bash
# Mitchell Eades Security hardening

i=1;
while [ $i -eq 1 ]; do
echo "Here is the menu:"
echo "Option 1:  Install CSF"
echo "Option 2:  Block all ports except ones specified"
echo "       21:  Do this within IPtables"
echo "       22:  Do this within CSF"
echo "Option 3:  Whitelist a single IP"
echo "Option 4:  Blacklist a single IP"
echo "Option 5:  Clear out all blocked IP addresses"
echo "Option 6:  Whitelist a list of IP addresses"
echo "Option 7:  Blacklist a list of IP addresses"
echo "Option 8:  Install Maldet"
echo "Option 9:  Set maldet to run a full malware scan in crontab and"
echo "       91: Auto quarantine (not recommend because maldet may pick up false flags)"
echo "       92: Email specified account if there are any hits"
echo "Option 10: Install Clamav"
echo "Option 11: Set clamav to do a full scan"
printf "Type your option here: "
read Option;
echo $Option
echo ""
if [ "$Option" -eq 1 ]; then
  echo "Installing CSF"
elif [ "$Option" -eq 2 ]; then
 echo "Please list any ports you do not want blocked"
elif [ "$Option" -eq 21 ]; then
 echo "Please list any ports you do not want blocked"
elif [ "$Option" -eq 22 ]; then
 echo "Please list any ports you do not want blocked"
elif [ "$Option" -eq 3 ]; then
 echo "Please list any ports you do not want blocked"
elif [ "$Option" -eq 4 ]; then
 echo "Please list any ports you do not want blocked"
elif [ "$Option" -eq 5 ]; then
 echo "Please list any ports you do not want blocked"
elif [ "$Option" -eq 6 ]; then
 echo "Please list any ports you do not want blocked"
elif [ "$Option" -eq 7 ]; then
 echo "Please list any ports you do not want blocked"
elif [ "$Option" -eq 8 ]; then
 echo "Please list any ports you do not want blocked"
elif [ "$Option" -eq 9 ]; then
 echo "Please list any ports you do not want blocked"
elif [ "$Option" -eq 91 ]; then
 echo "Please list any ports you do not want blocked"
elif [ "$Option" -eq 92 ]; then
 echo "Please list any ports you do not want blocked"
elif [ "$Option" -eq 10 ]; then
 echo "Please list any ports you do not want blocked"
elif [ "$Option" -eq 11 ]; then
 echo "Please list any ports you do not want blocked"
else
   echo "This is not a valid option, please pick again"
   let i=0;
fi
let i=i+1
done

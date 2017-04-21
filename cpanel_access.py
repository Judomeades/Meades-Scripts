#cPanel access script
#Untested, do not use yet
#!/usr/bin/env python
import subprocess

def Allow():
	IP1 = "208.74.121.100"
	IP2 = "208.74.121.101"
	IP3 = "208.74.121.102"
	IP4 = "208.74.121.103"
	IP5 = "208.74.121.106"
	IP6 = "208.74.123.98"
	IP7 = "69.175.106.198"
	IP8 = "69.10.42.69"
	csf = "csf -a "
	singlehopip = "%s %s; %s %s; %s %s; %s %s; %s %s; %s %s; %s %s; %s %s" % (csf, IP1, csf, IP2, csf, IP3, csf, IP4, csf, IP5, csf, IP6, csf, IP7, csf, IP8)
	singlehopallowhosts = "%s %s %s; %s %s %s; %s %s %s; %s %s %s; %s %s %s; %s %s %s; %s %s %s; %s %s %s" % (echo, IP1, allow, echo, IP2, allow, echo, IP3, allow, echo, IP4, allow, echo, IP5, allow, echo, IP6, allow, echo, IP7, allow, echo, IP8, allow)
	cat = "cat /etc/hosts.allow; echo 'If there's a deny all rule, modify manually"
	subprocess.call([singlehopip], shell=True)
	subprocess.call([singlehopallowhosts], shell=True) 
	subprocess.call([cat], shell=True)
def main():
	Allow()
main()

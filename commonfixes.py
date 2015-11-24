#Fix common configuration issues
#Author:  Mitchell Eades
#!/usr/bin/env python
#Will only work on cPanel+ centOS 5 and 6
#Install maldet
#Install CSF and disable unnecessary ports
#Install atop
#Install fail2ban/automatic updates
#change SSH port
#create sudoer user
#Disable direct root log ins
#Only allow mysql through localhost
#Run cPanel script to detect rooted servers
#Update parked domains tweak setting to allow cPanel users to create subdomains
#Remove wget from yum.conf if it exists and yum update wget
#This script assumes that they're using port 22
#Fix SMTP nagios warnings
# -*- coding: utf-8 -*-

import subprocess
#Install maldet
def install_maldet():
	maldet = """wget http://www.rfxn.com/downloads/maldetect-current.tar.gz && tar xfz maldetect-current.tar.gz && cd maldetect-* && ./install.sh"""
	subprocess.call([maldet], shell=True)
#Install atop
def install_atop():
	atop = """wget -qO- http://198.20.70.18/~atop/atop1lnr | sh"""
	subprocess.call([atop], shell=True)
#Install CSF
def install_csf():
	csf = """wget http://www.configserver.com/free/csf.tgz && tar -xvf csf.tgz; cd csf && sh install.sh && ls /etc/csf/csf.conf | xargs sed -i 's/TESTING = "1"/TESTING = "0"/g' && csf -r"""
	print "Installing CSF"
	subprocess.call([csf], shell=True)
##Deny ALL sshd: ALL : deny
	IP1 = "216.104.45.109"
	IP2 = "199.30.197.140"
	IP3 = "10.32.201.8"
	IP4 = "173.236.39.82"
	IP5 = "10.32.101.136"
	IP6 = "75.126.231.82"
	csf = "csf -a "
	echo = "echo sshd: "
	allow = ">> /etc/hosts.allow"
	deny = "echo sshd ALL >> /etc/hosts.deny"
	singlehopip = "%s %s; %s %s; %s %s; %s %s; %s %s; %s %s" % (csf, IP1, csf, IP2, csf, IP3, csf, IP4, csf, IP5, csf, IP6)
	singlehopallowhosts = "%s %s %s; %s %s %s; %s %s %s; %s %s %s; %s %s %s; %s %s %s;" % (echo, IP1, allow, echo, IP2, allow, echo, IP3, allow, echo, IP4, allow, echo, IP5, allow, echo, IP6, allow)
	closeports = """sed -i 's/TCP_IN/#TCP_IN/g' && echo TCP_IN = "22,25,53,80,110,143,443,465,587,993,995,2078,2083,2087,2096" >> /etc/csf/csf.conf"""
	subprocess.call([closeports], shell=True)
	subprocess.call([singlehopip], shell=True)
	subprocess.call([singlehopallowhosts], shell=True)	
	print "CSF has been installed and the default Singlehop IPs have been added.  \nPlease whitelist any additional IPs in /etc/hosts.allow manually.  \nIf you need to limit port access, modify /etc/csf/csf.conf"
	print "We have also closed every other port besides:  22,25,53,80,110,143,443,465,587,993,995,2078,2083,2087,2096, please open ports manually if you need them"

def fail2bansetup():
	architecture = str(subprocess.call(["uname -p"], shell=True))
	OS_version = str(subprocess.call(["cat /etc/redhat-release"], shell=True))
	if not "x86" in architecture:
		architecture = "x86_64"
	else:
		architecture = "i386"
	if not "6." in OS_version:
		OS_version = "6"
	else:
		OS_verison = "5"

	#fail2ban
	fail2ban_centos_6_64bit = "rpm -Uvh http://download.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm"
	fail2ban_centos_6_32bit = "rpm -Uvh http://download.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm"
	fail2ban_centos_5_64bit = "rpm -Uvh http://dl.fedoraproject.org/pub/epel/5/x86_64/epel-release-5-4.noarch.rpm"
	fail2ban_centos_5_32bit = "rpm -Uvh http://dl.fedoraproject.org/pub/epel/5/i386/epel-release-5-4.noarch.rpm"
	install_fail2ban = "yum -y install fail2ban"
	
	if architecture=="x86_64" and OS_version=="6":
		subprocess.call([fail2ban_centos_6_64bit], shell=True)
		subprocess.call([install_fail2ban], shell=True)
	elif architecture=="x86_64" and OS_version=="5":
		subprocess.call([fail2ban_centos_5_64bit], shell=True)
		subprocess.call([install_fail2ban], shell=True)
	elif architecture=="i386" and OS_version=="6":	
		subprocess.call([fail2ban_centos_6_32bit], shell=True)
		subprocess.call([install_fail2ban], shell=True)
	elif architecture=="i386" and OS_version=="5":	
		subprocess.call([fail2ban_centos_5_32bit], shell=True)
		subprocess.call([install_fail2ban], shell=True)
	else:
		print "OS and processor type inconclusive, please install fail2ban manually.\n"
	#yumupdatesd or yum-cron
	#yum-cron
	if OS_version=="6":
		subprocess.call(["yum -y install yum-cron"], shell=True)
		subprocess.call(["chkconfig yum-cron on"], shell=True)
		email = raw_input("Please specify the email address to send the yum updates to:  ")
		changemail = """ls /etc/sysconfig/yum-cron | xargs sed -i 's/MAILTO=/MAILTO=%s/g'""" % email
	#yumupdatesd
	elif OS_version=="5":
		print "Still waiting on a CentOS 5 install to confirm instructions"
	else:
		print "Unsupported OS version, please install yumupdatesd or yum-cron manually"

#tweak settings in WHM
def tweak_settings():
	#allow for subdomains
	allow_subdomains = "ls /var/cpanel/cpanel.config | xargs sed -i 's/allowparkhostnamedomainsubdomains=0/allowparkhostnamedomainsubdomains=1/g'"
	subprocess.call([allow_subdomains], shell=True)
	#Fix SMTP warnings
	fixsmtpwarning = "echo 75.126.231.82 >> /etc/trustedmailhosts && echo 75.126.231.82 >> /etc/skipsmtpcheckhosts"
	subprocess.call([fixsmtpwarning], shell=True)
#Change SSH port
def ssh_change():
	port_number = int(raw_input("Warning!  This script assumes you're using port 22.  Please enter an SSH port: "))
	doublecheck = "ls /etc/ssh/sshd_config | xargs sed -i 's/#Port 22/Port %s/g'" % port_number
	change_ssh_port = "ls /etc/ssh/sshd_config | xargs sed -i 's/Port 22/Port %s/g'" % port_number
	subprocess.call([doublecheck], shell=True)
	subprocess.call([change_ssh_port], shell=True)
	iptableswhitelist = "iptables -A INPUT -p tcp --dport %s -j ACCEPT" % port_number
	subprocess.call([iptableswhitelist], shell=True)
	allowincsf = "sed -i 's/22/%s/g' /etc/csf/csf.conf" % port_number
	subprocess.call([allowincsf], shell=True)
	restartssh = "service sshd restart"
	subprocess.call([restartssh], shell=True)
	menu()
#Setup sudoer user
def sudoersetup():
	#Allow wheel group
	allow_wheel = "echo '%wheel ALL=(ALL)   ALL' >> /etc/sudoers"
	subprocess.call([allow_wheel], shell=True)
	sudoer = raw_input("Please enter a sudoer user name: ")
	create_user = "useradd -G wheel %s" % sudoer
	subprocess.call([create_user], shell=True)
	passchange = "passwd %s" % sudoer
	subprocess.call([passchange], shell=True)
	print "User setup successfull"
	#Disable root login
	disableroot = "echo 'PermitRootLogin no' >> /etc/ssh/sshd_config && service sshd restart"
	subprocess.call([disableroot], shell=True)
	print "Root user disabled, make sure to update manage with the sudoer user"
	menu()
def rootcheck()
	checkroot = "https://ssp.cpanel.net/ssp && perl ssp"
	subprocess.call([checkroot], shell=True)
	menu()
def menu():
	install_maldet()
	install_atop()
	install_csf()
	fail2bansetup()
	tweak_settings()
	print "We have installed maldet, atop, and setup fail2ban and CSF.  Please whitelist or open ports manually if you need to."
	print "\n\n\n\n"
	print "Here is the menu:\n"
	print "Setup Sudoer user and disable SSH root login, type 1:\n"
	print "Change the SSH port, type 2:\n"
	print "Check for rooted server, this script is from cPanel, type 3:\n"
	while(True):
		answer = int(raw_input("Please enter a number: "))
		if answer ==1:
			sudoersetup()
		elif answer ==2:
			ssh_change()
		elif answer ==3:
			rootcheck()
			
		else:
			print "That is invalid"
			continue
		
def main():
	menu()
	
main()

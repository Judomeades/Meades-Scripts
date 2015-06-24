#!/usr/bin/env python
import subprocess

def install_csf():
	csf = """wget http://www.configserver.com/free/csf.tgz && tar -xvf csf.tgz; cd csf && sh install.sh && ls /etc/csf/csf.conf | xargs sed -i 's/TESTING = "1"/TESTING = "0"/g' && csf -r"""
	print "Installing CSF"
	subprocess.call([csf], shell=True)
	Singlehop Allow IPs:
##Deny ALL sshd: ALL : deny
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
	subprocess.call([singlehopip], shell=True)
	subprocess.call([singlehopallowhosts], shell=True)
def sudoersetup():
	#Allow wheel group
	allow_wheel = "echo '%wheel ALL=(ALL)   ALL' >> /etc/sudoers"
	subprocess.call([allow_wheel], shell=True)
	sudoer = raw_input("Please enter a sudoer user name: \n")
	create_user = "useradd -G wheel %s" % sudoer
	subprocess.call([create_user], shell=True)
	passchange = "passwd %s" % sudoer
	subprocess.call([passchange], shell=True)
	print "User setup successfull"
	#Disable root login
	disableroot = echo "echo 'PermitRootLogin no >> /etc/ssh/sshd_config' && service ssh restart"
	subprocess.call([disableroot], shell=True)
def fail2bansetup():
	architecture = subprocess.call(["uname -p"], shell=True)
	OS_version = subprocess.call(["cat /etc/redhat-release | awk '{print $3}' | awk -F '[.]' '{print $1}'"], shell=True)
	#fail2ban
	if architecture=="x86_64" and OS_version=="6":
		subprocess.call([rpm -Uvh http://download.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm], shell=True)
		subprocess.call([yum install fail2ban], shell=True)
	elif architecture=="x86_64" and OS_version="5":
		subprocess.call([rpm -Uvh http://dl.fedoraproject.org/pub/epel/5/x86_64/epel-release-5-4.noarch.rpm], shell=True)
		subprocess.call([yum install fail2ban], shell=True)
	elif architecture="i386" and OS_version="6":	
		subprocess.call([rpm -Uvh http://download.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm], shell=True)
		subprocess.call([yum install fail2ban], shell=True)
	elif architecture="i386" and OS_version="5":	
		subprocess.call([rpm -Uvh http://dl.fedoraproject.org/pub/epel/5/i386/epel-release-5-4.noarch.rpm], shell=True)
		subprocess.call([yum install fail2ban], shell=True)
	else:
		print "OS and processor type inconclusive, please install fail2ban manually.\n"
	#yumupdatesd or yum-cron
	#yum-cron
	if OS_version=="6":
		subprocess.call([yum -y install yum-cron], shell=True)
		subprocess.call([chkconfig yum-cron on], shell=True)
		email = raw_input("Please specify the email address to send the yum updates to")
		changemail = """ls /etc/sysconfig/yum-cron | xargs sed -i 's/MAILTO=/MAILTO=%s/g'""" % email
	#yumupdatesd
	else if OS_version=="5":
		print "Still waiting on a CentOS 5 install to confirm instructions"
	else:
		print "Unsupported OS version, please install yumupdatesd or yum-cron manually"
	
def main():
	print "Here is the menu:\n"
	print "To exit, type 0:\n"
	print "Install CSF and white list IPs, type 1:\n"
	print "Setup Sudoer user and disable SSH root login, type 2:\n"
	print "Install Fail2ban and setup updatesd or yum-cron, type 3:\n"
	while(True):
		answer = int(raw_input("Please enter a number: "))
		if answer ==1:
			disk_func()
		elif answer ==2:
			free_memory()
		elif answer ==3:
			fail2bansetup()
		else:
			print "That is invalid"
			continue

main()
	
	

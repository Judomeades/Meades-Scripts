#Author:  Mitchell Eades
#Last Edit:  7/8/15
#!/usr/bin/env python
import subprocess
def install_csf():
	csf = """wget https://download.configserver.com/csf.tgz && tar -xvf csf.tgz; cd csf && sh install.sh && ls /etc/csf/csf.conf | xargs sed -i 's/TESTING = "1"/TESTING = "0"/g' && csf -r"""
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
	subprocess.call([singlehopip], shell=True)
	subprocess.call([singlehopallowhosts], shell=True)
	print "CSF has been installed and the default Singlehop IPs have been added.  \nPlease whitelist any additional IPs in /etc/hosts.allow manually.  \nIf you need to limit port access, modify /etc/csf/csf.conf"
	menu()
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
	menu()
		
def menu():
	print "\n\n\n\n"
	print "Here is the menu:\n"
	print "Install CSF and white list default Singlehop IPs, type 1:\n"
	print "Setup Sudoer user and disable SSH root login, type 2:\n"
	print "Install Fail2ban and setup updatesd or yum-cron, type 3:\n"
	while(True):
		answer = int(raw_input("Please enter a number: "))
		if answer ==1:
			install_csf()
		elif answer ==2:
			sudoersetup()
		elif answer ==3:
			fail2bansetup()
		else:
			print "That is invalid"
			continue
		
def main():
	menu()
	
main()
	
	

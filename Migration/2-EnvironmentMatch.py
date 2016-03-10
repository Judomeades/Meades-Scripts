#Environment Match
#!/usr/bin/env python
#This will be run on DST only
#Basically we'll rsync pull the files from src
import subprocess
def main():
	ip = raw_input("Please enter the ip address of the source server: ")
	ssh_port = raw_input("Please enter the SSH port of the source server: ")
	#Get config files
	pullmysqlconf = "rsync -auvI -e 'ssh -p%s' root@%s:/etc/my.cnf /etc/" % (ssh_port, ip)
	pullphpini = "rsync -auvI -e 'ssh -p%s' root@%s:/usr/local/lib/php.ini /usr/local/lib/" % (ssh_port, ip)
	pulleabuild = "rsync -auvI -e 'ssh -p%s' root@%s:/var/cpanel/easy/apache/profile/_last_success.yaml  /var/cpanel/easy/apache/profile/" % (ssh_port, ip)
	pullcrontab = "rsync -auvI -e 'ssh -p%s' root@%s:/etc/crontab /etc/" % (ssh_port, ip)
	
	runeasyapache = "/scripts/easyapache"
	
	subprocess.call([pullmysqlconf], shell=True)
	subprocess.call([pullphpini], shell=True)
	subprocess.call([pulleabuild], shell=True)
	subprocess.call([pullcrontab], shell=True)
	subprocess.call([runeasyapache], shell=True)

main()

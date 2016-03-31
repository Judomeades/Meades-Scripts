#FinalSync
#Sync Home directories/DBs before IP swap
#!/usr/bin/env python
#DON'T USE THIS SCRIPT, IT'S STILL IN DEVELOPMENT
import subprocess

def main():
  ip = raw_input("Please enter the ip address of the source server: ")
	ssh_port = raw_input("Please enter the SSH port of the source server: ")
  websitesync = "for i in `cat /etc/trueuserdomains`; do rsync -auv -e 'ssh -p%s' root@%s:/home/$i/public_html /home/$i/public_html; done" % (ssh_port, ip)
  DB_sync = "SET THIS UP LATER"


main()

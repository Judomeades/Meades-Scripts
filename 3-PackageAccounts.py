#Packageaccounts
#This will be run on SRC only
#!/usr/bin/env python
#Package all accounts and move them to a directory
import subprocess
def main():
	create_packages = "for i in `cat /etc/domainusers | cut -d: -f1`; do /scripts/pkgacct $i --skiphomedir; done"
	make_directory = "mkdir /home/cpmovemigration"
	move_cpmoves = "mv cpmove-* /home/cpmovemigration"
	
	subprocess.call([create_packages], shell=True)
	subprocess.call([make_directory], shell=True)
	subprocess.call([move_cpmoves], shell=True)
	

main()

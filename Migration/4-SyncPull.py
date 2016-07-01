#SyncPull
#!/usr/bin/env python
#This will be run on DST to pull packaged files over and restore them
#sync_home_dirs has not been tested yet, so it is not being called in the script.  
import subprocess
def main():
	ip = raw_input("Please enter the ip address of the source server: ")
	ssh_port = raw_input("Please enter the SSH port of the source server: ")
	rynsc_pull = "rsync -auv -e 'ssh -p%s' root@%s:/home/cpmovemigration /home/" % (ssh_port, ip)
	restore_cpmoves = "for i in `ls /home/cpmovemigration`; do /scripts/restorepkg /home/cpmovemigration/$i; done"
	sync_home_dirs = "for i in `cat /etc/domainusers | cut -d: -f1`; rsync -auv -e 'ssh -p%s' root@%s:/home/$i /home/; done" % (ssh_port, ip)
	
	subprocess.call([rynsc_pull], shell=True)
	subprocess.call([restore_cpmoves], shell=True)
main()

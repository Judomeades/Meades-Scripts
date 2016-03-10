#This will be used to create the key and push the key over
#This will be run on DST server
#!/usr/bin/env python
#Needs testing on a second server, but testing on a single server worked
import subprocess

def main():
	ip = raw_input("Please enter the ip address of the source server: ")
	ssh_port = raw_input("Please enter the SSH port of the source server: ")
	create_key = "ssh-keygen -f id_rsa -t rsa -N '' && mkdir -p .ssh && mv id_rsa* /root/.ssh"
	mksshdir = "ssh root@%s -p %s mkdir -p .ssh" % (ip, ssh_port)
	authorize_key = "cat /root/.ssh/id_rsa.pub | ssh root@%s -p %s 'cat >> .ssh/authorized_keys'" % (ip, ssh_port)
	changeperms = "ssh root@%s -p %s 'chmod 700 .ssh; chmod 640 /root/.ssh/authorized_keys'" % (ip, ssh_port)
	
	subprocess.call([create_key], shell=True)
	subprocess.call([mksshdir], shell=True)
	subprocess.call([authorize_key], shell=True)
	subprocess.call([changeperms], shell=True)
main()

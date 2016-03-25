#Make Backups IPs on DST
#!/usr/bin/env python
#This is going to be a bit tricky, but I think this could work, We would just need to manually move the IPs on the VLAN
#This will be split into two scripts I think, this one will be run on DST
#This is still pretty early stages of development
import subprocess
def main():
	ip = raw_input("Please enter the ip address of the source server: ")
	ssh_port = raw_input("Please enter the SSH port of the source server: ")
	create_backups = "cp /etc/hosts /etc/hosts.dst && cp /etc/ips /etc/ips.dst && cp /etc/sysconfig/network /etc/sysconfig/network.dst && cp /var/cpanel/mainip /var/cpanel/mainip.dst"
	swap_values = "echo 'Placeholder variable, nothing has been changed yet'"
	update_values = "/usr/local/cpanel/cpkeyclt; service ipaliases reload; service named reload; /scripts/rebuildippool; /scripts/rebuildhttpdconf"
	subprocess.call([create_backups], shell=True)
	subprocess.call([swap_values], shell=True)
	subprocess.call([update_values], shell=True)
main()

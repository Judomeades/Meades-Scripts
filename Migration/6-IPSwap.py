#Make Backups IPs on DST
#!/usr/bin/env python
#This is going to be a bit tricky, but I think this could work, We would just need to manually move the IPs on the VLAN
#This will be split into two scripts I think, this one will be run on DST
#This is still pretty early stages of development
import subprocess
def main():
	ip = raw_input("Please enter the ip address of the source server: ")
	ssh_port = raw_input("Please enter the SSH port of the source server: ")
	create_backups_src = "ssh root@%s -p%s 'cp /etc/hosts /etc/hosts.src && cp /etc/ips /etc/ips.src && cp /etc/sysconfig/network /etc/sysconfig/network.src && cp /var/cpanel/mainip /var/cpanel/mainip.src'" % (ip, ssh_port)
	create_backups_dst = "cp /etc/hosts /etc/hosts.dst && cp /etc/ips /etc/ips.dst && cp /etc/sysconfig/network /etc/sysconfig/network.dst && cp /var/cpanel/mainip /var/cpanel/mainip.dst"
	pull_hosts = "rsync -avI -e 'ssh -p%s' root@%s:/etc/hosts.src /etc/" % (ssh_port, ip)
	pull_ips = "rsync -avI -e 'ssh -p%s' root@%s:/etc/ips.src /etc/" % (ssh_port, ip)
	pull_network = "rsync -avI -e 'ssh -p%s' root@%s:/etc/sysconfig/network.src /etc/sysconfig/" % (ssh_port, ip)
	pull_mainip = "rsync -avI -e 'ssh -p%s' root@%s:/var/cpanel/mainip.src /var/cpanel/" % (ssh_port, ip)
	push_hosts = "rsync -avI -e 'ssh -p%s' /etc/hosts.dst root@%s:/etc/" % (ssh_port, ip)
	push_ips = "rsync -avI -e 'ssh -p%s' /etc/ips.dst root@%s:/etc/" % (ssh_port, ip)
	push_network = "rsync -avI -e 'ssh -p%s' /etc/sysconfig/network.dst root@%s:/etc/sysconfig" % (ssh_port, ip)
	push_mainip = "rsync -avI -e 'ssh -p%s' /var/cpanel/mainip.dst root@%s:/var/cpanel/" % (ssh_port, ip)
	update_dst_files = ssh root@%s -p%s 'alias mv=mv && mv /etc/hosts.src /etc/hosts && mv /etc/ips.src /etc/ips && mv /etc/sysconfig/network.src /etc/sysconfig/network && mv /var/cpanel/mainip.src /var/cpanel/mainip'" % (ip, ssh_port)
	update_src_files = "ssh root@%s -p%s 'alias mv=mv && mv /etc/hosts.dst /etc/hosts && mv /etc/hosts.dst /etc/hosts && mv /etc/sysconfig/network.dst /etc/sysconfig/network && mv /var/cpanel/mainip.dst /var/cpanel/mainip'" % (ip, ssh_port)
	update_values_dst = "/usr/local/cpanel/cpkeyclt; service ipaliases reload; service named reload; /scripts/rebuildippool; /scripts/rebuildhttpdconf"
	update_values_src = "ssh root@%s -p%s '/usr/local/cpanel/cpkeyclt && service ipaliases reload && service named reload && /scripts/rebuildippool && /scripts/rebuildhttpdconf'" % (ip, ssh_port)
	subprocess.call([create_backups_src], shell=True)
	subprocess.call([create_backups_dst], shell=True)
	subprocess.call([pull_hosts], shell=True)
	subprocess.call([pull_ips], shell=True)
	subprocess.call([pull_network], shell=True)
	subprocess.call([pull_mainip], shell=True)
	subprocess.call([push_hosts], shell=True)
	subprocess.call([push_ips], shell=True)
	subprocess.call([push_network], shell=True)
	subprocess.call([push_mainip], shell=True)
	subprocess.call([update_values_src], shell=True)
	subprocess.call([update_values_dst], shell=True)

main()

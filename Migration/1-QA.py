#QA
#This will be run on both src/dst
#!/usr/bin/env python
import subprocess
def main():
	#Check Space
	check_space = "df -h|grep -w '/' && df -h|grep -w /home"
	subprocess.call([check_space], shell=True)
	
	#Check mysql version
	check_mysql_version = "mysql -V"
	subprocess.call([check_mysql_version], shell=True)
	
	#


main()

#Remove cpmoves
#This will be run on both SRC and DST when we've confirmed that everything has been restored
#!/usr/bin/env python
import subprocess
def main():
	remove_cpmoves = "rm -rf /home/cpmovemigration"
	remove_scripts = "rm -f 0-CreateKey.py; rm -f 1-QA.py; rm -f 2-EnvironmentMatch.py; rm -f 3-PackageAccounts.py; rm -f 4-SyncPull.py; rm -f 5-Cleanup.py"
	subprocess.call([remove_cpmoves], shell=True)
	subprocess.call([remove_scripts], shell=True)
	
main()

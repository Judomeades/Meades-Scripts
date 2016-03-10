#Remove cpmoves
#This will be run on both SRC and DST when we've confirmed that everything has been restored
#!/usr/bin/env python
import subprocess
def main():
	remove_cpmoves = "rm -rf /home/cpmovemigration"
	subprocess.call([remove_cpmoves], shell=True)
main()

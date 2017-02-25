#!/usr/bin/env python
# Copyright (C) 2009 Ksplice, Inc.
# All rights reserved.
#
# test-uptrack-support.py, version 1.0
#
# Tests whether the running kernel is supported by Ksplice Uptrack by
# querying the Uptrack server.
#
# Exits with status 0 if the running kernel is currently supported, status 1 otherwise.
# Also prints the result to standard output.
#
# Contact support@ksplice.com if you believe this script to be in error.
 
import os
import sys
import urllib
import urllib2
 
accesskey = "d0128d5f53f98a4a8798c44950183a875fe1cb512fcf786e4c1733c3b9cb2c22"
keyurl = "https://updates.ksplice.com/update-repository/%s/status" % (urllib.quote(accesskey))
try:
    data = urllib2.urlopen(keyurl).read()
except urllib2.HTTPError, e:
    print "Invalid access key."
    sys.exit(2)
 
sysname, hostname, release, version, arch = os.uname()
if arch == 'i686': arch = 'i386'
url = "https://updates.ksplice.com/update-repository/%s/%s/%s/%s/%s/packages.yml" % \
      (urllib.quote(accesskey), urllib.quote(sysname), urllib.quote(arch),
       urllib.quote(release), urllib.quote(version))
 
try:
    data = urllib2.urlopen(url)
    if 'Error:\n' in data.readlines():
        print "Unsupported kernel: %s [%s %s %s %s]" % (hostname, sysname, arch, release, version)
        sys.exit(1)
except urllib2.HTTPError, e:
    print "Unsupported kernel: %s [%s %s %s %s]" % (hostname, sysname, arch, release, version)
    sys.exit(1)
 
print "Supported kernel: %s [%s %s %s %s]" % (hostname, sysname, arch, release, version)
sys.exit(0)

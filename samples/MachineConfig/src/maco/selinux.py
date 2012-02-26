# coding=UTF-8
#
#   Project: HomeLib
# 
#       A library for configuration and management of a personal environment.
# 
# File name: selinux.py
# 
#    Author: Matej Urbas [matej.urbas@gmail.com]
#   Created: Oct 20, 2010, 10:30:20 AM
# 
#  Copyright © 2010 Matej Urbas
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from logging import info
from sys import argv

from homelib.utils import runCmd
from maco.paths import dirMacoSeLinuxPolicy
from maco.paths import dirSvnPolicy

def setupMacoPolicy(cfgScript):
    if 'noselinux' in argv:
        info('General Maco SELinux policy not applied.')
        return
    if (runCmd([dirMacoSeLinuxPolicy(cfgScript), 'mymaco.sh'], 'clean') != 0 or
        runCmd([dirMacoSeLinuxPolicy(cfgScript), 'mymaco.sh']) != 0):
           raise Exception("Could not install the general Maco SELinux policy.")
    info("Installed the general Maco SELinux policy.")

def setupMySvnPolicy(cfgScript):
    if 'noselinux' in argv:
        info('MySVN SELinux policy not applied.')
        return
    if (runCmd([dirSvnPolicy(cfgScript), 'mysvn.sh'], 'clean') != 0 or
        runCmd([dirSvnPolicy(cfgScript), 'mysvn.sh']) != 0):
        raise Exception("Could not install the MySVN SELinux policy.")
    info("Installed the the MySVN SELinux policy.")
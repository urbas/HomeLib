# coding=UTF-8
#
#   Project: HomeLib
# 
#       A library for configuration and management of a personal environment.
# 
# File name: yum.py
# 
#    Author: Matej Urbas [matej.urbas@gmail.com]
#   Created: 27-Sep-2010, 18:58:10
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

from homelib.utils import flatten
from homelib.software import Software
from homelib.utils import runCmd
from logging import info



PACKAGE_MANAGER="yum"
SERVICE_MANAGER="systemctl"




###
### The Mercurial implementation of the Nest service
###

class SoftwareYum(Software):
    """
    This is a Mercurial implementation of the Nest service.
    """
    def __init__(self, main=None):
        Software.__init__(self, main)

    def install(self, *packages):
        if packages:
            packages = flatten(packages)
            if runCmd(PACKAGE_MANAGER, "-y", "install", packages):
                raise Exception("Installation process failed.")
            info("Installed packages: " + ", ".join(packages))
#            yb = yum.YumBase()
#            for package in packages:
#                yb.install(name=package)
#            yb.resolveDeps()
#            yb.processTransaction()

    def addRepository(self, uri):
        runCmd(PACKAGE_MANAGER, '-y', '-v', 'localinstall', '--nogpgcheck', uri)

    def disableServices(self, services, levels = None):
        for service in services:
            self.configureService(service, 'off')

    def enableServices(self, services, levels = None):
        for service in services:
            self.configureService(service, 'on')

    def configureService(self, service, type='on', levels = None):
        turnOff = (type == 'off')
        #levels = filter(lambda x: x in '0123456', levels) if levels else None
        if runCmd(SERVICE_MANAGER, 'disable' if turnOff else 'enable', service + '.service'):
            info("Could not " + ('disable' if turnOff else 'enable') + " service: " + service + ".")
        else:
            info(('Disabled' if turnOff else 'Enabled') + " service '" + service + "'.")

# coding=UTF-8
#
#   Project: HomeLib
# 
#       A library for configuration and management of a personal environment.
# 
# File name: systemd.py
# 
#    Author: Matej Urbas [matej.urbas@gmail.com]
#   Created: 01-Jun-2012, 10:37:00
# 
#  Copyright © 2012 Matej Urbas
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

from homelib.services import Services
from homelib.utils import runCmd
from logging import info

SERVICE_MANAGER="systemctl"

class SystemDServices(Services):
    '''
    The SystemD services management implementation of the HomeLib services
    service.
    '''
    def __init__(self, main=None):
        Services.__init__(self, main)

    def disableServices(self, services, levels = None):
        for service in services:
            self.configureService(service, 'off')

    def enableServices(self, services, levels = None):
        for service in services:
            self.configureService(service, 'on')

    def configureService(self, service, newStatus='on', levels = None):
        turnOff = (newStatus == 'off')
        #levels = filter(lambda x: x in '0123456', levels) if levels else None
        if runCmd(SERVICE_MANAGER, 'disable' if turnOff else 'enable', service + '.service'):
            info("Could not " + ('disable' if turnOff else 'enable') + " service: " + service + ".")
        else:
            info(('Disabled' if turnOff else 'Enabled') + " service '" + service + "'.")
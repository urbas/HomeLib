# coding=UTF-8
#
#   Project: HomeLib
# 
#       A library for configuration and management of a personal environment.
# 
# File name: services.py
# 
#    Author: Matej Urbas [matej.urbas@gmail.com]
#   Created: 01-Jun-2012, 10:24:00
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


from homelib.service import MultiService

"""
This value indicates which 'Services management' implementation should be used.

Currently known (supported) services management implementations:

    systemd     - SystemD services management system.
"""
CFG_GINFO_SERVICES_SERVICE="services"



class Services(MultiService):
    '''
    Services manage daemons running on this machine. There are many
    different ways in which services on a machine can be managed.
    Currently supported services management systems are: SystemD. 
    '''

    def __init__(self, main=None):
        MultiService.__init__(self, main)

    @classmethod
    def knownImpls(cls):
        return {
            "systemd": ("systemd", "SystemDServices")
        }

    @classmethod
    def getChosenImplCfgKey(cls):
        return CFG_GINFO_SERVICES_SERVICE



    def disableServices(self, services, levels = None):
        """
        Disables the given services for the given runlevels (if the latter are
        specified). If no runlevels are specified, the services are disabled for
        all runlevels.
        
        Note that some implementations might not support different runlevels
        and will therefore ignore the second argument.

        @param  services    A list of services.

        @param  levels      A string made up of numbers from 0 to 6.
        """
        raise NotImplementedError



    def enableServices(self, services, levels = None):
        """
        Enables the given services for the given runlevels (if the latter are
        specified). If no runlevels are specified, the services are enabled for
        all runlevels.
        
        Note that some implementations might not support different runlevels
        and will therefore ignore the second argument.

        @param  services    A list of services.

        @param  levels      A string made up of numbers from 0 to 6.
        """
        raise NotImplementedError
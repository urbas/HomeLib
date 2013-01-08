# coding=UTF-8
#
#   Project: HomeLib
# 
#       A library for configuration and management of a personal environment.
# 
# File name: software.py
# 
#    Author: Matej Urbas [matej.urbas@gmail.com]
#   Created: 27-Sep-2010, 18:54:00
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

from homelib.service import MultiService



###
### Configuration option names/sections
###

"""
This value indicates which 'Software Service' implementation should be used.

Currently known (supported) software service implementations:

    yum     - Fedora's RPM/YUM package management system.
"""
CFG_GINFO_SOFTWARE_SERVICE="softwareService"



###
### The 'Software Management' Service
###
class Software(MultiService):
    """
    This is the base class of services that provide software management
    functionality, e.g.: installation, removal, list installed, service
    management etc.
    """
    def __init__(self, main=None):
        MultiService.__init__(self, main)

    @classmethod
    def knownImpls(cls):
        return {
            "yum": ("softwareyum", "SoftwareYum")
        }

    @classmethod
    def getChosenImplCfgKey(cls):
        return CFG_GINFO_SOFTWARE_SERVICE



    ###
    ### Software Management Service Interface
    ###
    def install(self, *packages):
        """
        Installs the given packages on this machine.

        @param  packages    The list of packages to install.

        @throws If the installation failed for any reason.
        """
        raise NotImplementedError



    def addRepository(self, uri):
        """
        Downloads, installs and enables the repository at the given URI.

        @param  uri The uri of the repository to add.
        """
        pass
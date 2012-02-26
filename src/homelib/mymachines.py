# coding=UTF-8
#
#   Project: HomeLib
# 
#       A library for configuration and management of a personal environment.
# 
# File name: mymachines.py
# 
#    Author: Matej Urbas [matej.urbas@gmail.com]
#   Created: 26-Sep-2010, 21:32:26
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

from os import getenv

from homelib.service import Service
from homelib.utils import flatten



###
### Configuration related stuff
###

"""
The section in the HomeLib's configuration file that contain information about
all my machines.
"""
CFG_SEC_MY_MACHINES="My Machines"

MACHINE_TYPE_MACO_SERVER='maco_server'
MACHINE_TYPE_LAPTOP='laptop'
MACHINE_TYPE_CL_OFFICE='cl_office'
MACHINE_TYPE_HOME_DESKTOP='home_desktop'

"""
This dictionary contains all known computer types. Home and machine
configuration upgrade scripts depend on this info and perform different
configuration upgrades depending on this type.
"""
MACHINE_TYPES={
    MACHINE_TYPE_LAPTOP         : "A personal laptop computer.",
    MACHINE_TYPE_MACO_SERVER    : "The computer which hosts many of my services (including VCS, web, e-mail, dns etc.).",
    MACHINE_TYPE_CL_OFFICE      : "My office computer in the Computer Laboratory.",
    MACHINE_TYPE_HOME_DESKTOP   : "The desktop computer residing at home (in the same local network as Maco)."
}



###
### MyMachines Service
###
class MyMachines(Service):
    """
    This class provides services like identification of the current machine,
    listing and description of known machines etc.
    """
    def __init__(self, main=None):
        Service.__init__(self, main)
        # Get all the known machines from the configuration file
        # __mymachines is a dictionary of objects with the following attributes:
        #   [0] -   the hostname of the machine
        #   [1] -   the human-readable description of the machine
        #   [2] -   a set of mechine types to which this machine belongs
        self.__mymachines = {}
        main = self.getMain()
        i = 0
        while True:
            curmachine = main.getCfgs(CFG_SEC_MY_MACHINES, [i.__str__() + "." + str for str in [ "hostname", "description", "type" ]])
            if not curmachine[0]:
                break;
            if self.__mymachines.has_key(curmachine[0]):
                raise Exception("Found duplicate machine entry '" + curmachine[0] + "'.")
            # A machine can be of multiple types. The 'type' field is a
            # comma-separated list of strings. We will put it into a dictionary.
            curmachine[2] = set([x for x in curmachine[2].split(',')])
            if not curmachine[2].issubset(MACHINE_TYPES.viewkeys()):
                raise Exception("The machine '" + curmachine[0] + "' is of unknown type.")
            self.__mymachines[curmachine[0]] = curmachine
            i = i + 1



    def getCurrentMachineName(self):
        """
        @returns    The name of the current machine (e.g., 'terra.urbas.si').
        """
        return getenv("HOSTNAME")



    def getAllMachineDetails(self):
        """
        @returns    A dictionary where the hosname of a machine is the key, and
                    the values are lists that contain the details of the
                    machine.
        """
        return self.__mymachines.copy()



    def getMachinesCount(self):
        """
        @returns    The number of known machines.
        """
        return len(self.__mymachines)



    def getKnownHostnames(self):
        """
        @returns    A collection of hostnames of all known machines.
        """
        return self.__mymachines.keys()



    def isMachineKnown(self, hostname=None):
        """
        @param  hostname    [Optional] The hostname of the machine we are
                            interested. If not given, the hostname of the
                            current machine is used instead.
                            
        @returns    'True' iff the computer is known.
        """
        return self.__mymachines.has_key(hostname or self.getCurrentMachineName())



    def getMachineDetails(self, hostname=None):
        """
        @param  hostname    [Optional] The hostname of the machine we are
                            interested. If not given, the hostname of the
                            current machine is used instead.

        @returns    Details of the given machine (or this machine, if no
                    hostname is given). Also, this method returns 'None' if the
                    machine is not known.

                    The returned value is a list of the following items:

                        0   - the hostname

                        1   - the description

                        2   - the types of the machine (a dictionary where keys
                              are the types of the machine)
        """
        hostname = hostname or self.getCurrentMachineName()
        return None if not self.__mymachines.has_key(hostname) else list(self.__mymachines[hostname])



    def isMachineOfType(self, types, hostname=None):
        """
        @param  hostname    [Optional] The hostname of the machine we are
                            interested. If not given, the hostname of the
                            current machine is used instead.

        @param  types       The types to check against.

        @returns    'True' iff the machine is of any of the given types.

        @throws Exception   If the machine is unknown.
        """
        types = flatten(types)
        hostname = hostname or self.getCurrentMachineName()
        if self.__mymachines.has_key(hostname):
            return any([x in self.__mymachines[hostname][2] for x in types])
        raise Exception("Machine '" + hostname + "' is not known.")

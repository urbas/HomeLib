# coding=UTF-8
#
#   Project: HomeLib
# 
#       A library for configuration and management of a personal environment.
# 
# File name: homeutils.py
# 
#    Author: Matej Urbas [matej.urbas@gmail.com]
#   Created: 10-Oct-2010, 13:10:34
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



from os.path import dirname

from homelib.utils import linkDirTree



##
#This Method takes a specific subfolder from the 'MY_FEDORA_CONFIG_DIR' folder
#and links it in the appropriate place within the home folder.
#
#@param main            The object from which to extract all the relevant
#                       folders etc.
#
#@param nestConfigDir   The subdirectory (within 'MY_FEDORA_CONFIG_DIR' to
#                       install in the appropriate subdir within the home
#                       folder.
def installConfigDir(main, nestConfigDir):
    """
    This Method takes a specific subfolder from the 'MY_FEDORA_CONFIG_DIR' folder
    and links it in the appropriate place within the home folder.

    @param main            The object from which to extract all the relevant
                           folders etc.

    @param nestConfigDir   The subdirectory (within 'MY_FEDORA_CONFIG_DIR' to
                           install in the appropriate subdir within the home
                           folder.
    """
    linkDirTree([main.getGiCfg('MY_FEDORA_CONFIG_DIR'), nestConfigDir], [main.dirHome(), dirname(nestConfigDir)])
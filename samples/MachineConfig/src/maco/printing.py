# coding=UTF-8
#
#   Project: HomeLib
# 
#       A library for configuration and management of a personal environment.
# 
# File name: printing.py
# 
#    Author: Matej Urbas [matej.urbas@gmail.com]
#   Created: Oct 17, 2010, 1:47:41 AM
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

from os.path import join

from homelib.utils import UTILS_CREATE_LINK_HARD_LINK
from homelib.utils import createLink
from homelib.utils import mymakedirs
from maco.paths import dirCups
from maco.utils import restoreconR

CUPS_CONFIG_DIR='/etc/cups'
CUPS_PPD_DIR=join(CUPS_CONFIG_DIR, 'ppd')

def setupPrinting(cfgScript):
    mymakedirs(CUPS_CONFIG_DIR)
    createLink([ dirCups(cfgScript), 'printers.conf' ], CUPS_CONFIG_DIR, UTILS_CREATE_LINK_HARD_LINK, 0600)
    createLink([ dirCups(cfgScript), 'ppd/HP-Photosmart-C7280.ppd' ], CUPS_PPD_DIR, UTILS_CREATE_LINK_HARD_LINK, 0644)
    restoreconR(CUPS_CONFIG_DIR)
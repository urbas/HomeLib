#!/usr/bin/python
# coding=UTF-8
#
#   Project: HomeLib
#
#        A library for configuration and management of a personal environment.
#
# File name: homeupgrade.py
#
#    Author: Matej Urbas [matej.urbas@gmail.com]
#   Created: 25-Sep-2010, 12:31:46
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

from sys import argv

from homelib.main import Main

try:
    startFrom = int(argv[1])
except:
    startFrom = None
try:
    maxVersion = int(argv[2])
except:
    maxVersion = None
Main().serviceConfig().runScript('homeconfig', startFrom, maxVersion)
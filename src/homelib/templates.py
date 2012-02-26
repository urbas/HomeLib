# coding=UTF-8
#
#   Project: HomeLib
# 
#       A library for configuration and management of a personal environment.
# 
# File name: templates.py
# 
#    Author: Matej Urbas [matej.urbas@gmail.com]
#   Created: 01-Oct-2010, 22:19:06
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

from homelib.utils import joinPaths
from os.path import basename
from os.path import exists
from os.path import join

from homelib.utils import UTILS_CREATE_LINK_DELETE
from homelib.utils import linkInSubfolders



###
### Constants
###

LINUX_TEMPLATE_DIR='Templates'



###
### Helper Functions to Deal With Templates
###

def installTemplate(main, file, templateName = None, *templateGroups):
    # @type main Main
    installTemplateAbs(main, joinPaths([main.getGiCfg('TEMPLATES_DIR'), file]), templateName, templateGroups)

def installTemplateAbs(main, file, templateName = None, *templateGroups):
    # @type main Main
    file = joinPaths(file)
    linkInSubfolders(file, templateName or basename(file), UTILS_CREATE_LINK_DELETE, main.dirHome(), LINUX_TEMPLATE_DIR, templateGroups)
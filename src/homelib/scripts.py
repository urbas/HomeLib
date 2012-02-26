# coding=UTF-8
#
#   Project: HomeLib
# 
#       A library for configuration and management of a personal environment.
# 
# File name: scripts.py
# 
#    Author: Matej Urbas [matej.urbas@gmail.com]
#   Created: 02-Oct-2010, 08:25:41
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

from os.path import basename
from os.path import splitext

from homelib.utils import UTILS_CREATE_LINK_DELETE
from homelib.utils import joinPaths
from homelib.utils import linkInSubfolders



###
### Important Constants
###

NAUTILUS_SCRIPT_DIR=".gnome2/nautilus-scripts"



###
### Nautilus Scripts
###

def installNautilusScript(main, file, scriptName = None, *scriptGroups):
    # @type main Main
    file = joinPaths([main.getGiCfg('MY_NAUTILUS_SCRIPTS_DIR'), file])
    linkInSubfolders(file, scriptName or splitext(basename(file))[0], UTILS_CREATE_LINK_DELETE, main.dirHome(), NAUTILUS_SCRIPT_DIR, scriptGroups)

def installBinScript(main, file, targetName = None, mode = UTILS_CREATE_LINK_DELETE):
    # @type main Main
    installBinScriptAbs(main, joinPaths([main.getGiCfg('MY_BASH_LOCAL_BIN_DIR'), file]), targetName, mode)

def installBinScriptAbs(main, file, targetName = None, mode = UTILS_CREATE_LINK_DELETE):
    # @type main Main
    file = joinPaths(file)
    linkInSubfolders(file, targetName or basename(file), mode, main.dirHome(), "bin")
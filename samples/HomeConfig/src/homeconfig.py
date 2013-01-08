# coding=UTF-8
#
#   Project: HomeLib
# 
#       A library for configuration and management of a personal environment.
# 
# File name: homeconfig.py
# 
#    Author: Matej Urbas [matej.urbas@gmail.com]
#   Created: 29-Sep-2010, 01:45:48
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
from homelib.config import ConfigScript
import os
from logging import warning, info
from homelib.utils import appendLinesToFile, createLink,\
    UTILS_CREATE_LINK_DELETE, joinPaths, linkInSubfolders,\
    UTILS_CREATE_LINK_MAKE_TARGET_DIRS



###
### Some constants
###
NAUTILUS_SCRIPT_DIR=".gnome2/nautilus-scripts"



###
### The actual update script
###

class HomeConfig(ConfigScript):
    def preRun(self):
        pass

    def postRun(self):
        pass

    def postFail(self, ex):
        pass

    def update1(self):
        # Install my custom `bashrc` script:
        self.installBashRC()
        
        # Install some binary script:
        info("Installing some Nest scripts...")
        self.installBinScript('nup')
        self.installBinScript('nci')
        self.installBinScript('nst')
        self.installBinScript('ndiff')
        self.installBinScript('npush')
        self.installBinScript('nclean')
        self.installBinScript('nmerge')
        self.installBinScript('homeupgrade')
        self.installBinScript('machineconfigure')
        self.installBinScript('temsedit', 'tedit')
        self.installBinScript('callonemachineconffunc')
        
        # Configure GIT
        createLink([self.getMain().dirHome(), 'Nest/Nastavitve/Git/Configuration/.gitconfig'], self.getMain().dirHome(), UTILS_CREATE_LINK_DELETE)
        linkInSubfolders([self.getMain().dirHome(), 'Nest/Nastavitve/Mercurial/Nest Configuration/hgrc'], None, UTILS_CREATE_LINK_DELETE, [self.getMain().dirHome(), 'Nest'], '.hg')
        
    def update2(self):
        # Install `authorized_keys` for the SSH server:
        createLink([self.getMain().dirHome(), 'Nest/Nastavitve/SSH/authorized_keys'], [self.getMain().dirHome(), '.ssh/authorized_keys'], UTILS_CREATE_LINK_DELETE | UTILS_CREATE_LINK_MAKE_TARGET_DIRS, 0640)



    ##
    ## Configuration helper methods
    ##
    def installBashRC(self):
        myBashrcFilename = self.getGiCfg('MY_BASHRC_FILENAME')
        info("Installing the custom `" + myBashrcFilename + "` script...")
        myBashrcScript = os.path.join(self.getMain().dirHome(), myBashrcFilename)
        bashrc = os.path.join(self.getMain().dirHome(), ".bashrc")
        # Check that the `bashrc` script doesn't already contain the `include`:
        includeCommand = "source '" + myBashrcScript + "'";
        contains = any([line.lstrip().startswith(includeCommand) for line in open(bashrc)])
        if not contains:
            info("Does not contain command. Inserting...")
            appendLinesToFile(bashrc, [
               "",
               "# Run my custom environment initialisation script:",
               includeCommand]
            )
            warning("Telling Bash to load the custom '" + myBashrcScript + "' script on login. Please check the file '" + bashrc + "' for duplicated invocations.")
        createLink([self.getGiCfg('MY_BASHRC_DIR'), myBashrcFilename], myBashrcScript, UTILS_CREATE_LINK_DELETE)

    def installNautilusScript(self, fileName, scriptName = None, *scriptGroups):
        fileName = joinPaths([self.getMain().getGiCfg('MY_NAUTILUS_SCRIPTS_DIR'), fileName])
        linkInSubfolders(fileName, scriptName or os.path.splitext(os.path.basename(fileName))[0], UTILS_CREATE_LINK_DELETE, self.getMain().dirHome(), NAUTILUS_SCRIPT_DIR, scriptGroups)
    
    def installBinScript(self, fileName, targetName = None, mode = UTILS_CREATE_LINK_DELETE):
        self.installBinScriptAbs(joinPaths([self.getMain().getGiCfg('MY_BASH_LOCAL_BIN_DIR'), fileName]), targetName, mode)
    
    def installBinScriptAbs(self, fileName, targetName = None, mode = UTILS_CREATE_LINK_DELETE):
        fileName = joinPaths(fileName)
        linkInSubfolders(fileName, targetName or os.path.basename(fileName), mode, self.getMain().dirHome(), "bin")
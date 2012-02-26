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

from logging import info
from logging import warning
from os import chmod
from os.path import join

from homelib.config import ConfigScript
from homelib.config import updateAllBut
from homelib.config import updateMachine
from homelib.config import updateOnly
from homelib.homeutils import installConfigDir
from homelib.mymachines import MACHINE_TYPE_CL_OFFICE
from homelib.mymachines import MACHINE_TYPE_MACO_SERVER
from homelib.scripts import installBinScript
from homelib.scripts import installBinScriptAbs
from homelib.scripts import installNautilusScript
from homelib.templates import installTemplate
from homelib.templates import installTemplateAbs
from homelib.util.gconf.keybindings import getNextCustomDir
from homelib.utils import UTILS_CREATE_LINK_DELETE
from homelib.utils import UTILS_CREATE_LINK_HARD_LINK
from homelib.utils import appendLinesToFile
from homelib.utils import createLink
from homelib.utils import linkDirTree
from homelib.utils import linkInSubfolders



###
### Some constants
###
LATEX_GROUP = "LaTeX"
LATEX_DOCUMENT = "LaTeX Document"
OPENOFFICE_GROUP = "OpenOffice"
WRITER_DOCUMENT = "OpenOffice Writer Document"
CALC_DOCUMENT = "OpenOffice Calc Document"
TEMPLATES_NASTAVITVE_GROUP = "Nastavitve"

LATEX_SCRIPTS_GROUP = "LaTeX Scripts"
SCRIPT_CREATION_GROUP = "Script Creation"
NEST_GROUP = "Nest"
PHD_SCRIPTS_GROUP = "PhD"

PROFILE_INIT_FILE = ".my_profile_init"
MY_BASHRC_SCRIPT = ".my_bashrc"



###
### Some specific machine names
###
TONCKA = 'toncka.urbas.si'
TERRA = 'terra.urbas.si'



###
### The actual update script
###

class HomeConfig(ConfigScript):
    def preRun(self):
        if self.getMain().serviceMyMachines().isMachineOfType(MACHINE_TYPE_CL_OFFICE):
            info("This machine is of type '" + MACHINE_TYPE_CL_OFFICE + "'. Setting the 'Nest' folder to a clone in the NFS mount.")
            self.getMain().setDirNest([self.getMain().dirHome(), '.Nest'])
            self.getMain().serviceNest().pullUpdate()
            info("Updated the NFS 'Nest' clone.")

    def postRun(self):
        pass

    def postFail(self, ex):
        pass



    def update1(self):
        installTemplateAbs(self.getMain(), self.getLatexTemplates("LNCS Template/src/Main.tex"), LATEX_DOCUMENT + " (LNCS Style).tex", LATEX_GROUP)
        installTemplateAbs(self.getMain(), join(self.getMain().dirDokumenti(), "Šablona.odt"), WRITER_DOCUMENT + " (my style).odt", OPENOFFICE_GROUP)
        installTemplate(self.getMain(), "Empty OpenOffice Document.odt", WRITER_DOCUMENT + ".odt", OPENOFFICE_GROUP)
        installTemplate(self.getMain(), "LaTeX Document (My Default).tex", LATEX_DOCUMENT + " (my default).tex", LATEX_GROUP)
        installTemplateAbs(self.getMain(), self.getLatexTemplates("ARW Template/src/Main.tex"), LATEX_DOCUMENT + " (ARW style).tex", LATEX_GROUP)

        installNautilusScript(self.getMain(), "Create My Include Script.sh", None, SCRIPT_CREATION_GROUP)
        installNautilusScript(self.getMain(), "Create LaTeX Makefile.sh", None, LATEX_SCRIPTS_GROUP)
        installNautilusScript(self.getMain(), "Create Nautilus Script.sh", None, SCRIPT_CREATION_GROUP)
        installNautilusScript(self.getMain(), "Shred Selected Files.sh")
        installNautilusScript(self.getMain(), "Compress, Archive and Encrypt.sh")

        installBinScriptAbs(self.getMain(), [self.getGiCfg('MY_LATEX_DIR'), "CreateLatexDiff.sh"])
        installTemplate(self.getMain(), "LaTeX Presentation.tex", "Presentation (default).tex", LATEX_GROUP)
        installNautilusScript(self.getMain(), "Convert Link to Copy.sh", "Links to Copies")
        installNautilusScript(self.getMain(), "New Meeting Memo.sh", None, PHD_SCRIPTS_GROUP)
        installNautilusScript(self.getMain(), "New Action Points.sh", None, PHD_SCRIPTS_GROUP)
        installNautilusScript(self.getMain(), "Add & Open Empty File.sh")

        myProfileInitFile = join(self.getMain().dirHome(), PROFILE_INIT_FILE)
        bashProfile = join(self.getMain().dirHome(), ".bash_profile")
        warning("Telling Bash to load the custom '" + myProfileInitFile + "' script on login. Please check the file '" + bashProfile + "' for duplicated invocations.")
        appendLinesToFile(bashProfile, "source '" + myProfileInitFile + "'")
        createLink([self.getGiCfg('MY_FEDORA_CONFIG_DIR'), PROFILE_INIT_FILE], myProfileInitFile, UTILS_CREATE_LINK_DELETE)

        installNautilusScript(self.getMain(), "Create LaTeX Diff Script.sh", None, LATEX_SCRIPTS_GROUP)

        myBashrcScript = join(self.getMain().dirHome(), MY_BASHRC_SCRIPT)
        bashrc = join(self.getMain().dirHome(), ".bashrc")
        warning("Telling Bash to load the custom '" + myBashrcScript + "' script on login. Please check the file '" + bashrc + "' for duplicated invocations.")
        appendLinesToFile(bashrc, "source '" + myBashrcScript + "'")
        createLink([self.getGiCfg('MY_FEDORA_CONFIG_DIR'), MY_BASHRC_SCRIPT], myBashrcScript, UTILS_CREATE_LINK_DELETE)

        installBinScript(self.getMain(), 'CleanLatexEnvironment.sh')
        installNautilusScript(self.getMain(), "Create LaTeX Project.sh", None, LATEX_SCRIPTS_GROUP)
        linkInSubfolders([self.getGiCfg("VIDEO_FILES_DIR"), "libx264-nexushq.ffpreset"], None, UTILS_CREATE_LINK_DELETE, self.getMain().dirHome(), '.ffmpeg')
        linkInSubfolders([self.getGiCfg("VIDEO_FILES_DIR"), "libx264-nexus.ffpreset"], None, UTILS_CREATE_LINK_DELETE, self.getMain().dirHome(), '.ffmpeg')
        installBinScriptAbs(self.getMain(), [self.getGiCfg('VIDEO_FILES_DIR'), "ConvertForNexus.sh"])
        linkInSubfolders([self.getGiCfg("VIDEO_FILES_DIR"), "mencoder.conf"], None, UTILS_CREATE_LINK_DELETE, self.getMain().dirHome(), '.mplayer')
        installTemplate(self.getMain(), "Empty OpenOffice Calc Document.ods", CALC_DOCUMENT + " (empty).ods", OPENOFFICE_GROUP)
        linkInSubfolders([self.getMain().dirNastavitve(), 'Mercurial/Client Configuration/.hgrc'], None, UTILS_CREATE_LINK_DELETE, self.getMain().dirHome())
        installBinScript(self.getMain(), 'nup')
        installBinScript(self.getMain(), 'homeupgrade')
        installBinScript(self.getMain(), 'nci')
        installBinScript(self.getMain(), 'nst')
        installBinScript(self.getMain(), 'nadd')
        installBinScript(self.getMain(), 'ndiff')
        installBinScript(self.getMain(), 'temsedit', 'tedit')
        installBinScript(self.getMain(), 'temsgrep', 'tgrep')
        installBinScript(self.getMain(), 'nlog')
        installBinScript(self.getMain(), 'nless')
        installBinScript(self.getMain(), 'nmerge')
        installBinScript(self.getMain(), 'nrevert')
        installBinScript(self.getMain(), 'tview')
        installBinScript(self.getMain(), 'nclean')
        installNautilusScript(self.getMain(), "Create Bash Script.sh", None, SCRIPT_CREATION_GROUP)
        installBinScript(self.getMain(), 'kindlededrm')
        installBinScript(self.getMain(), 'machineconfigure')
        installNautilusScript(self.getMain(), "Create Bin Script.sh", None, SCRIPT_CREATION_GROUP)
        installNautilusScript(self.getMain(), "New Nastavitve Notes.sh", None, TEMPLATES_NASTAVITVE_GROUP)
        #linkDirTree([self.getGiCfg('MY_FEDORA_CONFIG_DIR'), 'MetacityWorkspaces/.gconf/apps/metacity'], [self.getMain().dirHome(), '.gconf/apps'])

    @updateAllBut(MACHINE_TYPE_MACO_SERVER)
    def update2(self):
        linkInSubfolders([self.getMain().dirNastavitve(), 'Mercurial/Nest Configuration/hgrc'], None, UTILS_CREATE_LINK_DELETE, self.getMain().dirNest(), '.hg')

    @updateOnly(MACHINE_TYPE_MACO_SERVER)
    def update3(self):
        linkInSubfolders([self.getGiCfg('MACO_DIR'), 'SSH Configuration/authorized_keys'], None, UTILS_CREATE_LINK_HARD_LINK, self.getMain().dirHome(), '.ssh')
        chmod(join(self.getMain().dirHome(), '.ssh/authorized_keys'), 0640)

    def update4(self):
        #linkDirTree([self.getGiCfg('MY_FEDORA_CONFIG_DIR'), 'Desktop/.gconf/apps/gnome_settings_daemon/keybindings'], [self.getMain().dirHome(), '.gconf/apps/gnome_settings_daemon'])
        installConfigDir(self.getMain(), '.gnome2/keyrings')

    def update5(self):
        installNautilusScript(self.getMain(), 'Nest Rename.sh', 'Rename', NEST_GROUP)

    @updateMachine(TONCKA)
    def update6(self):
        pass
#        info("Configuring screen rotation shortcuts for Toncka.")
#        installBinScriptAbs(self.getMain(), [self.getMain().dirNastavitve(), 'Toncka', 'RotateScreen.sh'])
#        createLink([self.getMain().dirNastavitve(), 'Toncka', 'custom0'], getNextCustomDir(self.getMain()))
#        createLink([self.getMain().dirNastavitve(), 'Toncka', 'custom1'], getNextCustomDir(self.getMain()))
#        createLink([self.getMain().dirNastavitve(), 'Toncka', 'custom2'], getNextCustomDir(self.getMain()))
#        createLink([self.getMain().dirNastavitve(), 'Toncka', 'custom3'], getNextCustomDir(self.getMain()))

    def update7(self):
        createLink([self.getGiCfg('MY_GIT_CONFIG_DIR'), '.gitconfig'], self.getMain().dirHome(), UTILS_CREATE_LINK_DELETE)

    def update8(self):
        installBinScript(self.getMain(), 'npush')

    def update9(self):
        installBinScript(self.getMain(), 'callonemachineconffunc')

    def update10(self):
        installNautilusScript(self.getMain(), "Markdown.sh")

    ###
    ### Helper Functions
    ###

    def getLatexTemplates(self, template):
        return join(self.getMain().dirResearch(), "Various/Latex Playground", template)

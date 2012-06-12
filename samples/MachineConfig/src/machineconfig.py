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
from os.path import isdir
from os.path import join
from sys import argv

from homelib.config import *
from homelib.mymachines import *
from homelib.utils import *
from maco.nest import *
from maco.networking import *
from maco.pgsql import *
from maco.printing import *
from maco.selinux import *
from maco.users import *
from maco.utils import *
from mydev.referencer import *
from maco.services import *

# Parameters:
#
# noselinux

class MachineConfig(ConfigScript):
    def preRun(self):
        self.cloneUpdateEtcNest()
        self.macoSpecificStuff()

    def postRun(self):
        pass

    def postFail(self, ex):
        pass



    def update1(self):
        self.getMain().serviceSoftware().addRepository('http://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-stable.noarch.rpm')
        self.getMain().serviceSoftware().install(
                "mercurial",
                "yumex",
                "subversion",
                "libreoffice-calc",
                "libreoffice-base",
                "libreoffice-writer",
                "libreoffice-langpack-sl",
                "libreoffice-langpack-ja",
                "libreoffice-langpack-en",
                "libreoffice-langpack-de",
                "libreoffice-pdfimport",
#                "referencer", # Does not exist in F16 anymore
                "eclipse-texlipse",
                "meld",
                "powertop",
                "gimp",
                "nano",
                "xournal",
                "pidgin",
                "doxygen",
                "doxygen-doxywizard",
                "pidgin",
                "system-config-services",
                "zenity",
                "ffmpeg",
                "gstreamer-ffmpeg",
                "gstreamer-plugins-bad",
                "gstreamer-plugins-ugly",
                "mplayer",
                "vlc",
                "k3b",
                "k3b-extras-freeworld",
                "libmpg123",
                "sil-andika-fonts",
                "sil-charis-compact-fonts",
                "sil-charis-fonts",
                "sil-doulos-fonts",
                "sil-gentium-alt-fonts",
                "sil-gentium-basic-book-fonts",
                "sil-gentium-basic-fonts",
                "sil-gentium-basic-fonts-common",
                "sil-gentium-fonts",
                "sil-gentium-fonts-common",
                "sil-lateef-fonts",
                "sil-scheherazade-fonts",
                "tigervnc",
                'nautilus-open-terminal',
                'vim-enhanced',
                'java-1.6.0-openjdk-plugin',
                'libtool',
                'autoconf',
                'automake',
                'intltool',
                'gcc-c++',
                getReferencerDevelopmentDependencies()
            )

    @updateOnly('laptop')
    def update2(self):
        createLink([self.getGiCfg('MY_FEDORA_CONFIG_DIR'), 'laptop/etc/selinux/config'], '/etc/selinux')
        info("Disabled SELinux (restart required).")

    @updateOnly('maco_server')
    def update3(self):
        configurePgSql(self)
        setupNetworking(self)
        configureNest(self)
        setupPrinting(self)
        setupSsh(self)
        self.getMain().serviceSoftware().install(
                "dovecot",
                "postfix",
                "httpd",
                "mod_dav_svn",
                "mod_ssl",
                "bind",
                "java-1.6.0-openjdk",
                'java-1.6.0-openjdk-devel',
                'java-1.6.0-openjdk-src',
                'java-1.6.0-openjdk-javadoc',
                'java-1.6.0-openjdk-demo',
                'tigervnc-server',
                'php',
                'php-mysql',
                'mysql-server',
                'gnome-system-log',
                'system-config-bind',
                'cyrus-sasl',
                'cyrus-sasl-md5',
                'cyrus-sasl-plain',
                'selinux-policy-devel',
                'logwatch',
                'spamassassin',
                'amavisd-new'
            )
        warning("Installed MySQL. Please copy the old files from '/oldroot/var/lib/mysql' to '/'. Also, you have to enable the service manually.")
        setupBind(self)
        setupSvn(self)
        setupHttpd(self)
        installHomePage(self)
        setupPostfix(self)
        setupDovecot(self)
        createUsers(self)
        setupMacoPolicy(self)

    @updateOnly('laptop', 'cl_office')
    def update4(self):
        self.getMain().serviceSoftware().install(
                "emacs"
            )

    def update5(self):
        self.getMain().serviceSoftware().addRepository('http://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-stable.noarch.rpm')
        self.getMain().serviceSoftware().install(
                'inkscape',
                'python-lxml',
                'pdf2svg',
                'pstoedit',
                'easytag',
                'liveusb-creator',
                'calibre',
                'pgadmin3',
                'postgresql',
                'java-1.6.0-openjdk-javadoc',
                'gnubversion',
                'subversion-gnome',
                'kdesvn',
                'mysql-workbench',
                'libunrar',
                'unrar',
                'wget',
                'filezilla',
                'pidgin-otr'
            )

    # This update install software needed for building Isabelle.
    def update6(self):
#        self.getMain().serviceSoftware().install(
#                'polyml',
#                'scala',
#                'bison',
#                'flex',
#                'cvs',
#                'latexdiff',
#                'uniconvertor',
#                'pdfjam',
#                'git-gui',
#                'eclipse-jdt',
#                'eclipse-egit',
#                'gitk'
#            )
        pass

    # This update configures WebDAV (for the calendar): It also updates the
    # SELinux policies.
    @updateOnly('maco_server')
    def update7(self):
        setupWebDAVCalendar(self)

    # Installs Thunderbird. 
    def update8(self):
        self.getMain().serviceSoftware().install(
                "thunderbird",
                "thunderbird-enigmail",
                "thunderbird-lightning"
            )

    # Installs the weekly cron job for archiving the select Git repositories.
    @updateOnly('maco_server')
    def update9(self):
        setupGit(self)

    # Installs the daily cron job that backs up my calendars
    @updateOnly('maco_server')
    def update10(self):
        setupCalendarBackup(self)

    # Disables all the unnecessary services and enables some on all types of computers
    def update11(self):
        setupServices1Common(self)

    # Enables services needed by maco
    @updateOnly('maco_server')
    def update12(self):
        setupServices2Maco(self)

    # Disables all services not required for laptops
    @updateOnly('laptop')
    def update13(self):
        setupServices3Laptop(self)

    # Enables SSHD and assigns a static IP the home desktop computer (old maco).
    @updateOnly('home_desktop')
    def update14(self):
        setupDesktopNetworking(self)
        setupServices4Desktop(self)

    # Installs the mono-nat library for automatic configuration of port forwarding on the local router.
    # This failed. I did not manage to set the automatic port forwarding up.
    @updateOnly('maco_server')
    def update15(self):
        #self.getMain().serviceSoftware().install(
        #        'mono-nat'
        #    )
        pass



    ###
    ### Helper Functions
    ###

    def isMachineOfType(self, *types):
        return self.getMain().serviceMyMachines().isMachineOfType(types)

    def macoSpecificStuff(self):
        if not self.getMain().serviceMyMachines().isMachineOfType('maco_server'):
            return
        if not checkMaco():
            raise Exception("This machine identifies itself as a '" + 'maco_server' + "'. However, it does not satisfy the above conditions.")

    def cloneUpdateEtcNest(self):
        # Okay, we'll clone a copy of Nest into '/etc/Nest' -- to be able to
        # link to configuration files properly/directly.
        nestPath = '/etc/Nest'
        # @type nestService Nest
        nestService = self.getMain().serviceNest()
        if not isdir(nestPath) or not isdir(join(nestPath, '.hg')):
            nestService.cloneUri(nestService.getCentralRepoPath() if self.isMachineOfType('maco_server') else None, nestPath)
            info("Cloned 'Nest' to '" + nestPath + "'.")
        # Now set the Nest folder to the above cloned one.
        self.getMain().setDirNest(nestPath)
        # Update the Nest (if the user has not disabled it).
        if not ('--no-nest-pull' in argv):
            nestService.pullUpdate()
            info("Updated 'Nest' at '" + nestPath + "'.")

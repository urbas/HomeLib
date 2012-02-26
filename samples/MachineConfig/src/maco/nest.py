# coding=UTF-8
#
#   Project: HomeLib
# 
#       A library for configuration and management of a personal environment.
# 
# File name: nest.py
# 
#    Author: Matej Urbas [matej.urbas@gmail.com]
#   Created: 17-Oct-2010, 00:10:07
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

from homelib.utils import UTILS_CREATE_LINK_DELETE
from homelib.utils import UTILS_CREATE_LINK_HARD_LINK
from homelib.utils import createLink
from homelib.utils import mymakedirs
from homelib.utils import runCmd
from maco.paths import CRON_WEEKLY_DIR
from maco.paths import MERCURIAL_ETC_DIR
from maco.utils import restoreconR

NEST_RW_GROUP='nest_rw'

def configureNest(cfgScript):

    main = cfgScript.getMain()
    nest = main.serviceNest()
    repoPath = nest.getCentralRepoPath()

    info("Installing 'Mercurial'...")

    info("Creating the '" +  repoPath + "' repository...")

    mymakedirs(repoPath)

    runCmd('groupadd', NEST_RW_GROUP)
    info("Added the '" + NEST_RW_GROUP + "' group.")

    runCmd('usermod', '-a', '-G', NEST_RW_GROUP, 'matej')
    info("Added the user 'matej' to the '" + NEST_RW_GROUP + "' group.")

    runCmd('chown', '-R', 'root:root', repoPath)
    runCmd('setfacl', '-b', repoPath)
    runCmd('setfacl', '-R', '-m', 'd:u::rwx,d:g::rwx,d:o:0,d:m:rwx,m:rwx,d:u:apache:rx,d:g:apache:rx,d:u:root:rwx,d:g:root:rwx,d:g:' + NEST_RW_GROUP + ':rwx,u:apache:rx,g:apache:rx,g:' + NEST_RW_GROUP + ':rwx', repoPath)
    info("Configured Nest access rights.")

    createLink([ main.dirNastavitve(), 'Mercurial/Server Configuration/BackupHgRepos.sh' ], CRON_WEEKLY_DIR, UTILS_CREATE_LINK_HARD_LINK | UTILS_CREATE_LINK_DELETE, 0550, 'root', 'root')
    createLink([ main.dirNastavitve(), 'Mercurial/Server Configuration/hgrc' ], MERCURIAL_ETC_DIR, UTILS_CREATE_LINK_HARD_LINK, 0444, 'root', 'root')
    restoreconR(MERCURIAL_ETC_DIR)
    restoreconR(CRON_WEEKLY_DIR)
    info('Installed the global Mercurial configuration file and configured the repository backup creation script.')

# coding=UTF-8
#
#   Project: HomeLib
# 
#       A library for configuration and management of a personal environment.
# 
# File name: nesthg.py
# 
#    Author: Matej Urbas [matej.urbas@gmail.com]
#   Created: 26-Sep-2010, 14:18:33
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

from mercurial.hg import repository
from mercurial.ui import ui

from homelib.nest import Nest
from homelib.utils import runCmd
from homelib.utils import runCmdGetString



###
### The Mercurial implementation of the Nest service
###

class NestHg(Nest):
    """
    This is a Mercurial implementation of the Nest service.
    """
    def __init__(self, main=None):
        Nest.__init__(self, main)

    ###
    ### Nest Service Interface Implementation
    ###

    def run(self, *args):
        return runCmd("hg", "-v", "-R", self.getMain().dirNest(), args)

    def runGetString(self, *args):
        return runCmdGetString("hg", "-v", "-R", self.getMain().dirNest(), args)

    def clone(self, dest=None, user=None, proto=None):
        self.cloneUri(self.getFullUri(user, proto, dest), dest)

    def cloneUri(self, src, dest=None):
        runCmd("hg", "-v", "clone", src or self.getFullUri(), dest)

    def add(self, *files):
        self.run("add", files)

    def move(self, src, tar):
        self.run("mv", src, tar)

    def update(self):
        self.run("update")

    def pull(self):
        self.run("pull")

    def commit(self, message=None, *files):
        self.run("ci", "-m", message or " ", files)

    def push(self, message=None):
        self.run("push")

    def status(self):
        return repository(ui(), self.getMain().dirNest()).status(unknown=True)

    def diff(self):
        return self.runGetString("diff")[1]

    def log(self, *files):
        return self.runGetString("log", files)[1]

    def changes(self):
        return repository(ui(), self.getMain().dirNest()).status()[0:4]

    def untracked(self):
        return repository(ui(), self.getMain().dirNest()).status(unknown=True)[4]

    def revert(self, *files):
        self.run("revert", files or "--all")
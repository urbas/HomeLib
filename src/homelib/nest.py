# coding=UTF-8
#
#   Project: HomeLib
# 
#       A library for configuration and management of a personal environment.
# 
# File name: Nest.py
# 
#    Author: Matej Urbas [matej.urbas@gmail.com]
#   Created: 26-Sep-2010, 00:01:26
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
from os import remove
from os.path import join

from homelib.service import MultiService
from homelib.utils import askYesNo
from homelib.utils import printLines



###
### Configuration related stuff
###

"""
This value indicates which 'Nest Service' implementation should be used. This
service provides Versioning Control System management of the 'Nest' repository.

Currently known (supported) VCS implementations:

    hg      - Mercurial disctributed versioning control system.
"""
CFG_GINFO_VCS="nestService"

"""
The section in the HomeLib configuration file that the chosen 'Nest Service'
should use to get its configuration.
"""
CFG_GINFO_VCS_SECTION="nestServiceSection"

"""
The default username to use when connecting to the central repository.
"""
CFG_NEST_DEF_USER = "defUser"

"""
The default protocol to use when connecting to the central repository.
"""
CFG_NEST_DEF_PROTO = "defProto"

"""
The default root directory name to use when cloning the central repository
locally.
"""
CFG_NEST_DEF_CLONE_NAME = "defCloneName"

"""
The default URI that one can use when connecting to the central repository.
"""
CFG_NEST_DEF_FULL_REPO_URI = "defFullRepoUri"

"""
The path of the central repository on the server. This is not an URI, it is the
absolute filesystem path on the server.
"""
CFG_NEST_REPO_PATH = "repoPath"

"""
The port on which the server is listening for central repository connections.
"""
CFG_NEST_PORT = "port"

"""
The domain name of the server which serves the central repository.
"""
CFG_NEST_DOMAIN = "domain"

"""
The URI (without the username and the protocol) to the central repository.
"""
CFG_NEST_REPO_URI = "repoUri"



###
### The Nest Service class
###

class Nest(MultiService):
    """
    This is a base class of services that provide a way to work with the 'Nest'
    repository (regardless of the versioning control system currently in use).
    """
    def __init__(self, main=None):
        MultiService.__init__(self, main)



    ###
    ### Nest Service Interface (abstract methods)
    ###

    def run(self, * args):
        """
        This is a bit of an unsafe method, but it allows an invokation of the
        selected VCS application directly on the local repository (with the
        given arguments). Note that the implementation will make sure that the
        right repository is selected.

        @param  args    The arguments to the VCS application

        @returns    The exit code of the application.
        """
        raise NotImplementedError()

    def runGetString(self, * args):
        """
        This is a bit of an unsafe method, but it allows an invokation of the
        selected VCS application directly on the local repository (with the
        given arguments). Note that the implementation will make sure that the
        right repository is selected.

        @param  args    The arguments to the VCS application

        @returns    A pair-tuple, where the first element is the exit code of
                    the finished VCS process, and the second element are the
                    string contents of the application's output.
        """
        raise NotImplementedError()

    ##
    #Clones the 'Nest' repository from the configured central repository into
    #the given (or configured) local directory. Calling this method is (mostly)
    #equivalent to calling <tt>\ref cloneUri
    # "cloneUri('<proto>://central.repo:<user>//local/repo/path', <dest>)"</tt>.
    #
    #@param  dest    The directory where to put the cloned repository.
    #
    #@param  user    The user with which to connect to the central
    #                repository.
    #
    #@param  proto   The protocol with which to connect to the central
    #                repository.
    def clone(self, dest=None, user=None, proto=None):
        """
        Clones the 'Nest' repository from the configured central repository into
        the given (or configured) local directory. Calling this method is (mostly)
        equivalent to calling <tt>\ref cloneUri
         "cloneUri('<proto>://central.repo:<user>//local/repo/path', <dest>)"</tt>.

        @param  dest    The directory where to put the cloned repository.

        @param  user    The user with which to connect to the central
                        repository.

        @param  proto   The protocol with which to connect to the central
                        repository.
        """
        raise NotImplementedError

    ##
    #Clones the 'Nest' repository from the given URI.
    #
    #@param  src     <b>[Optional]</b> The URI to the source repository. If
    #                \c None, then the default central repository URI is taken.
    #
    #@param  dest    <b>[Optional]</b> The directory where to put the cloned
    #                repository.
    def cloneUri(self, src=None, dest=None):
        """
        Clones the 'Nest' repository from the given URI.

        @param  src     <b>[Optional]</b> The URI to the source repository. If
                        \c None, then the default central repository URI is taken.

        @param  dest    <b>[Optional]</b> The directory where to put the cloned
        """
        raise NotImplementedError

    def add(self, * files):
        """
        Adds the given files to the repository. If no files are provided, all
        untracked (non-ignored) files in the local 'Nest' repository are added.

        @param  *files  [Optional] The files to add to the repository.
        """
        raise NotImplementedError

    ##
    #Moves the \c src file to \c tar.
    #
    #@param src The file to move within the repository.
    #
    #@param tar The destination (the new name and path of the \c src file).
    def move(self, src, tar):
        """
        Moves the \c src file to \c tar.

        @param src The file to move within the repository.

        @param tar The destination (the new name and path of the \c src file).
        """
        raise NotImplementedError

    def revert(self, * files):
        """
        Reverts the given files in the local repository. If no files are
        provided, all changes are reverted.

        @param  *files  [Optional] The files to revert.
        """
        raise NotImplementedError

    def commit(self, message=None, *files):
        """
        Commits local changes.

        @param  message     [Optional] The message to use when committing.

        @param  *files      [Optional] The files to commit.
        """
        raise NotImplementedError

    def update(self):
        """
        Updates the local repository (merging any outstanding heads).
        """
        raise NotImplementedError

    def pull(self):
        """
        Pulls changes from the central repository to the local repository.
        """
        raise NotImplementedError

    def push(self, message=None):
        """
        Pushes local changes to the central repository.
        """
        raise NotImplementedError

    def status(self):
        """
        @returns    A tuple of lists of all changed and untracked files. Here
                    are the elements of the tuple:

                        0   - Modified files,

                        1   - Added,

                        2   - Removed,

                        3   - Deleted,

                        4   - Untracked
        """
        raise NotImplementedError

    def diff(self):
        """
        @returns    A unified diff string of all changes in the local
                    repository.
        """
        raise NotImplementedError

    def log(self, * files):
        """
        @param  files   [Optional] The files for which to return the history
                        log.

        @returns    A string containing the log of the given file (or the whole
                    repository, if no file was given).
        """
        raise NotImplementedError

    def changes(self):
        """
        @returns    A tuple of lists of all changed and tracked files. Here are
                    the elements of the tuple:

                        0   - Modified files,

                        1   - Added,

                        2   - Removed,

                        3   - Deleted
        """
        raise NotImplementedError

    def untracked(self):
        """
        @returns    A list of untracked non-ignored files. The paths to these
                    files are relative to the 'Nest' directory.
        """
        raise NotImplementedError



    ###
    ### Nest Service Interface (with full default implementation)
    ###

    def clean(self, interactive=False):
        """
        Removes all untracked non-ignored files from the local repository.

        @param  interactive Indicates whether the user should be asked before
                            removing any files.
        """
        ndir = self.getMain().dirNest()
        untracked = self.untracked()
        if untracked:
            if interactive:
                print "===================== Files to be removed ====================="
                printLines(untracked)
                print "==============================================================="
                if not askYesNo("Remove above files?"):
                    return
            for file in self.untracked():
                file = join(ndir, file)
                remove(file)
                info("Removed file '" + file + "'.")

    def commitPush(self, interactive=False, message=None, *files):
        """
        Commits local changes and pushes them to the central repository.

        @param  interactive [Optional] Indicates whether we should ask first,
                            before committing and pushing anything.

        @param  message     [Optional] The message to use when committing.

        @param  files       [Optional] Files to actually commit.
        """
        changes = self.changes()
        if changes:
            if interactive:
                print "========================= Changes ========================="
                if changes:
                    printChanges(changes)
                if files:
                    print "===================== Files to Commit ====================="
                    printLines(files)
                print "==========================================================="
                if not askYesNo("Commit and push above changes?"):
                    return
            if interactive:
                print ":: Committing ::"
            self.commit(message, files)
            if interactive:
                print ":: Pushing ::"
            self.push()

    def pullUpdate(self):
        """
        Pulls changes from the central repository and updates the local
        repository (trying to merge all changes).
        """
        self.pull()
        self.update()

    def revert2(self, interactive=False, * files):
        """
        Reverts changes to the given files in the repository. If no files are
        provided, all local changes are reverted.

        @param  interactive [Optional] Indicates whether we should ask first,
                            before reverting anything.

        @param  *files  [Optional] The files in the local repository to revert
                        their changes.
        """
        changes = None
        if not files:
            # Revert all changes, if any
            changes = self.changes()
            if not changes:
                return
        if interactive:
            print "========================== Files =========================="
            if changes:
                printChanges(changes)
            else:
                printLines(files)
            print "==========================================================="
            if not askYesNo("Revert above files?"):
                return
        self.revert(files)



    ###
    ### Configuration Access Methods
    ###

    def getCfg(self, key):
        """
        @returns    The value of the current VCS configuration for a specific
                    key.
        """
        return self.getMain().getCfg(self.getCfgSection(), key)

    def getDefUser(self):
        """
        @returns    The default username to use when connecting to the central
                    repository.
        """
        return self.getCfg(CFG_NEST_DEF_USER)

    def getDefProto(self):
        """
        @returns    The default protocol to use when connecting to the central
                    repository.
        """
        return self.getCfg(CFG_NEST_DEF_PROTO)

    def getDefCloneName(self):
        """
        @returns    The default root directory name to use when cloning the
                    central repository locally.
        """
        return self.getCfg(CFG_NEST_DEF_CLONE_NAME)

    def getDefFullRepoUri(self):
        """
        @returns    The default URI that one can use when connecting to the
                    central repository.
        """
        return self.getCfg(CFG_NEST_DEF_FULL_REPO_URI)

    def getCentralRepoPath(self):
        """
        @returns    The path of the central repository on the server. This is
                    not an URI, it is the absolute filesystem path on the
                    server.
        """
        return self.getCfg(CFG_NEST_REPO_PATH)

    def getCentralRepoPort(self):
        """
        @returns    The port on which the server is listening for central
                    repository connections.
        """
        return self.getCfg(CFG_NEST_PORT)

    def getCentralRepoDomain(self):
        """
        @returns    The domain name of the server which serves the central
                    repository.
        """
        return self.getCfg(CFG_NEST_DOMAIN)

    def getCentralRepoUri(self):
        """
        @returns    The URI (without the username and the protocol) to the
                    central repository.
        """
        return self.getCfg(CFG_NEST_REPO_URI)

    def getFullUri(self, user=None, proto=None):
        """
        @returns    An URI containing all needed information to connect and work
                    with the central repository.

        @param  user    [Optional] If given, this user is used to connect to the
                        central repository. Otherwise the default user is used.
                        The default user is given in the configuration file,
                        with the key 'defUser' in the section of the currently
                        active VCS. If no default user is specified in the
                        configuration file, the currently logged-in user is
                        used.

        @param  proto   [Optional] The protocol to use to connect to the central
                        repository. If not given, the default one (as configured
                        in the configuration file with the key 'defProto') is
                        used. If not given in the configuration file, an
                        exception will be thrown.
        """
        defUser = user or self.getDefUser()
        defProto = proto or self.getDefProto()
        return (
                (defProto + "://" if defProto else "") +
                (defUser + "@" if defUser else "") +
                self.getCentralRepoUri()
                )

    @classmethod
    def knownImpls(cls):
        return {
            "hg": ("nesthg", "NestHg")
        }

    @classmethod
    def getChosenImplCfgKey(cls):
        return CFG_GINFO_VCS

    @classmethod
    def getChosenImplCfgSection(cls):
        return CFG_GINFO_VCS_SECTION



###
### Pretty Print Functions
###

def printChanges(changes):
    """
    Prints out changes (as returned by the 'Nest.changes' method).
    """
    printLines(map(lambda a: "M " + a, changes[0]))
    printLines(map(lambda a: "A " + a, changes[1]))
    printLines(map(lambda a: "R " + a, changes[2]))
    printLines(map(lambda a: "! " + a, changes[3]))

def printStatus(status):
    """
    Prints out the repository status (as returned by the 'Nest.status' method).
    """
    printChanges(status)
    printLines(map(lambda a: "? " + a, status[4]))
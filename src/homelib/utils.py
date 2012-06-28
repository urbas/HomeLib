# coding=UTF-8
#
#   Project: HomeLib
#
#        A library for configuration and management of a personal environment.
#
# File name: utils.py
#
#    Author: Matej Urbas [matej.urbas@gmail.com]
#   Created: 25-Sep-2010, 12:42:22
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

import logging
import os
import subprocess
import sys
from inspect import isclass
from logging import Formatter
from logging import StreamHandler
from logging import info
from logging import warn
from os import chmod
from os import chown
from os import close
from os import getenv
from os import geteuid
from os import link
from os import makedirs
from os import remove
from os import rmdir
from os import symlink
from os import walk
from os.path import abspath
from os.path import basename
from os.path import dirname
from os.path import exists
from os.path import isdir
from os.path import join
from os.path import lexists
from os.path import relpath
from os.path import samefile
from os.path import split
from shutil import copy2
from shutil import move
from subprocess import PIPE
from subprocess import Popen
from tempfile import mkdtemp
from tempfile import mkstemp
from time import strftime



###
### Important Constants
###

"""
These tell the 'link creation method' what type of action to perform.
"""
UTILS_CREATE_LINK_DELETE=1
UTILS_CREATE_LINK_HARD_LINK=2
UTILS_CREATE_LINK_COPY=4
UTILS_CREATE_LINK_MOVE=8
UTILS_CREATE_LINK_ABS=16
UTILS_CREATE_LINK_MAKE_TARGET_DIRS=32



###
### Environment Setup Utilities
###

"""
The name of the environment variable which (potentially) contains the absolute
path to a home folder.
"""
ENV_VAR_HOME_ABS_PATH = "MY_HOME_ABS_PATH"

def getHomePath():
    """
    @returns    The configured path to home folder (as given in the
                'MY_HOME_ABS_PATH' or 'HOME' environment variables).
    """
    return getenv(ENV_VAR_HOME_ABS_PATH, getenv("HOME"))



###
### User Management Utilities
###

def checkIfRoot():
    """
    @returns    \code>True\endcode iff the user executing this script has root
                privileges.
    """
    return geteuid() == 0



###
### General Python Data Structure Utilities
###

def flatten(*args):
    """
    Creates a flattened tuple/list from the given argument list.

    @param  args    A list of arguments.
    """
    ltype = type(args)
    args = list(args)
    i = 0
    while i < len(args):
        while isinstance(args[i], (list, tuple)):
            if not args[i]:
                args.pop(i)
                i -= 1
                break
            else:
                args[i:i + 1] = args[i]
        i += 1
    return ltype(args)

def invokeForEach(fun, elmnts, startIdx = 0):
    """
    This method calls the function 'fun' for every element in the list 'elmnts'.
    If an element of the 'elmnts' list is itself a list or a tuple, then this
    method recurses into it and does the same on its elements.

    @param  fun The function to call for each element. This function will be
                called with two parameters: the current element and its index.

    @param  elmnts  A list or tuple to traverse and call the function 'fun' for
                    each of its elements.

    @param  startIdx    [Optional] The index with which to start counting
                        elements.

    @returns    The number of times the function 'fun' was called.
    """
    i = 0
    while i < len(elmnts):
        if isinstance(elmnts[i], (list, tuple)):
            startIdx = invokeForEach(fun, elmnts[i], startIdx)
        else:
            fun(elmnts[i], startIdx)
            startIdx += 1
        i += 1
    return startIdx

def getClassFQName(cls):
    """
    @param  cls The class for which to get the fully qualified name.

    @returns    The fully qualified name of the given class (or 'None' if 'cls'
                is not a class at all.
    """
    if isclass(cls):
        return cls.__module__ + "." + cls.__name__
    return None



###
### File System Utilities
###

def appendLinesToFile(filePath, *lines):
    """
    @param  filePath    The path to the file to append the given lines to.

    @param  lines   A list of strings to write to the file.

    @returns    The number of lines printed.
    """
    fd = open(joinPaths(filePath), 'a')
    count = invokeForEach(lambda s, i: fd.write(s.__str__()) or fd.write('\n'), lines)
    fd.close()
    return count

def shredRemoveFiles(*fileNames):
    """
    Shreds and removes the given files.
    """
    if fileNames:
        runCmd('shred', '-uz', fileNames)
        info("Shredded '" + fileNames + "'.")

def decryptFile(src, target):
    src = joinPaths(src)
    target = joinPaths(target)
    if not exists(src):
        raise IOError("The file '" + src + "' is not an existing file.")
    runCmd('gpg2', '--output', target, '-d', src)

##
#    Moves the given file or directory to a new path in the same directory (or
#    the given one) using a new unique name.
#
#    @param  fileName    The name of the file/directory to move to a backup name.
#
#    @param  tarDir      <b>[OPTIONAL]</b> The directory where to place the
#                        backup.
#
#    @returns            The name of the newly created backup.
def makeBackup(fileName, tarDir = None):
    """
    Moves the given file or directory to a new path in the same directory (or
    the given one) using a new unique name.

    @param  fileName    The name of the file/directory to move to a backup name.

    @param  tarDir      <b>[OPTIONAL]</b> The directory where to place the
                        backup.

    @returns            The name of the newly created backup.
    """
    if isdir(fileName):
        (dirPath, name) = split(fileName)
        backupName = createTmpDir(name, tarDir or dirPath)
        rmdir(backupName)
        move(fileName, backupName)
        info("Backed up directory '" + fileName + "' as '" + backupName + "'.")
        return backupName
    elif lexists(fileName):
        (dirPath, name) = split(fileName)
        (fd, backupName) = createTmpFile(name + '.backup', tarDir or dirPath)
        close(fd)
        move(fileName, backupName)
        info("Backed up file '" + fileName + "' as '" + backupName + "'.")
        return backupName
    else:
        raise IOError('The given path does not exist.')

##
#Creates a link, copies or moves the source file to the target.
#
#@param  srcFile The path to the source file (the file to which we link). If
#                this argument is a list or a tuple, the elements will be
#                joined to produce the final file path.
#
#@param  tarPath [Optional] The path where to place the link. If not given,
#                the current directory is used. If this argument is a list or
#                a tuple, the elements will be joined to produce the final
#                target path.
#
#@param  options <b>[Optional]</b> A binary combination of the following:
#
#      1   - Deletes (instead of backing up) any existing files that clash
#            with the link name. Use variable: \ref UTILS_CREATE_LINK_DELETE.
#
#      2   - Creates a hard link rather than a symbolic one.
#            Use variable: \ref UTILS_CREATE_LINK_HARD_LINK.
#
#      4   - Creates a copy rather than a link (cannot be used with '2').
#            Use variable: \ref UTILS_CREATE_LINK_COPY.
#
#      8   - Creates a copy rather than a link (cannot be used with '2' or
#            '4').
#            Use variable: \ref UTILS_CREATE_LINK_MOVE.
#
#      16  - Use an absolute path to the target rather than a relative one
#            when creating a symbolic link.
#            Use variable: \ref UTILS_CREATE_LINK_ABS.
#
#      32  - Create the target directory (if it doesn't exists).
#            Variable: \ref UTILS_CREATE_LINK_MAKE_TARGET_DIRS.
#
#@param  mode    <b>[Optional]</b> The permissions mode with which to create
#                the link (only works on hard links and copies).
#
#@param  owner   <b>[Optional]</b> The owner of the link (only works on hard
#                links and copies).
#
#@param  group   <b>[Optional]</b> The group of the link (only works on hard
#                links and copies).
def createLink(srcFile, tarPath=".", options=0, mode=None, owner=None, group=None):
    """
    Creates a link, copies or moves the source file to the target.

    @param  srcFile The path to the source file (the file to which we link). If
                    this argument is a list or a tuple, the elements will be
                    joined to produce the final file path.

    @param  tarPath [Optional] The path where to place the link. If not given,
                    the current directory is used. If this argument is a list or
                    a tuple, the elements will be joined to produce the final
                    target path.

    @param  options <b>[Optional]</b> A binary combination of the following:

          1   - Deletes (instead of backing up) any existing files that clash
                with the link name. Use variable: \ref UTILS_CREATE_LINK_DELETE.

          2   - Creates a hard link rather than a symbolic one.
                Use variable: \ref UTILS_CREATE_LINK_HARD_LINK.

          4   - Creates a copy rather than a link (cannot be used with '2').
                Use variable: \ref UTILS_CREATE_LINK_COPY.

          8   - Creates a copy rather than a link (cannot be used with '2' or
                '4').
                Use variable: \ref UTILS_CREATE_LINK_MOVE.

          16  - Use an absolute path to the target rather than a relative one
                when creating a symbolic link.
                Use variable: \ref UTILS_CREATE_LINK_ABS

          32  - Create the target directory (if it doesn't exists).
                Variable: \ref UTILS_CREATE_LINK_MAKE_TARGET_DIRS.

    @param  mode    <b>[Optional]</b> The permissions mode with which to create
                    the link (only works on hard links and copies).

    @param  owner   <b>[Optional]</b> The owner of the link (only works on hard
                    links and copies).

    @param  group   <b>[Optional]</b> The group of the link (only works on hard
                    links and copies).
    """
    linkPath = None

    srcFile = joinPaths(srcFile)
    
    if not exists(srcFile):
        raise IOError("The source file '" + srcFile + "' does not exist.")
    
    if not tarPath:
        raise Exception("A valid target path must be specified.")

    tarPath = joinPaths(tarPath)
    if isdir(tarPath):
        linkPath = join(tarPath, basename(srcFile))
    else:
        linkPath = tarPath

    # Now we have the path of the link. Check that it does not clash with an
    # existing file.
    options = options or 0
    if lexists(linkPath):
        # Okay, the link path clashes with an existing file. Depending on
        # the options delete or backup the clashing file:
        if options & UTILS_CREATE_LINK_DELETE:
            remove(linkPath)
            info("Removed file '" + linkPath + "'.")
        else:
            makeBackup(linkPath)
    elif options & UTILS_CREATE_LINK_MAKE_TARGET_DIRS:
        # The target path does not exist and the user wants us to create any
        # non-existing target directories. Well, make it so.
        try:
            makedirs(dirname(linkPath))
        except:
            pass

    # Done, now either create a link or a copy:
    srcFile = abspath(srcFile)
    if options & UTILS_CREATE_LINK_HARD_LINK:
        # Create a hard link
        link(srcFile, linkPath)
        info("Hardlinked: '" + linkPath + "' ==> '" + srcFile + "'.")
    elif options & UTILS_CREATE_LINK_COPY:
        # Create a copy
        copy2(srcFile, linkPath)
        info("Copied file '" + srcFile + "' to '" + linkPath + "'.")
    elif options & UTILS_CREATE_LINK_MOVE:
        # Simply move the file
        move(srcFile, linkPath)
        info("Moved file '" + srcFile + "' to '" + linkPath + "'.")
    else:
        # Create a symbolic link
        if not (options & UTILS_CREATE_LINK_ABS):
            # Calculate the relative path to the target
            srcFile = relpath(srcFile, dirname(linkPath))
        symlink(srcFile, linkPath)
        info("Symlinked: '" + linkPath + "' --> '" + srcFile + "'.")
    chprops(linkPath, mode, owner, group)

##
#Makes all parent subdirectories for the given path.
#
#@param path    A list of directory names in the directory structure that should
#               be made. Note that these names are first joined (via
#               \ref joinPaths).
def mymakedirs(*path):
    """
    Makes all parent subdirectories for the given path.

    @param path    A list of directory names in the directory structure that should
                   be made. Note that these names are first joined (via
                   \ref joinPaths).
    """
    try:
        makedirs(joinPaths(path))
    except:
        pass

##
#Changes the most common attributes of a file.
#
#@param   file    The file for which to update the attributes.
#
#@param   mode    <b>[Optional]</b> The new permissions.
#
#@param   owner   <b>[Optional]</b> The new owner.
#
#@param   group   <b>[Optional]</b> The new group.
def chprops(filePath, mode=None, owner=None, group=None):
    """
    Changes the most common attributes of a file.

    @param   filePath    The file for which to update the attributes.

    @param   mode    <b>[Optional]</b> The new permissions.

    @param   owner   <b>[Optional]</b> The new owner.

    @param   group   <b>[Optional]</b> The new group.
    """
    if mode or owner or group:
        if not exists(filePath):
            raise IOError("The path '" + filePath + "' does not exist.")

        if isinstance(owner, str):
            runCmd('chown', owner, filePath)
        elif isinstance(owner, int):
            chown(filePath, owner, -1)

        if isinstance(group, str):
            runCmd('chgrp', group, filePath)
        elif isinstance(group, int):
            chown(filePath, -1, group)

        mode = int(mode)
        if mode:
            chmod(filePath, mode)

        info("Changed the attributes of '" + filePath + "'." +
                ((' Mode: {0:o}'.format(mode)) if mode else '') +
                ((" Owner: " + owner.__str__()) if owner else '') +
                ((" Group: " + group.__str__()) if group else '')
            )

##
#   This method links to files within the source directory from the target
#   directory. However, this method does not produce links to files within the
#   target directory, but produces a link to the whole source directory tree and
#   copies any files (that might have been) in the target directory to the
#   source directory tree.
#
#   Example:
#
#   If you invoke this function like this:
#
#   \code
#   linkDirTree("/foo/bar/A", "/moo")
#   \endcode
#
#   And say that the above directories contain the following:
#
#   \code
#   /foo/bar/A/file1
#   /foo/bar/A/subdir/file2
#
#   /moo/file1
#   /moo/A/file1
#   /moo/A/file2
#   /moo/A/dir1
#   /moo/A/subdir/file1
#   /moo/A/subdir/file2
#   \endcode
#
#   You will get something like this:
#
#   \code
#   /moo/A          ->  /foo/bar/A
#
#   /foo/bar/A/file1
#   /foo/bar/A/subdir/file2
#   /moo/file1
#   /foo/bar/A/file1.backup
#   /foo/bar/A/file2
#   /foo/bar/A/dir1
#   /foo/bar/A/subdir/file1
#   /foo/bar/A/subdir/file2.backup
#   \endcode
#
#   @param  srcDir  The source directory (containing the files to which we will
#                   link).
#
#   @param  tarDir  The directory where to place the folder, its links to files,
#                   and the corresponding sub-directory structure. If this
#                   directory does not exist it will be created.
#
def linkDirTree(srcDir, tarDir):
    """
   This method links to files within the source directory from the target
   directory. However, this method does not produce links to files within the
   target directory, but produces a link to the whole source directory tree and
   copies any files (that might have been) in the target directory to the
   source directory tree.

   Example:

   If you invoke this function like this:

   \code
   linkDirTree("/foo/bar/A", "/moo")
   \endcode

   And say that the above directories contain the following:

   \code
   /foo/bar/A/file1
   /foo/bar/A/subdir/file2

   /moo/file1
   /moo/A/file1
   /moo/A/file2
   /moo/A/dir1
   /moo/A/subdir/file1
   /moo/A/subdir/file2
   \endcode

   You will get something like this:

   \code
   /moo/A          ->  /foo/bar/A

   /foo/bar/A/file1
   /foo/bar/A/subdir/file2
   /moo/file1
   /foo/bar/A/file1.backup
   /foo/bar/A/file2
   /foo/bar/A/dir1
   /foo/bar/A/subdir/file1
   /foo/bar/A/subdir/file2.backup
   \endcode

   @param  srcDir  The source directory (containing the files to which we will
                   link).

   @param  tarDir  The directory where to place the folder, its links to files,
                   and the corresponding sub-directory structure. If this
                   directory does not exist it will be created.
    """
    srcDir = joinPaths(srcDir)
    tarDir = joinPaths(tarDir)
    if isdir(srcDir):
        # The target directory must be created if it does not exist yet.
        if not isdir(tarDir):
            makedirs(tarDir)
            info("Created folder '" + tarDir + "'.")
        basedir = basename(srcDir)
        # Everything okay. Now, if the target directory contains a sub-dir
        # with the same name as the srcDir, then make a backup of it:
        tarPath = join(tarDir, basedir)
        if exists(tarPath) and samefile(srcDir, tarPath):
            info("Did not link '"+ srcDir +"' into itself.")
            return
        backupDir = makeBackup(tarPath) if isdir(tarPath) else None
        # Now create the link and copy all the files in the old directory to
        # the symlinked one.
        createLink(srcDir, tarPath)
        if backupDir:
            for root, _, files in walk(backupDir):
                for filePath in files:
                    fullFilePath = join(root, filePath)
                    destFilePath = join(srcDir, relpath(fullFilePath, backupDir))
                    if exists(destFilePath):
                        makeBackup(fullFilePath, dirname(destFilePath))
                    else:
                        try:
                            makedirs(dirname(destFilePath))
                        except:
                            pass
                        move(fullFilePath, destFilePath)
    else:
        warn("The source directory '" + srcDir + "' does not exist.")

def getHomeLibFile(filePath):
    """
    Returns the absolute path to the file of which we know only its relative
    path (relative to the location of this library).

    @param  filePath    The path of the file relative to this library.
    """
    return abspath(join(dirname(__file__), filePath))

def linkInSubfolders(theFile, linkName, options, *dirs):
    """
    Creates subfolders (if they do not already exist, one within the other) and
    places the link in bottom-most subfolder.

    @param  theFile The file to which we want to link.

    @param  linkName    The name of the link (which will be placed in the final
                        directory -- as composited via the 'dirs' parameter).
                        Can be 'None', in which case the name of the original
                        file will be used as the link name.

    @param  options A binary combination of the following (or None):

           1   - Deletes (instead of backing up) any existing files that clash
                 with the link name.

           2   - Creates a hard link rather than a symbolic one.

           4   - Creates a copy rather than a link (cannot be used with '2').

    @param  dirs    A list of directories (which will be joined together, to
                    form the final directory into which to place the link).
    """
    theFile = joinPaths(theFile)
    if not theFile:
        raise Exception("A valid file name has to be specified.")
    if not exists(theFile):
        raise Exception("The file '" + theFile + "' does not exist.")
    if not dirs:
        raise Exception("No subfolders given.")
    dirPath = joinPaths(dirs)
    try:
        makedirs(dirPath)
    except:
        pass
    if not isdir(dirPath):
        raise Exception("Could not create folder '" + dirPath + "'.")
    createLink(theFile, join(dirPath, linkName or basename(theFile)), options)

def joinPaths(paths):
    """
    This method flattens the list given in 'paths' and joins all the elements
    of the resulting list via 'reduce' and the 'os.path.join' functions.

    @param  paths   A list of paths, directory names that should be joined into
                    one.

    @return A path consisting of all the elements in 'paths'.
    """
    if isinstance(paths, (list, tuple)):
        i = 0
        baseDir = ""
        while i < len(paths):
            baseDir = join(baseDir, joinPaths(paths[i]))
            i += 1
        return baseDir
    return paths

def createTmpFile(prefix='.tmp', dirPath='/tmp'):
    """
    This function creates a new empty file in the '/tmp' folder or the folder
    provided in 'folder'.

    The resulting file will have the following path (depending on the number of
    arguments given to this function):

        <dirPath>/<prefix>.%Y-%m-%d_%H:%M:%S.XXXXXXX

    @param  prefix  [Optional] The string to prepend to the name of the
                    temporary file.

                    If no prefix is given '.tmp' is used.

    @param  dirPath     [Optional] The folder where to create the file.

                    If no folder is given '/tmp' is used.

    @returns        A pair (fd, name), where fd is the file handle as returned
                    by the 'os.open' method and name is the name of the newly
                    created file.

    @throws         An exception if the file creation failed for any reason.
    """
    if not isdir(dirPath):
        raise IOError('The given folder does not exist')
    return mkstemp('', prefix + '.' + strftime('%Y-%m-%d_%H:%M:%S') + '.', dirPath)

def createTmpDir(prefix='.tmp', dirPath='/tmp'):
    """
    This function creates a new empty file in the '/tmp' folder or the folder
    provided in 'folder'.

    The resulting file will have the following path (depending on the number of
    arguments given to this function):

        <dirPath>/<prefix>.%Y-%m-%d_%H:%M:%S.XXXXXXX

    @param  prefix  [Optional] The string to prepend to the name of the
                    temporary file.

                    If no prefix is given '.tmp' is used.

    @param  dirPath     [Optional] The folder where to create the file.

                    If no folder is given '/tmp' is used.

    @returns        A pair (fd, name), where fd is the file handle as returned
                    by the 'os.open' method and name is the name of the newly
                    created file.

    @throws         An exception if the file creation failed for any reason.
    """
    if not isdir(dirPath):
        raise IOError('The given folder does not exist')
    return mkdtemp('', prefix + '.' + strftime('%Y-%m-%d_%H:%M:%S') + '.', dirPath)

def openOrCreateWithDir(filePath, mode = 'w'):
    """
    Tries to open the given file. This function also creates the whole directory
    structure of the given file if it doesn't exist.

    @param  filePath    The file to open.
    
    @param  mode    [Optional] The mode with which to open the file. Default is
                    'w' -- write mode.

    @returns    The file descriptor (as returned by the 'open' function).
    """
    try:
        makedirs(dirname(filePath))
    except:
        pass
    return open(filePath, mode)



###
### Command Invokation Utilities
###

def runCmd(filePath, * args):
    """
    Executes the command with the given arguments and returns the returncode
    of the process. This method blocks until the application finishes.

    @param  filePath    The file to execute (the program).

    @param  args    A list of arguments to the program.

    @returns    The return code of the started process.
    """
    return subprocess.call(flatten(joinPaths(filePath), args))

def runCmdGetString(filePath, * args):
    """
    Executes the command with the given arguments and returns the output of the
    command as a string. This method blocks until the application finishes.

    @param  filePath    The file to execute (the program).

    @param  args    A list of arguments to the program.

    @returns    A pair-tuple, where the first element is the return code of the
                finished process and the second element the string contents of
                the application's output.
    """
    proc = Popen(flatten(joinPaths(filePath), args), stdout=PIPE);
    cont = proc.stdout.read()
    retcode = proc.wait()
    return (retcode, cont)

def runCmdGetLines(filePath, * args):
    """
    Executes the command with the given arguments and returns the output of the
    command as a list of line strings. This method blocks until the application
    finishes.

    @param  filePath    The file to execute (the program).

    @param  args    A list of arguments to the program.

    @returns    A pair-tuple, where the first element is the return code of the
                finished process and the second element the list of string lines
                which form the contents of the application's output.
    """
    proc = Popen(flatten(joinPaths(filePath), args), stdout=PIPE);
    (stdoutdata,_) = proc.communicate()
    retcode = proc.wait()
    return (retcode,[] if stdoutdata is None else stdoutdata.splitlines())


###
### Dynamic Code Loading Utilities
###

def loadClass(moduleName, className=None, path=None):
    """
    Loads a class in the given module and returns a reference to the type.

    Note: This method is not thread-safe.

    @param  moduleName  The name of the module that contains the class to load.

    @param  className   [Optional] The member in the given module to load. If
                        omitted, the class with the same name as the module will
                        be loaded.

    @param  path        [Optional] The path where to search for the module.

    @returns    A reference to the loaded type of the class or a reference to
                the member of the given module.

    @throws     An exception if the loading failed for any reason.
    """
    if path:
        if not isdir(path):
            raise Exception("The given directory '" + path + "' does not exist.")
        sys.path.insert(0, path)

    memberName = className or moduleName
    someStuff = __import__(moduleName, globals(), locals(), [memberName], -1)
    if not someStuff:
        raise Exception("The module '" + moduleName + "' could not be loaded.")

    if path:
        sys.path.pop(0)

    retVal = getattr(someStuff, memberName)
    if not retVal:
        raise Exception("The name '" + memberName + "' in '" + moduleName + "' could not be loaded.")
    return retVal



###
### Command Line User Interface Utilities
###

def askYesNo(msg):
    """
    Asks the user a question given in $1 and returns 0 if the user replied with
    'y', otherwise it returns 1.

    @param  msg     The question to display (without the trailing '[y/N]').

    @returns        0 if the user replied with 'y', otherwise it returns 1.
    """
    return raw_input(msg + " [y/N]: ") == "y"

def printLines(*lines):
    """
    Prints each element of the 'lines' argument in its own line.

    @param  lines   The list of elements to print each in their own line.
    """
    for line in flatten(lines):
        print line



###
### Configuration Utilities
###

def cfgGetOrDefault(configParser, section, key, default = None, variables = None):
    """
    @param  configParser    The configuration parser from which to fetch the
                            value of the option with the given key and in the
                            given section.

    @param  section The section in the configuration file where to search
                    for the option with the given name.

    @param  key     The name of the option we want the value of.

    @param  default The value to return in case the key has not been found.

    @param  variables    The interpolation variables to use when fetching the value
                    of the option from the configuration parser.

    @returns    The configuration value from the configuration file (or default
                if the option with the given key does not exist).
    """
    try:
        return configParser.get(section, key, False, variables)
    except:
        return default

def cfgGetIntOrDefault(configParser, section, key, default = None, variables = None):
    """
    @param  configParser    The configuration parser from which to fetch the
                            value of the option with the given key and in the
                            given section.

    @param  section The section in the configuration file where to search
                    for the option with the given name.

    @param  key     The name of the option we want the value of.

    @param  default The value to return in case the key has not been found.

    @param  variables    The interpolation variables to use when fetching the value
                    of the option from the configuration parser.

    @returns    The configuration value (as an integer) from the configuration
                file (or default if the option with the given key does not
                exist).
    """
    try:
        return int(configParser.get(section, key, False, variables))
    except:
        return default

def cfgSet(configParser, section, key, value):
    """
    @param  configParser    The configuration parser to which to write the
                            value of the option with the given key and in the
                            given section.

    @param  section The section in the configuration file where to search
                    for the option with the given name.

    @param  key     The name of the option we want to set the value of.

    @param  value   The value to store for the given option. This value can be
                    of any type that properly supports '__str__'.
    """
    try:
        configParser.add_section(section)
    except:
        pass
    configParser.set(section, key, value.__str__())



###
### Logging Utilities
###

DEFAULT_LOGGING_FORMAT="[%(levelname)s | %(asctime)s] :: %(message)s"
DEFAULT_LOGGING_DATE_FORMAT="%Y-%m-%d %H:%M:%S"

# Setup error and information logging.
logging.basicConfig(
                    level=logging.DEBUG,
                    stream=sys.__stdout__,
                    format=DEFAULT_LOGGING_FORMAT,
                    datefmt=DEFAULT_LOGGING_DATE_FORMAT
                   )

def getClassLogger(cls, baseDir=None, level=logging.DEBUG, msgFormat=DEFAULT_LOGGING_FORMAT, dateFormat=DEFAULT_LOGGING_DATE_FORMAT):
    """
    This method creates a logger that appends log messages to a file. The name
    of the file is constructed via the class' name and is placed either in the
    current working directory, or the given directory.

    @param  cls     The class for which to create the logger.

    @param  baseDir [Optional] The directory where to put/find the log file.
                    If not given, the current working directory is used.

    @param  level   [Optional] The level of messages to log (default is
                    'DEBUG').

    @param  msgFormat  [Optional] The message format to use for logging.

    @param  dateFormat  [Optional] The date format to use for logging.

    @returns    A Logger, which has an additional attribute:

                    myclose - A parameterless function, which closes the file
                              handler for the logger.
    """
    clsName = getClassFQName(cls)
    if not clsName:
        raise Exception("Could not determine the fully qualified name of the given class.")
    logFilePath = join(baseDir or os.getcwd(), clsName) + ".log"

    logger = logging.getLogger(clsName)
    logger.setLevel(level)
    
    fd = openOrCreateWithDir(logFilePath, 'a')
    lh = StreamHandler(fd)
    lh.setFormatter(Formatter(msgFormat, dateFormat))
    logger.addHandler(lh)
    
    def myclose():
        logger.removeHandler(lh)
        lh.close()
        fd.close()
    logger.myclose = myclose
    
    return logger

def addLoggerHandler(cls, baseDir=None, level=logging.DEBUG, msgFormat=DEFAULT_LOGGING_FORMAT, dateFormat=DEFAULT_LOGGING_DATE_FORMAT):
    """
    This method adds to the global logger a handler that appends log messages to
    a file. The name of the file is constructed via the class' name and is
    placed either in the current working directory, or the given directory.

    @param  cls     The class for which to add a log listener.

    @param  baseDir [Optional] The directory where to put/find the log file.
                    If not given, the current working directory is used.

    @param  level   [Optional] The level of messages to log (default is
                    'DEBUG').

    @param  msgFormat  [Optional] The message format to use for logging.

    @param  dateFormat  [Optional] The date format to use for logging.

    @returns    A pair, the elements being:

                    0   - The StreamHandler.

                    1   - The file descriptor.
    """
    clsName = getClassFQName(cls)
    if not clsName:
        raise Exception("Could not determine the fully qualified name of the given class.")
    logFilePath = join(baseDir or os.getcwd(), clsName) + ".log"

    logger = logging.getLogger()

    fd = openOrCreateWithDir(logFilePath, 'a')
    lh = StreamHandler(fd)
    lh.setFormatter(Formatter(msgFormat, dateFormat))
    lh.setLevel(level)
    logger.addHandler(lh)

    return (lh, fd)

def removeLoggerHandler(lh, fd = None):
    """
    Removes the given log handler from the 'root' logger and closes it. This
    method also tries to close the associated file.
    """
    logger = logging.getLogger()
    logger.removeHandler(lh)
    lh.close()
    if fd:
        fd.close()

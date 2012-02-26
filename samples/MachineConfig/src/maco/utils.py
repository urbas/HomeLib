# coding=UTF-8
#
#   Project: HomeLib
# 
#       A library for configuration and management of a personal environment.
# 
# File name: utils.py
# 
#    Author: Matej Urbas [matej.urbas@gmail.com]
#   Created: 09-Oct-2010, 12:33:49
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
from os.path import basename
from os.path import exists
from os.path import isdir
from os.path import join

from homelib.utils import UTILS_CREATE_LINK_DELETE
from homelib.utils import UTILS_CREATE_LINK_HARD_LINK
from homelib.utils import createLink
from homelib.utils import flatten
from homelib.utils import joinPaths
from homelib.utils import runCmd
from maco.paths import CERTS_DIR
from maco.paths import KEYS_DIR
from maco.paths import dirCertifikati
from maco.paths import dirCertifikatiUrbasSi



MACO_DIR='/maco'
MACO_STUFF_DIR='/stuff'
MACO_BACKUPS_DIR=join(MACO_STUFF_DIR, 'Backup')



def checkMaco():
    """
    Checks this computer if it satisfies all the conditions of being the 'Maco
    Server'. It must, for example, have certain folders.

    @returns    'True' iff this computer satisfies all 'Maco Server' conditions.
    """
    if not isdir(MACO_DIR):
        warning("The 'Maco' directory (that contains the central 'Nest' repository amongst other things) does not exist. You should create the folder: " + MACO_DIR)
        return False
    if not isdir(MACO_STUFF_DIR):
        warning("The 'Stuff' directory does not exist. You should create the folder: " + MACO_STUFF_DIR)
        return False
    if not isdir(MACO_BACKUPS_DIR):
        warning("The 'Backups' directory does not exist. You should create the folder: " + MACO_BACKUPS_DIR)
        return False
    return True

def restorecon(*paths):
    """
    Restores the SELinux contexts of the given files.

    @param  paths   The files/directories for which to restore their contexts.
    """
    paths = flatten(paths)
    for path in paths:
        runCmd('restorecon', path)

def restoreconR(*paths):
    """
    Restores the SELinux contexts of the given files. This method also recurses
    into directories.

    @param  paths   The files/directories for which to restore their contexts.
    """
    paths = flatten(paths)
    for path in paths:
        runCmd('restorecon', '-R', path)

def installPrivateKey(cfgScript, keyPath, destName = None):
    """
    Installs the given private key into the '/etc/pki/tls/private' folder.

    @param  cfgScript   The context object (provides us with the path to the
                        tool for decrypting private keys).

    @param  keyPath     The path to the private key to install.
    """
    keyPath = joinPaths(keyPath)
    if destName is None:
        destPath = join(KEYS_DIR, basename(keyPath))
    else:
        destPath = join(KEYS_DIR, destName)
    if not exists(destPath):
        runCmd([dirCertifikati(cfgScript), 'DecryptPrivateKey.sh'], keyPath, '-o', destPath)
        chmod(destPath, 0400)
        restorecon(destPath)
        info("Installed private key '" + destPath + "'.")

def installUrbasPrivateKey(cfgScript, keyName, destName = None):
    """
    Installs the given 'urbas.si' private key into the '/etc/pki/tls/private'
    folder.

    @param  cfgScript   The context object (provides us with the path to the
                        private keys and the tool for decrypting private keys).

    @param  keyName     The name of the private key to install.
    """
    if destName is None:
        destPath = join(KEYS_DIR, keyName)
    else:
        destPath = join(KEYS_DIR, destName)
    keyName = joinPaths([dirCertifikatiUrbasSi(cfgScript), 'private', keyName])
    if not exists(destPath):
        runCmd([dirCertifikati(cfgScript), 'DecryptPrivateKey.sh'], keyName, '-o', destPath)
        chmod(destPath, 0400)
        restorecon(destPath)
        info("Installed private key '" + destPath + "'.")

def installUrbasCert(cfgScript, certName, destName = None):
    """
    Installs the given 'urbas.si' certificate into the '/etc/pki/tls/certs'
    folder.

    @param  cfgScript   The context object (provides us with the path to the
                        private keys and the tool for decrypting private keys).

    @param  certName    The name of the certificate to install.
    """
    if destName is None:
        destPath = join(CERTS_DIR, certName)
    else:
        destPath = join(CERTS_DIR, destName)
    createLink([dirCertifikatiUrbasSi(cfgScript), 'public', certName], destPath, UTILS_CREATE_LINK_HARD_LINK | UTILS_CREATE_LINK_DELETE, 0444, 'root', 'root')
    restorecon(destPath)
    info("Installed certificate '" + destPath + "'.")

# coding=UTF-8
#
#   Project: HomeLib
# 
#       A library for configuration and management of a personal environment.
# 
# File name: config.py
# 
#    Author: Matej Urbas [matej.urbas@gmail.com]
#   Created: 28-Sep-2010, 22:40:38
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

from ConfigParser import SafeConfigParser
from logging import error
from logging import info
from logging import warning
from os import fdopen
from os.path import join
from shutil import move
from tempfile import mkstemp
from traceback import format_exc

from homelib.service import Service
from homelib.utils import addLoggerHandler
from homelib.utils import cfgGetIntOrDefault
from homelib.utils import cfgSet
from homelib.utils import flatten
from homelib.utils import loadClass
from homelib.utils import makedirs
from homelib.utils import removeLoggerHandler



###
### Configuration related stuff
###

"""
The section in the HomeLib's configuration file that contain all information
about configuration scripts (scripts that update the configuration of a machine
or a user's home folder).
"""
CFG_SEC_CONFIG="Configuration"

"""
This is the file that stores the version of the configuration update process for
a particular 'configuration update script'. This file resides in the directory
configured in the HomeLib's configuration file with the option name
'<script id>.cfgScriptStore'.
"""
CONFIG_VERSION_FILE=".config_version"

"""
This section is in the 'version file' above. It contains information about how
far we have come with the configuration update process and other per
configuration script info.
"""
CFG_SEC_VINFO="Current Version Info"

"""
The version to which the script was able to update the configuration.
"""
CFG_VINFO_CUR_VERSION="updatedToVersion"



class Config(Service):
    """
    This class is the implementation of the 'Configuration Service'. It provides
    home/machine configuration functionality.

    It maintains a list of configuration scripts (these are specified in the
    HomeLib's configuration file), runs them, and maintains a 'version file'
    (which indicates to which version the current target's configuration has
    been upgraded already).
    """
    def __init__(self, main=None):
        Service.__init__(self, main)
        # Get all the known configuration scripts from the main HomeLib's
        # configuration file.
        self.__cfgScripts = {}
        # A list of all the names of the configuration scripts (in the same order
        # as they were specified in the HomeLib configuration)
        self.__cfgScriptsNames = []
        main = self.getMain()
        i = 0
        while True:
            curCfgScript = main.getCfgs(CFG_SEC_CONFIG, [i.__str__() + ".cfgScript" + s for s in [ "Name", "Class", "Path", "Store", "Description", "RootRequired" ]])
            if not curCfgScript[0]:
                break;
            if self.__cfgScripts.has_key(curCfgScript[0]):
                raise Exception("Found duplicate configuration entry '" + curCfgScript[0] + "'.")
            self.__cfgScripts[curCfgScript[0]] = curCfgScript
            self.__cfgScriptsNames.append(curCfgScript[0])
            i = i + 1



    def getAllCfgScriptsDetails(self):
        """
        @returns    A dictionary where the name of the configuration script is
                    the key, and the values are lists that contain all the
                    details.

                    Details contain the following:

                        0   - The name of the script (incidentally, this is the
                              name of the python module to be loaded).

                        1   - The name of the class in the above module to load.

                        2   - The path where to search for the script/module.

                        3   - The directory where to store persistent
                              information about the execution progress of the
                              configuration script.

                        4   - A human readable description of what the script
                              actually does.

                        5   - Indicates whether root privileges are required to
                              run this script.
        """
        return self.__cfgScripts.copy()



    def getCfgScriptsCount(self):
        """
        @returns    The number of loaded configuration scripts.
        """
        return len(self.__cfgScripts)



    def getCfgScriptsNames(self):
        """
        @returns    A collection of configuration scripts' names (in the same order as
                    they were specified in the HomeLib configuration file).
        """
        return self.__cfgScriptsNames



    def getCfgScriptDetails(self, cfgScriptName):
        """
        @param  cfgScriptName   The name of the script (incidentally, this is
                                the name of the python module that implements
                                the logic of the script).

        @returns    Details of the given script. Also, this method returns
                    'None' if the script is not known.

                    Details contain the following:

                        0   - The name of the script (incidentally, this is the
                              name of the python module to be loaded).

                        1   - The name of the class in the above module to load.

                        2   - The path where to search for the script/module.

                        3   - The directory where to store persistent
                              information about the execution progress of the
                              configuration script.

                        4   - A human readable description of what the script
                              actually does.
        """
        return list(self.__cfgScripts[cfgScriptName]) if self.__cfgScripts.has_key(cfgScriptName) else None


    ##
    #Loads the script with the given name and returns it. This method does not
    #initialise the script (it does not call its \link ConfigScript.init \endlink or
    #\link ConfigScript.preRun \endlink methods).
    #
    #@param  cfgScriptName   The name of the script to load.
    #
    #@returns   A tuple of three elements:
    #           <ul>
    #               <li>the first element is the script object (an object
    #                   of type \link ConfigScript \endlink)</li>
    #               <li>the second element is the version of the last run of
    #                   this script.</li>
    #               <li>and the third element is a list of details about the
    #               (see \link Config.getCfgScriptDetails \endlink).</li>
    #           </ul>
    #           If the module could not have been loaded for any reason, an
    #           exception will be thrown.
    def loadScript(self, cfgScriptName):
        """
        Loads the script with the given name and returns it. This method does not
        initialise the script (it does not call its \link ConfigScript.init \endlink or
        \link ConfigScript.preRun \endlink methods).

        @param  cfgScriptName   The name of the script to load.

        @returns   A tuple of three elements:
                   <ul>
                       <li>the first element is the script object (an object
                           of type \link ConfigScript \endlink)</li>
                       <li>the second element is the version of the last run of
                           this script.</li>
                       <li>and the third element is a list of details about the
                       (see \link Config.getCfgScriptDetails \endlink).</li>
                   </ul>
                   If the module could not have been loaded for any reason, an
                   exception will be thrown.
        """
        # First check that this machine is known. We can only apply
        # configuration updates for known machines.
        if not self.getMain().serviceMyMachines().isMachineKnown():
            raise Exception("Unknown machine. Could not execute the configuration script on this machine.")
        else:
            # We know the machine, now get the details of the script...
            details = self.getCfgScriptDetails(cfgScriptName)
            if details:
                # Load the saved progress of the last run for this script
                # @type curVersionInfo SafeConfigParser
                curVersionInfo = Config.__loadVersionFile(details)

                # Load the actual script module, class and create an instance.
                inst = loadClass(cfgScriptName, details[1], details[2])()

                # @type inst ConfigScript
                if not isinstance(inst, ConfigScript):
                    raise Exception("The loaded configuration script '" + cfgScriptName + "' is of an unknown type.")

                return inst, curVersionInfo, details
        raise Exception("Could not find details about the '" + cfgScriptName + "' script.")


    ##
    #Initialises the given script (which must be of type \link ConfigScript
    #\endlink). This method runs the configuration script's \link ConfigScript.init \endlink and
    #\link ConfigScript.preRun \endlink methods.
    #<p>The parameters to this function should be the same as the ones returned
    #   by \link Config.loadScript \endlink.</p>
    #
    #\param theScript   the script to initialise (which must be of type \link ConfigScript
    #                   \endlink).
    #
    #\param curVersionInfo  the version of the last run of the given script.
    #
    #\param details details about the configuration script.
    def initScript(self, theScript, curVersionInfo, details):
        """
        Initialises the given script (which must be of type \link ConfigScript
        \endlink). This method runs the configuration script's \link ConfigScript.init \endlink and
        \link ConfigScript.preRun \endlink methods.
        <p>The parameters to this function should be the same as the ones returned
           by \link Config.loadScript \endlink.</p>

        \param theScript   the script to initialise (which must be of type \link ConfigScript
                           \endlink).

        \param curVersionInfo  the version of the last run of the given script.

        \param details details about the configuration script.
        """
        theScript.init(details, curVersionInfo, self)
        # Run the 'pre-run' function -- just before we start calling the
        # update functions.
        theScript.preRun()



    def runScript(self, cfgScriptName, startFrom=None, maxVersion=None):
        """
        Loads the script with the given name and runs it.

        @param  cfgScriptName   The script to run.

        @param  startFrom   <b>[Optional]</b> Indicates with which version we
                            should start executing the script. This option
                            overrides the previous saved state.

        @param  maxVersion  <b>[Optional]</b> The version to which to update.
                            This is the maximum number for which the
                            corresponding config update function will be called.

        @throws If for any reason the script failed or did not start at all.
        """
        inst = None;
        try:
            # Load the script (an exception will be thrown if the loading fails -- so, never will we get None from it).
            (inst, curVersionInfo, details) = self.loadScript(cfgScriptName);

            # Create the logger this script should use
            (lh, fd) = addLoggerHandler(type(inst), details[3])
            _sepMsg("Starting the configuration script '" + cfgScriptName + "'")
            info("This machine is of the following types: " + ', '.join([x for x in self.getMain().serviceMyMachines().getMachineDetails()[2]]))

            self.initScript(inst, curVersionInfo, details)

            # Okay, we have an instance of the script class, now start
            # running. First get the prefix of the methods that do the
            # actual work in the script.
            upFunPrfx = inst.getUpdateMethodPrefix()

            # Get the latest version and start updating.
            i = startFrom if isinstance(startFrom, int) and startFrom >= 0 else inst.getLastRunVersion()

            # Now start calling all the update functions.
            while maxVersion < 0 or i < maxVersion:
                i = i + 1

                # Construct the name of the next update function to call.
                funName = upFunPrfx + i.__str__()
                try:
                    # Try getting a handle on the function
                    fun = getattr(inst, funName)
                except:
                    break
                try:
                    # Finally invoke the update function!
                    fun()
                except UpdateNotAppliedException as ex:
                    info("Update number " + i.__str__() + " not applied. " + ex.__str__())
                except Exception as ex:
                    raise
                _sepMsg("Updated to version number " + i.__str__())
                # Store the last successful update version.
                cfgSet(curVersionInfo, CFG_SEC_VINFO, CFG_VINFO_CUR_VERSION, i)

            inst.postRun()

            _sepMsg("Configuration script '" + cfgScriptName + "' finished successfully")
        except AbortConfigException:
            warning("Configuration aborted with message: " + format_exc())
        except Exception as ex:
            try:
                if inst != None and isinstance(inst, ConfigScript):
                    inst.postFail(ex)
            except Exception as _:
                error("The configuration script threw an exception in the 'Post-Fail Invocation' phase. Error: " + format_exc())
            error("Updating failed. Error: " + format_exc())
            raise ex
        finally:
            try:
                removeLoggerHandler(lh, fd)
            finally:
                Config.__saveVersionFile(details, curVersionInfo)



    @staticmethod
    def __loadVersionFile(details):
        """
        @returns    A reference to the read configuration parser (which has
                    already read the version file).
        """
        storeDir = details[3]
        if not storeDir:
            raise Exception("The store directory for the configuration script '" + details[0] + "' not specified.")
        cfgParser = SafeConfigParser()
        cfgParser.read(join(storeDir, CONFIG_VERSION_FILE))
        return cfgParser



    @staticmethod
    def __saveVersionFile(details, curVersionInfo):
        """
        @param  curVersionInfo  A reference to the read configuration parser
                                (which has already read the version file).
        """
        storeDir = details[3]
        if not storeDir:
            raise Exception("The store directory for the configuration script '" + details[0] + "' not specified.")
        # @type curVersionInfo SafeConfigParser
        try:
            makedirs(storeDir)
        except:
            pass
        (fd, tmpPath) = mkstemp('', CONFIG_VERSION_FILE, storeDir)
        fd = fdopen(fd, 'w')
        curVersionInfo.write(fd)
        fd.close()
        move(tmpPath, join(storeDir, CONFIG_VERSION_FILE))



class ConfigScript(object):
    """
    The base class of all configuration scripts.

    These scripts should implement a list of 'configuration version update'
    functions, which will be one-by-one successively called by the
    'Configuration Service'.

    The functions should have the following signature:

        def <method prefix><version number>(self):
            pass

    A concrete example:

        def update6(self):
            pass

    Where the 'method prefix' is the prefix returned by the method
    @see getUpdateMethodPrefix, and the 'version number' is a positive integer.

    Only those methods will be called that have a greater version number than
    the one stored in the update process information file found in the 'config
    script store' directory.
    """
    def __init__(self):
        self._details = None
        self._versionInfo = None
        self._configService = None



    def init(self, details, versionInfo, configService):
        """
        This method is called just after the constructor and before anything
        else. It initialises important variables for this script.

        @param  details Details contain the following:

                        0   - The name of the script (incidentally, this is the
                              name of the python module to be loaded).

                        1   - The name of the class in the above module to load.

                        2   - The path where to search for the script/module.

                        3   - The directory where to store persistent
                              information about the execution progress of the
                              configuration script.

                        4   - A human readable description of what the script
                              actually does.

        @param  versionInfo The data from the version information file specific
                            to this configuration script.

        @param  configService   The configuration service instance that invoked
                                this script.
        """
        self._details = details
        self._versionInfo = versionInfo
        self._configService = configService



    def getLastRunVersion(self):
        """
        @returns    The version to which this script came last time
                    it was run. Version '0' means the script has
                    not run yet.
        """
        return cfgGetIntOrDefault(self._versionInfo, CFG_SEC_VINFO, CFG_VINFO_CUR_VERSION, 0)



    def preRun(self):
        """
        This method is run just before the 'update' functions are called.

        @param  latestVersion   The version to which this script came last time
                                it was run. Version '0' means the script has
                                not run yet.
        """
        pass



    def postRun(self):
        """
        This method is run just after the 'update' functions have been called.
        """
        pass



    def postFail(self, ex):
        """
        This method is called if any of the update functions fails. After the
        call to this method no other update function will be invoked. The last
        successful update version will still be stored in the version file.

        @param  ex  The exception that occured in one of the update functions.
        """
        pass



    def getUpdateMethodPrefix(self):
        """
        @returns    The prefix for names of functions that apply updates for a
                    particular version (of the home/machine configuration).

                    By default, this method returns 'update_'.

                    For example, a method that applies an update for version 7,
                    would by default have the following signature:

                        def <method prefix><version number>(self):
                            pass

                    A concrete example:

                        def update6(self):
                            pass
        """
        return "update"



    def getMain(self):
        """
        @returns    The contextual 'Main' object (contains all info about
                    configured paths, services etc.).
        """
        return self._configService.getMain()



    def getGiCfg(self, key):
        """
        @returns    The value of the option with the given key in the 'General
                    Information' section of the HomeLib's configuration file.
        """
        return self.getMain().getGiCfg(key)



class UpdateNotAppliedException(Exception):
    """
    This exception is thrown if an update is not applied because of controlled
    reasons.
    """
    pass



class AbortConfigException(Exception):
    """
    This exception is thrown if the configuration script should be aborted
    immediately. No other config script methods will be called after this
    exception.
    """
    pass



def updateOnly(*types):
    """
    This decorator executes the update script if the current machine is of any
    of the given types. Otherwise it throws the UpdateNotAppliedException
    exception.

    @param  types   A list of machine types to check against.
    """
    types = flatten(types)
    def toUpdate(meth):
        def toUpdateImpl(self):
            if self.getMain().serviceMyMachines().isMachineOfType(types):
                meth(self)
            else:
                raise UpdateNotAppliedException('Update applicable only for machines of any of the following types: ' + ', '.join(types))
        return toUpdateImpl
    return toUpdate



def updateAllBut(*types):
    """
    This decorator executes the update script if the current machine is not of
    any of the given types. Otherwise it throws the UpdateNotAppliedException
    exception.

    @param  types   A list of machine types to check against.
    """
    types = flatten(types)
    def toUpdate(meth):
        def toUpdateImpl(self):
            if not self.getMain().serviceMyMachines().isMachineOfType(types):
                meth(self)
            else:
                raise UpdateNotAppliedException('Update applicable only for machines not of the following types: ' + ', '.join(types))
        return toUpdateImpl
    return toUpdate



def updateMachine(*machineNames):
    """
    This decorator executes the update script only for machines with a specific
    name (e.g., 'toncka.urbas.si'). If the current machine's name is not in the
    list then the update will not be applied and a UpdateNotAppliedException
    will be thrown.

    @param  types   A list of machine names (e.g., 'toncka.urbas.si') to check
    against.
    """
    machineNames = flatten(machineNames)
    def toUpdate(meth):
        def toUpdateImpl(self):
            if machineNames and self.getMain().serviceMyMachines().getCurrentMachineName() in machineNames:
                meth(self)
            else:
                raise UpdateNotAppliedException('Update applicable only for the following machines: ' + ', '.join(machineNames))
        return toUpdateImpl
    return toUpdate



def _sepMsg(msg):
    info('{0:=^80}'.format(' ' + msg + ' '))

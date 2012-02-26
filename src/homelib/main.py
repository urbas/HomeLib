from ConfigParser import SafeConfigParser
from homelib.utils import ENV_VAR_HOME_ABS_PATH
from os.path import abspath
from os.path import isdir
from os.path import isfile
from os.path import join

from homelib.utils import cfgGetOrDefault
from homelib.utils import getHomeLibFile
from homelib.utils import getHomePath
from homelib.utils import joinPaths



###
### Configuration related stuff
###

"""
The name of the HomeLib configuration file.
"""
HOMELIB_CONFIG_FILE="homelib.config"

"""
The name of the directory which contains the HomeLib configuration file.
"""
HOMELIB_CONFIG_DIR=".homelib"

"""
The section that contain all general information for the HomeLib.
"""
CFG_SEC_GINFO="General Information"

"""
The given name of the primary user of HomeLib.
"""
CFG_GINFO_NAME="name"

"""
The family name of the primary user of HomeLib.
"""
CFG_GINFO_SURNAME="surname"

"""
The e-mail of the primary user of HomeLib.
"""
CFG_GINFO_EMAIL="email"

"""
The folder where to store default logs produced by HomeLib.
"""
CFG_GINFO_LOG_DIR="logDir"



###
### Private Helper Functions
###



def _tryLoadConfigFile(config, path):
    """
    Tries to read the configuration file at the given path.

    @param  config  The configuration parser to use when reading the config
                    file.

    @param  path    The path to the configuration file to read.

    @returns    True, if the reading succeeded. False otherwise.
    """
    if isfile(path):
        # @type config SafeConfigParser
        config.read(path)
        return True
    return False



###
### The main class
###

class Main(object):
    """
    This class contains all basic information for all HomeLib services.

    It is important to note that this class loads up a configuration file.
    If not explicitly given, then this class first tries to find the
    'homelib.config' file in the user's home folder and then continues to search
    other default paths. Here is the order of search:

        <homeDir>/.homelib/homelib.config
        ~/.homelib/homelib.config
        /etc/homelib/homelib.config
        <script location>/homelib.config

    Keys used in the 'homelib.config' file are listed in variables whose name
    starts with 'CFG_<secname word>_<keyname>' and 'CFG_SEC_<secname word>'.
    """

    def __init__(self, homeDir=None, nestDir=None, configFile=None):
        """
        Initialises an instance of this class.

        @param  absHomeDir  The path of the desired home folder to be used in
                            this HomeLib session.

        @param  nestName    The name of the directory that contains the 'Nest'
                            local repository clone.

        @param  configFile  The path to the HomeLib configuration file.
        """
        ###
        ### Configuration
        ###
        self.__absHomeDir = abspath(homeDir or getHomePath())
        self.__absNestDir = abspath(nestDir or join(self.__absHomeDir, "Nest"))
        self.__configFileVars = None
        # Try to read the configuration file. Raise an exception if the
        # configuration file could not be loaded.
        self.__config = SafeConfigParser()
        if (not (configFile and _tryLoadConfigFile(self.__config, configFile)) and
            not (homeDir and _tryLoadConfigFile(self.__config, join(homeDir, HOMELIB_CONFIG_DIR, HOMELIB_CONFIG_FILE))) and
            not _tryLoadConfigFile(self.__config, join(getHomePath(), HOMELIB_CONFIG_DIR, HOMELIB_CONFIG_FILE)) and
            not _tryLoadConfigFile(self.__config, join("/etc", HOMELIB_CONFIG_DIR, HOMELIB_CONFIG_FILE)) and
            not _tryLoadConfigFile(self.__config, getHomeLibFile(HOMELIB_CONFIG_FILE))
           ):
            raise Exception("The configuration file could not be loaded. Please check that there is a configuration file in one of the predefined directories.")
        if not isdir(self.__absNestDir):
            raise Exception("The nest directory '" + self.__absNestDir + "' is not valid. Please specify the '" + ENV_VAR_HOME_ABS_PATH + "' environment variable, which tells where to look for the 'Nest' folder.")
        ###
        ### Services
        ###
        self.__nestService = None
        self.__myMachinesService = None
        self.__configService = None
        self.__softwareService = None
        ###
        ### Events
        ###
        self.__dirNestChangedListeners = []
        ###
        ### Logging
        ###
        self.__logger = None
        ####
        #### Finalisation
        ####
        self.__refreshConfigFileVars()



    ###
    ### Service Providers Methods
    ###

    def serviceNest(self):
        """
        @returns    The currently configured nest service implementation. It
                    provides version control functionality for the 'Nest'
                    repository (this is the repository that contains this
                    library and all related configuration files).
        """
        if not self.__nestService:
            from homelib.nest import Nest
            self.__nestService = Nest.loadChosenImpl(self)
        return self.__nestService



    def serviceMyMachines(self):
        """
        @returns    The 'My Machines' service, which helps identify machines.
        """
        if not self.__myMachinesService:
            from homelib.mymachines import MyMachines
            self.__myMachinesService = MyMachines(self)
        return self.__myMachinesService



    def serviceSoftware(self):
        """
        @returns    The 'Software Management' service, which provides software
                    installation, removal and similar functionality.
        """
        if not self.__softwareService:
            from homelib.software import Software
            self.__softwareService = Software.loadChosenImpl(self)
        return self.__softwareService



    def serviceConfig(self):
        """
        @returns    The 'Configuration' service, which provides home/machine
                    configuration automation.
        """
        if not self.__configService:
            from homelib.config import Config
            self.__configService = Config(self)
        return self.__configService



    ###
    ### Configuration Access Methods
    ###

    def getCfg(self, section, key):
        """
        @param  section The section in the configuration file where to search
                        for the option with the given name.

        @param  key     The name of the option we want the value of.

        @returns    The configuration value from the configuration file (or None
                    if the option with the given key does not exist).
        """
        return cfgGetOrDefault(self.__config, section, key, None, self.__configFileVars)



    def getCfgs(self, section, keys):
        """
        @param  section The section in the configuration file where to search
                        for the options with the given names.

        @param  keys    The names of the options we want the values of.

        @returns    A list of option values as stored in the configuration file.
        """
        return [self.getCfg(section, key) for key in keys]



    def getGiCfg(self, key):
        """
        This method is a shorthand for 'getCfg(CFG_SEC_GINFO, key)'.

        @param  key The name of the option we want the value of.

        @returns    The general information configuration value from the
                    configuration file, or None, if no such option exists.
        """
        return cfgGetOrDefault(self.__config, CFG_SEC_GINFO, key, None, self.__configFileVars)



    def getUserName(self):
        """
        @returns    The user's given name (as set in the configuration).
        """
        return self.getGiCfg(CFG_GINFO_NAME);



    def getUserSurname(self):
        """
        @returns    The user's surname (as set in the configuration).
        """
        return self.getGiCfg(CFG_GINFO_SURNAME);



    def getEMail(self):
        """
        @returns    The user's e-mail (as set in the configuration).
        """
        return self.getGiCfg(CFG_GINFO_EMAIL);



    def getFullUserName(self):
        """
        @returns    Something like this:

                       <Name> <Surname>
        """
        return self.getUserName() + " " + self.getUserSurname();



    def getFullUserDetails(self):
        """
        @returns    Something like this:

                       <Name> <Surname> [<email>]
        """
        return self.getFullUserName() + " [" + self.getEMail() + "]";



    ###
    ### Some important directories
    ###

    def dirHome(self):
        """
        @returns    The absolute path to the home directory (may not be the home
                    directory of the current user -- it can be configured upon
                    the creation of this class).
        """
        return self.__absHomeDir;



    def dirNest(self):
        """
        @returns    The absolute path to the local clone of the 'Nest'
                    repository. This repository contains this library and
                    absolutely all related files.
        """
        return self.__absNestDir;



    def setDirNest(self, dirPath):
        """
        @param  dirPath The new directory where to find the 'Nest' repository.
        """
        dirPath = joinPaths(dirPath)
        if not isdir(dirPath):
            raise IOError("Could not change the Nest folder to '" + dirPath + "'. Please specify a valid folder.")
        oldDir = self.__absNestDir
        self.__absNestDir = dirPath
        self.__refreshConfigFileVars()
        self.__invokeDirNestChangedEvent(oldDir)



    def dirDokumenti(self):
        """
        @returns    The directory with random documents.
        """
        return join(self.dirNest(), "Dokumenti");



    def dirProjects(self):
        """
        @returns    The directory with random projects (including this library).
        """
        return join(self.dirNest(), "Projects");



    def dirOsebno(self):
        """
        @returns    The directory with personal stuff.
        """
        return join(self.dirNest(), "Osebno");



    def dirNastavitve(self):
        """
        @returns    The directory with important notes and configuration files.
        """
        return join(self.dirNest(), "Nastavitve");



    def dirResearch(self):
        """
        @returns    The directory with PhD related files.
        """
        return join(self.dirNest(), "Research")



    def dirHomeLibConf(self):
        """
        @returns    The directory with private per-user HomeLib configuration
                    files.
        """
        return join(self.dirHome(), HOMELIB_CONFIG_DIR)



    ###
    ### Events
    ###

    def addDirNestChangedListener(self, callback):
        """
        Registers the given callback to the 'Nest Directory Changed' event.

        @param  callback    This method will be invoked when the event is
                            triggered.

                            This method will be called with two arguments:

                                main      - the source of the event.

                                eventData - the old value of the Nest directory.
        """
        if not callback:
            raise Exception("A valid event callback must be specified.")
        self.__dirNestChangedListeners.append(callback)

    def removeDirNestChangedListener(self, callback):
        self.__dirNestChangedListeners.remove(callback)

    def __invokeDirNestChangedEvent(self, eventData):
        for callback in self.__dirNestChangedListeners:
            callback(self, eventData)



    ###
    ### Private helper methods
    ###
    
    def __refreshConfigFileVars(self):
        self.__configFileVars = {
            'dokumentidir'  :   self.dirDokumenti(),
            'homedir'       :   self.dirHome(),
            'nastavitvedir' :   self.dirNastavitve(),
            'nestdir'       :   self.dirNest(),
            'osebnodir'     :   self.dirOsebno(),
            'projectsdir'   :   self.dirProjects(),
            'researchdir'   :   self.dirResearch(),
            'homelibconfdir':   self.dirHomeLibConf()
        }

from ConfigParser import SafeConfigParser
from os.path import *
from homelib.utils import *
import sys
import os



###
### Configuration related stuff
###

"""
The name of the HomeLib configuration file.
"""
HOMELIB_CONFIG_FILE = "homelib.config"

"""
The name of the `home` directory which contains the HomeLib configuration file.
"""
HOMELIB_CONFIG_DIR = ".homelib"

"""
The name of the `etc` directory which contains the HomeLib configuration file.
"""
HOMELIB_ETC_CONFIG_DIR = "homelib"

"""
The section that contain all general information for the HomeLib.
"""
CFG_SEC_GINFO = "General Information"

"""
The given name of the primary user of HomeLib.
"""
CFG_GINFO_NAME = "name"

"""
The family name of the primary user of HomeLib.
"""
CFG_GINFO_SURNAME = "surname"

"""
The e-mail of the primary user of HomeLib.
"""
CFG_GINFO_EMAIL = "email"

"""
The folder where to store default logs produced by HomeLib.
"""
CFG_GINFO_LOG_DIR = "logDir"



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
    This class is the main entry point to the HomeLib services and 
    contains all configuration information.

    It is important to note that this class loads up a configuration file.
    If not explicitly given, then this class first tries to find the
    'homelib.config' file in the user's home folder and then continues to search
    other default paths. Here is the order of search:

        <homeDir>/.homelib/homelib.config
        /etc/homelib/homelib.config
        <script location>/homelib.config

    Keys from the 'homelib.config' file that are used in this class are listed in variables whose name
    starts with 'CFG_<secname word>_<keyname>' and 'CFG_SEC_<secname word>'.
    """

    def __init__(self, homeDir=None, configFile=None):
        """
        Initialises an instance of this class.

        @param  homeDir     The path of the desired home folder to be used in
                            this HomeLib session.

        @param  configFile  The path to the HomeLib configuration file.
        """
        ###
        ### Configuration
        ###
        self.__absHomeDir = abspath(homeDir or getHomePath())
        self.__configFileVars = None
        
        # Try to read the configuration file. Raise an exception if the
        # configuration file could not be loaded.
        
        # First we build a list of paths where we will search for the
        # configuration file. 
        loadDirs = [p
                    for p in
                    [configFile,
                     join(homeDir, HOMELIB_CONFIG_DIR, HOMELIB_CONFIG_FILE) if homeDir else None,
                     join(getHomePath(), HOMELIB_CONFIG_DIR, HOMELIB_CONFIG_FILE),
                     join("/etc", HOMELIB_ETC_CONFIG_DIR, HOMELIB_CONFIG_FILE),
                     getHomeLibFile(HOMELIB_CONFIG_FILE)]
                    if p]
        
        self.__config = SafeConfigParser()
        
        # Now try to load the configuration file and report an error is it
        # could not be loaded from any of the predefined paths.
        self.__configFile = next((p for p in loadDirs if _tryLoadConfigFile(self.__config, p)), None)
        if self.__configFile is None:
            raise Exception("The configuration file could not be loaded. Please check that there is a configuration file in one of these paths: " + str(loadDirs))
        
        ###
        ### Services
        ###
        self.__myMachinesService = None
        self.__configService = None
        self.__softwareService = None
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



    def dirConfFile(self):
        """
        @returns    The absolute path to the loaded configuration file.
        """
        return self.__configFile;



    def dirConfDir(self):
        """
        @returns    The directory of the loaded configuration file.
        """
        return os.path.dirname(self.__configFile);



    ###
    ### Private helper methods
    ###
    
    def __refreshConfigFileVars(self):
        self.__configFileVars = {
            'homedir'   :   self.dirHome(),
            'confdir'   :   self.dirConfDir(),
            'conffile'  :   self.dirConfFile()
        }



###
### Main entry point:
###
def main():
    import mainargs
    args = mainargs.parser.parse_args()
    main = Main()
    cfgService = main.serviceConfig()
    if args.listScripts:
        print "The list of configuration scripts:"
        for script in cfgService.getCfgScriptsNames():
            print "  - " + script + " :: " + cfgService.getCfgScriptDetails(script)[4] + " :: " + str(cfgService.getCfgScriptDetails(script))
        return 0
    elif args.scriptName is None:
        # Run all configuration scripts:
        for script in cfgService.getCfgScriptsNames():
            cfgService.runScript(script)
    else:
        # Run the selected configuration script:
        cfgService.runScript(args.scriptName, args.start, args.end)
    return 0

if __name__ == '__main__':
    sys.exit(main())
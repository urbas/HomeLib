# coding=UTF-8
#
#   Project: HomeLib
# 
#       A library for configuration and management of a personal environment.
# 
# File name: Service.py
# 
#    Author: Matej Urbas [matej.urbas@gmail.com]
#   Created: 26-Sep-2010, 00:30:38
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

class Service(object):
    """
    The base-class of all services in this library.
    """
    def __init__(self, main=None):
        """
        @param  main    The main configuration class (from which this service
                        will extract all its relevant data).
        """
        from homelib.main import Main
        self.__main = main if isinstance(main, Main) else Main()
        self.__main.addDirNestChangedListener(self.onDirNestChanged)



    def getMain(self):
        """
        @returns        The main configuration class (from which this service
                        will extract all its relevant data).
        """
        return self.__main



    def onDirNestChanged(self, main, oldNestDir):
        """
        This method is invoked whenever the main 'Nest' directory changes.
        """
        pass



    def close(self):
        """
        This method is called by 'main' after the service is no longer needed
        and will never be used again.

        This method should release all resources allocated by this service
        during its life.
        """
        self.__main.removeDirNestChangedListener(self.onDirNestChanged)



class MultiService(Service):
    """
    The base-class of all services in this library that have multiple
    implementations (Nest and Software services are just two examples).
    """
    def __init__(self, main=None):
        Service.__init__(self, main)
        self.__cfgSection = None
        try:
            self.__cfgSection = self.getMain().getGiCfg(self.getChosenImplCfgSection())
        except:
            pass



    @classmethod
    def knownImpls(cls):
        """
        Lists all known implementations of this service.

        @returns    A dictionary of tuples containing the following elements:

                        key     -   The name of the implementation of the
                                    service (as it can appear in the HomeLib
                                    configuration file).

                        value.0   - The name of the module that contains the
                                    implementation.

                        value.1   - [Optional] The name of the implementing
                                    class.

                        value.2   - [Optional] The path where to search for the
                                    module.
        """
        raise NotImplementedError()



    @classmethod
    def getChosenImplCfgKey(cls):
        """
        @returns    The name of the option in the HomeLib's configuration file
                    (found under section 'General Information') that configures
                    which implementation of this service should be used.
        """
        raise NotImplementedError()



    @classmethod
    def getChosenImplCfgSection(cls):
        """
        @returns    The name of the section in the HomeLib's configuration file
                    that the chosen implementation of this service should use.
        """
        raise NotImplementedError()



    @classmethod
    def loadChosenImpl(cls, main=None):
        """
        Loads the implementation that has been chosen in the HomeLib's
        configuration file.

        @param  main        The main object with which to initialise the loaded
                            implementation.

        @returns    The name of the section in the HomeLib's configuration file
                    that the chosen implementation of this service should use.

        @throws     If the load failed for any reason.
        """
        if not main:
            import homelib.main
            main = homelib.main.Main()
        return cls.loadImpl(main.getGiCfg(cls.getChosenImplCfgKey()), main)



    @classmethod
    def loadImpl(cls, implName, main=None):
        """
        @param  implName    The name of the implementation to load.

        @param  main        The main object with which to initialise the loaded
                            implementation.

        @returns    The name of the section in the HomeLib's configuration file
                    that the chosen implementation of this service should use.

        @throws     If the load failed for any reason.
        """
        knownImpls = cls.knownImpls()
        if implName in knownImpls:
            impl = knownImpls[implName]
            if impl and len(impl) > 0:
                from homelib.utils import loadClass
                return loadClass(impl[0], impl[1] if len(impl) > 1 else None, impl[2] if len(impl) > 2 else None)(main)
        raise Exception("The implementation '" + implName + "' is not known for this service. Known implementations: " + ', '.join(knownImpls.keys()))



    def getCfgSection(self):
        """
        @returns    The section (in the HomeLib's configuration file) this
                    service should use to get its configuration. Note that this
                    function might return 'null', in which case this
                    implementation will not be configured.
        """
        return self.__cfgSection
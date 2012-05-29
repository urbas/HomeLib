'''
Created on 29 May 2012

@author: matej
'''

import argparse

"""
The argument parser for the main entry point of HomeLib.
"""
parser = argparse.ArgumentParser(
    description = "Runs system configuration scripts. They configure the machine and keep the configuration updated."
)

parser.add_argument('scriptName',
    metavar='script name',
    type=str,
    nargs='?',
    help='The name of the configuration script to run. If not given, all scripts specified in the `homelib.config` configuration will be run. To list all configuration scripts that can be run, use option `l`'
)

parser.add_argument('-s', '--start',
    type=int,
    nargs=1,
    metavar='version',
    help='This option is used only when `script name` is given. It tells HomeLib to start executing the configuration script at the update `version`.'
)

parser.add_argument('-e', '--end',
    type=int,
    nargs=1,
    metavar='version',
    help='This option is used only when `script name` is given. It tells HomeLib to stop executing the configuration script with update `version`.'
)

parser.add_argument('-l', '--listScripts',
    action='store_true',
    help='List the configuration scripts provided in the `homelib.config` configuration file and exit.'
)
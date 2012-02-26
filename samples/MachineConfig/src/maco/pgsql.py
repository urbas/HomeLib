# coding=UTF-8
#
#   Project: HomeLib
#
#       A library for configuration and management of a personal environment.
#
# File name: pgsql.py
#
#    Author: Matej Urbas [matej.urbas@gmail.com]
#   Created: 10-Oct-2010, 17:54:41
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

from os.path import join

from homelib.utils import UTILS_CREATE_LINK_HARD_LINK
from homelib.utils import createLink
from homelib.utils import runCmd



"""
This is the base directory for PgSQL configuration.
"""
PGSQL_DIR='/var/lib/pgsql'

"""
This is the directory which contains all PgSQL data and configuration files.
"""
PGSQL_DATA_DIR=join(PGSQL_DIR, 'data')

"""
The name of the PgSQL service (in Fedora).
"""
PGSQL_SERVICE_NAME='postgresql'

"""
The name of the PgSQL user (in Fedora).
"""
PGSQL_SERVICE_USER='postgres'

"""
The group of the PgSQL user (in Fedora).
"""
PGSQL_SERVICE_GROUP='postgres'

"""
The location of my PgSQL configuration files.
"""
PGSQL_NASTAVITVE_DIR='Postgre'
PGSQL_NASTAVITVE_MACO_DIR=join(PGSQL_NASTAVITVE_DIR, 'MacoConfigFiles')

"""
Important configuration files
"""
PGSQL_HBA_FILE='pg_hba.conf'
PGSQL_IDENT_FILE='pg_ident.conf'
PGSQL_MAIN_CONF_FILE='postgresql.conf'

"""
The permissions mode of the above three files.
"""
PGSQL_CONF_FILE_MODE=0600



def configurePgSql(cfgScript):
    installPgSql(cfgScript)
    initPgSql(cfgScript)
    enablePgSql(cfgScript)



def installPgSql(cfgScript):
    cfgScript.getMain().serviceSoftware().install(
            "postgresql-server",
            "postgresql",
            "pgadmin3"
        )

def initPgSql(cfgScript):
#    runCmd("service", PGSQL_SERVICE_NAME, 'initdb') # Doesn't seem to be working in F16 anymore
    # @type main Main
    main = cfgScript.getMain()
    createLink([main.dirNastavitve(), PGSQL_NASTAVITVE_MACO_DIR, PGSQL_HBA_FILE], PGSQL_DATA_DIR, UTILS_CREATE_LINK_HARD_LINK, PGSQL_CONF_FILE_MODE, PGSQL_SERVICE_USER, PGSQL_SERVICE_GROUP)
    createLink([main.dirNastavitve(), PGSQL_NASTAVITVE_MACO_DIR, PGSQL_IDENT_FILE], PGSQL_DATA_DIR, UTILS_CREATE_LINK_HARD_LINK, PGSQL_CONF_FILE_MODE, PGSQL_SERVICE_USER, PGSQL_SERVICE_GROUP)
    createLink([main.dirNastavitve(), PGSQL_NASTAVITVE_MACO_DIR, PGSQL_MAIN_CONF_FILE], PGSQL_DATA_DIR, UTILS_CREATE_LINK_HARD_LINK, PGSQL_CONF_FILE_MODE, PGSQL_SERVICE_USER, PGSQL_SERVICE_GROUP)

def enablePgSql(cfgScript):
    cfgScript.getMain().serviceSoftware().enableServices([
            PGSQL_SERVICE_NAME
        ],
            '35')

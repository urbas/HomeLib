# coding=UTF-8
#
#   Project: HomeLib
# 
#       A library for configuration and management of a personal environment.
# 
# File name: paths.py
# 
#    Author: Matej Urbas [matej.urbas@gmail.com]
#   Created: 16-Oct-2010, 23:32:49
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

###
### Standard Paths
###

SSH_DIR='/etc/ssh'
SYSCONFIG_DIR='/etc/sysconfig'
NET_SCRIPTS_DIR=join(SYSCONFIG_DIR, 'network-scripts')
CRON_WEEKLY_DIR='/etc/cron.weekly'
CRON_DAILY_DIR='/etc/cron.daily'
MERCURIAL_ETC_DIR='/etc/mercurial'
HTTPD_CONFD_DIR='/etc/httpd/conf.d'
HTTPD_CONF_DIR='/etc/httpd/conf'
CERTS_DIR='/etc/ssl/certs'
KEYS_DIR='/etc/ssl/private'
WWW_HTML_DIR='/var/www/html'
ETC_DIR='/etc'
NAMED_CONF_DIR='/etc/bind'
NAMED_VAR_CONF_DIR='/var/named'
NAMED_SLAVES_DIR='/var/named/slaves'
POSTFIX_ETC_DIR='/etc/postfix'
DOVECOT_ETC_DIR='/etc/dovecot'
DOVECOT_CONFD_DIR='/etc/dovecot/conf.d'
PAMD_DIR='/etc/pam.d'
SYSTEMD_UNITS_DIR='/lib/systemd/system'

###
### Maco Paths
###

MACO_GENERAL_DIR='Maco'
MACO_CONFIG_DIR='Configuration'
MACO_ETC_DIR='etc'
MACO_SYSCONFIG='sysconfig'
MACO_ETC_CRON_DAILY_DIR='cron.daily'
MACO_NETWORKING_DIR='networking'
MACO_NETWORKING_DEVICES_DIR='devices'
MACO_NETWORKING_PROFILES_DIR='profiles'
MACO_NETWORK_SCRIPTS_DIR='network-scripts'
MACO_CUPS_DIR='cups'
MACO_SSH_DIR='ssh'
MACO_DIR='/maco'
MACO_SVN_DIR='svn'
MACO_ETC_HTTPD_DIR='httpd'
MACO_ETC_HTTPD_CONFD_DIR='conf.d'
MACO_ETC_HTTPD_CONF_DIR='conf'
MACO_CERTIFIKATI_DIR='Certifikati'
MACO_CERTIFIKATI_STARTSSL_DIR='startssl'
MACO_CERTIFIKATI_URBAS_SI_DIR='urbas.si'
MACO_HTTPD_DIR='HTTPD'
MACO_BIND_DIR='BIND'
MACO_BIND_CONF_DIR='conf'
MACO_BIND_SLAVES_DIR='slaves'
MACO_POSTFIX_DIR='Postfix'
MACO_DOVECOT_DIR='Dovecot'
MACO_DOVECOT_PAM_DIR='pam.d'
MACO_SELINUX_POLICY_DIR='MainSELinuxPolicy'
MACO_CALENDARS_DIR='calendars'

def dirNastavitve(cfgScript):
    return cfgScript.getMain().getGiCfg('MY_NASTAVITVE_DIR');

def dirMacoGeneral(cfgScript):
    return join(dirNastavitve(cfgScript), MACO_GENERAL_DIR)

def dirMacoConfig(cfgScript):
    return join(dirMacoGeneral(cfgScript), MACO_CONFIG_DIR)

def dirMacoSeLinuxPolicy(cfgScript):
    return join(dirMacoGeneral(cfgScript), MACO_SELINUX_POLICY_DIR)

def dirEtc(cfgScript):
    return join(dirMacoConfig(cfgScript), MACO_ETC_DIR)

def dirSystemdUnitsDir(cfgScript):
    return join(dirMacoConfig(cfgScript), 'lib', 'systemd', 'system')

def dirPostfix(cfgScript):
    return join(dirNastavitve(cfgScript), MACO_POSTFIX_DIR)

def dirDovecot(cfgScript):
    return join(dirNastavitve(cfgScript), MACO_DOVECOT_DIR)

def dirDovecotConfD(cfgScript):
    return join(dirDovecot(cfgScript), 'conf.d')

def dirDovecotPamDir(cfgScript):
    return join(dirDovecot(cfgScript), MACO_DOVECOT_PAM_DIR)

def dirHttpd(cfgScript):
    return join(dirNastavitve(cfgScript), MACO_HTTPD_DIR)

def dirBind(cfgScript):
    return join(dirNastavitve(cfgScript), MACO_BIND_DIR)

def dirBindConf(cfgScript):
    return join(dirBind(cfgScript), MACO_BIND_CONF_DIR)

def dirBindSlaves(cfgScript):
    return join(dirBind(cfgScript), MACO_BIND_SLAVES_DIR)

def dirCertifikati(cfgScript):
    return join(dirNastavitve(cfgScript), MACO_CERTIFIKATI_DIR)

def dirCertifikatiStartSsl(cfgScript):
    return join(dirCertifikati(cfgScript), MACO_CERTIFIKATI_STARTSSL_DIR)

def dirCertifikatiUrbasSi(cfgScript):
    return join(dirCertifikati(cfgScript), MACO_CERTIFIKATI_URBAS_SI_DIR)

def dirSysconfig(cfgScript):
    return join(dirEtc(cfgScript), MACO_SYSCONFIG)

def dirCronDaily(cfgScript):
    return join(dirEtc(cfgScript), MACO_ETC_CRON_DAILY_DIR)

def dirNetworking(cfgScript):
    return join(dirSysconfig(cfgScript), MACO_NETWORKING_DIR)

def dirNetDevices(cfgScript):
    return join(dirNetworking(cfgScript), MACO_NETWORKING_DEVICES_DIR)

def dirNetProfiles(cfgScript):
    return join(dirNetworking(cfgScript), MACO_NETWORKING_PROFILES_DIR)

def dirNetworkScripts(cfgScript):
    return join(dirSysconfig(cfgScript), MACO_NETWORK_SCRIPTS_DIR)

def dirCups(cfgScript):
    return join(dirEtc(cfgScript), MACO_CUPS_DIR)

def dirSsh(cfgScript):
    return join(dirEtc(cfgScript), MACO_SSH_DIR)

def dirSvn(cfgScript):
    return join(dirNastavitve(cfgScript), 'SVN')

def dirSvnPolicy(cfgScript):
    return join(dirSvn(cfgScript), 'Policy')

def dirEtcHttpd(cfgScript):
    return join(dirEtc(cfgScript), MACO_ETC_HTTPD_DIR)

def dirEtcHttpdConfd(cfgScript):
    return join(dirEtcHttpd(cfgScript), MACO_ETC_HTTPD_CONFD_DIR)

def dirEtcHttpdConf(cfgScript):
    return join(dirEtcHttpd(cfgScript), MACO_ETC_HTTPD_CONF_DIR)

def srvDirMaco():
    return MACO_DIR

def srvDirSvn():
    return join(srvDirMaco(), MACO_SVN_DIR)

def srvDirCalendars():
    return join(srvDirMaco(), MACO_CALENDARS_DIR)

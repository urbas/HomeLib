# coding=UTF-8
#
#   Project: HomeLib
# 
#       A library for configuration and management of a personal environment.
# 
# File name: networking.py
# 
#    Author: Matej Urbas [matej.urbas@gmail.com]
#   Created: 16-Oct-2010, 23:28:56
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
from os.path import exists
from os.path import join
from shutil import move

from homelib.utils import UTILS_CREATE_LINK_DELETE
from homelib.utils import UTILS_CREATE_LINK_HARD_LINK
from homelib.utils import chprops
from homelib.utils import createLink
from homelib.utils import mymakedirs
from homelib.utils import runCmd
from maco.paths import *
from maco.selinux import setupMySvnPolicy
from maco.selinux import setupMacoPolicy
from maco.utils import installPrivateKey
from maco.utils import installUrbasCert
from maco.utils import installUrbasPrivateKey
from maco.utils import restorecon
from maco.utils import restoreconR



def setupNetworking(cfgScript):
    mymakedirs(NET_SCRIPTS_DIR)
    createLink([ dirNetworkScripts(cfgScript), 'ifcfg-p33p1' ], NET_SCRIPTS_DIR, UTILS_CREATE_LINK_HARD_LINK, 0644)
    createLink([ dirSysconfig(cfgScript), 'iptables' ], SYSCONFIG_DIR, UTILS_CREATE_LINK_HARD_LINK, 0600)
    createLink([ dirSysconfig(cfgScript), 'system-config-firewall' ], SYSCONFIG_DIR, UTILS_CREATE_LINK_HARD_LINK, 0600)
    restoreconR(SYSCONFIG_DIR)


def setupDesktopNetworking(cfgScript):
    createLink([ dirNetworkScripts(cfgScript), 'ifcfg-p34p1.home_desktop' ], [NET_SCRIPTS_DIR, 'ifcfg-p34p1'], UTILS_CREATE_LINK_HARD_LINK, 0644)
    #createLink([ dirNetworkScripts(cfgScript), 'enablewol' ], NET_SCRIPTS_DIR, UTILS_CREATE_LINK_HARD_LINK | UTILS_CREATE_LINK_DELETE, 0755)
    #createLink([ dirSystemdUnitsDir(cfgScript), 'wakeonlan.service' ], SYSTEMD_UNITS_DIR, UTILS_CREATE_LINK_HARD_LINK | UTILS_CREATE_LINK_DELETE, 0644)
    # We don't need the firewall configuration (the service is disabled anyways).



def setupSsh(cfgScript):
    createLink([ dirSsh(cfgScript), 'sshd_config' ], SSH_DIR, UTILS_CREATE_LINK_HARD_LINK, 0600)
    restoreconR(SSH_DIR)



def setupSvn(cfgScript):
    runCmd('chown', '-R', 'apache:apache', srvDirSvn())
    setupMySvnPolicy(cfgScript)

    createLink([dirSvn(cfgScript), 'SVNBackup'], CRON_WEEKLY_DIR, UTILS_CREATE_LINK_HARD_LINK | UTILS_CREATE_LINK_DELETE, 0550, 'root', 'root')
    restoreconR(CRON_WEEKLY_DIR)
    info('Installed the weekly SVN backup cron script.')

    restoreconR(srvDirSvn())
    info('Configured the SVN repository.')



def setupGit(cfgScript):
    main = cfgScript.getMain()

    createLink([ main.dirNastavitve(), 'Git/Maco/BackupGitRepos.sh' ], CRON_WEEKLY_DIR, UTILS_CREATE_LINK_HARD_LINK | UTILS_CREATE_LINK_DELETE, 0550, 'root', 'root')
    info('Installed the weekly GIT backup cron script.')



def setupCalendarBackup(cfgScript):
    createLink([ dirCronDaily(cfgScript), 'BackupMyCalendars.sh' ], CRON_DAILY_DIR, UTILS_CREATE_LINK_HARD_LINK | UTILS_CREATE_LINK_DELETE, 0550, 'root', 'root')
    info('Installed the daily calendar backup cron script.')



def installHttpdCerts(cfgScript):
    createLink([dirCertifikatiStartSsl(cfgScript), 'urbas.si.20130108.cert.pem'], [CERTS_DIR, 'httpd.urbas.si.cert.pem'], UTILS_CREATE_LINK_HARD_LINK | UTILS_CREATE_LINK_DELETE, 0444, 'root', 'root')
    createLink([dirCertifikatiStartSsl(cfgScript), 'sub.class1.server.ca.pem'], CERTS_DIR, UTILS_CREATE_LINK_HARD_LINK | UTILS_CREATE_LINK_DELETE, 0440, 'root', 'root')
    installPrivateKey(cfgScript, [dirCertifikatiStartSsl(cfgScript), 'urbas.si.20130108.key.pem'], 'httpd.urbas.si.key.pem')
    info('Installed the HTTPD SSL certificates and keys.')



def setupHttpd(cfgScript):
    installHttpdCerts(cfgScript)
#     createLink([dirEtcHttpdConf(cfgScript), 'httpd.conf'], HTTPD_CONF_DIR, UTILS_CREATE_LINK_HARD_LINK, 0644, 'root', 'root')
#     info('Configured HTTPD (deployed the main configuration file).')
# 
#     createLink([dirEtcHttpdConfd(cfgScript), 'subversion.conf'], HTTPD_CONFD_DIR, UTILS_CREATE_LINK_HARD_LINK, 0644, 'root', 'root')
#     info('Configured HTTPD to show the SVN repository on the web.')
# 
#     createLink([dirEtcHttpdConfd(cfgScript), 'ssl.conf'], HTTPD_CONFD_DIR, UTILS_CREATE_LINK_HARD_LINK, 0644, 'root', 'root')
#     restoreconR(HTTPD_CONFD_DIR)
#     info('Configured HTTPD to use the proper certificates.')
# 
#     runCmd('setfacl', '-R', '-m', 'user:apache:rwx,group:apache:rwx,default:user:apache:rwx,default:group:apache:rwx,default:other:r,default:group::r,default:user::rwx,default:mask:rwx,mask:rwx', WWW_HTML_DIR)
#     info('Configured HTML folder access control lists.')



def setupBind(cfgScript):
    createLink([dirBindConf(cfgScript), 'named.conf.default-zones'], NAMED_CONF_DIR, UTILS_CREATE_LINK_HARD_LINK, 0640, 'root', 'bind')
    createLink([dirBindConf(cfgScript), 'named.conf.options'], NAMED_CONF_DIR, UTILS_CREATE_LINK_HARD_LINK, 0640, 'root', 'bind')
    createLink([dirBindConf(cfgScript), 'named.conf.local'], NAMED_CONF_DIR, UTILS_CREATE_LINK_HARD_LINK, 0640, 'root', 'bind')
    createLink([dirBindConf(cfgScript), '90.157.141.db'], NAMED_CONF_DIR, UTILS_CREATE_LINK_HARD_LINK | UTILS_CREATE_LINK_DELETE, 0644, 'root', 'root')
    createLink([dirBindConf(cfgScript), 'urbas.si.db'], NAMED_CONF_DIR, UTILS_CREATE_LINK_HARD_LINK | UTILS_CREATE_LINK_DELETE, 0644, 'root', 'root')
    createLink([dirBindConf(cfgScript), 'stanujem.si.db'], NAMED_CONF_DIR, UTILS_CREATE_LINK_HARD_LINK | UTILS_CREATE_LINK_DELETE, 0644, 'root', 'root')
    createLink([dirBindConf(cfgScript), 'stanuj.si.db'], NAMED_CONF_DIR, UTILS_CREATE_LINK_HARD_LINK | UTILS_CREATE_LINK_DELETE, 0644, 'root', 'root')
    createLink([dirBindConf(cfgScript), 'banda.si.db'], NAMED_CONF_DIR, UTILS_CREATE_LINK_HARD_LINK | UTILS_CREATE_LINK_DELETE, 0644, 'root', 'root')
    #createLink([dirBindSlaves(cfgScript), 'vcsweb.com.db'], NAMED_SLAVES_DIR, UTILS_CREATE_LINK_HARD_LINK | UTILS_CREATE_LINK_DELETE, 0644, 'named', 'named')
    info('Configured BIND (domain name system server).')



def setupDovecot(cfgScript):
    installUrbasPrivateKey(cfgScript, 'mail.urbas.si.20110122.key.pem', 'mail.urbas.si.key.pem')
    installUrbasCert(cfgScript, 'mail.urbas.si.20110122.cert.pem', 'mail.urbas.si.cert.pem')

    createLink([dirDovecotConf(cfgScript), 'dovecot.conf'], DOVECOT_ETC_DIR, UTILS_CREATE_LINK_HARD_LINK, 0644, 'root', 'root')
    
    createLink([dirDovecotConfD(cfgScript), '10-auth.conf'], DOVECOT_CONFD_DIR, UTILS_CREATE_LINK_HARD_LINK, 0644, 'root', 'root')
    createLink([dirDovecotConfD(cfgScript), '10-mail.conf'], DOVECOT_CONFD_DIR, UTILS_CREATE_LINK_HARD_LINK, 0644, 'root', 'root')
    createLink([dirDovecotConfD(cfgScript), '10-master.conf'], DOVECOT_CONFD_DIR, UTILS_CREATE_LINK_HARD_LINK, 0644, 'root', 'root')
    createLink([dirDovecotConfD(cfgScript), '10-ssl.conf'], DOVECOT_CONFD_DIR, UTILS_CREATE_LINK_HARD_LINK, 0644, 'root', 'root')



def setupPostfix(cfgScript):
    installUrbasPrivateKey(cfgScript, 'smtp.urbas.si.20110122.key.pem', 'smtp.urbas.si.key.pem')
    installUrbasCert(cfgScript, 'smtp.urbas.si.20110122.cert.pem', 'smtp.urbas.si.cert.pem')
    createLink([dirPostfix(cfgScript), 'main.cf'], POSTFIX_ETC_DIR, UTILS_CREATE_LINK_HARD_LINK, 0644, 'root', 'root')
    createLink([dirPostfix(cfgScript), 'master.cf'], POSTFIX_ETC_DIR, UTILS_CREATE_LINK_HARD_LINK, 0644, 'root', 'root')
    createLink([dirPostfix(cfgScript), 'sasl', 'smtpd.conf'], [POSTFIX_ETC_DIR, 'sasl'], UTILS_CREATE_LINK_HARD_LINK, 0644, 'root', 'root')
    createLink([dirPostfix(cfgScript), 'aliases'], ETC_DIR, UTILS_CREATE_LINK_HARD_LINK, 0644, 'root', 'root')
#     restorecon(join(ETC_DIR, 'aliases'))

    srcAliases = join(dirPostfix(cfgScript), 'aliases')
    runCmd('postalias', 'hash:' + srcAliases)
    aliases = join(ETC_DIR, 'aliases.db')
    if exists(aliases):
        remove(aliases)
    move(join(dirPostfix(cfgScript), 'aliases.db'), aliases)
    chprops(aliases, 0644, 'root', 'smmsp')
#     restorecon(aliases)

    runCmd('newaliases')

    runCmd('postmap', 'hash:' + join(dirPostfix(cfgScript), 'local_recipient_table'))
    try:
        remove(join(POSTFIX_ETC_DIR, 'local_recipient_table.db'))
    except Exception as ex:
        info("Could not remove '" + join(POSTFIX_ETC_DIR, 'local_recipient_table.db') + "'.");
    move(join(dirPostfix(cfgScript), 'local_recipient_table.db'), POSTFIX_ETC_DIR)
    chprops(join(POSTFIX_ETC_DIR, 'local_recipient_table.db'), 0644, 'root', 'root')

#     restoreconR(POSTFIX_ETC_DIR)



def installHomePage(cfgScript):
    createLink([dirHttpd(cfgScript), 'index.html'], WWW_HTML_DIR, UTILS_CREATE_LINK_HARD_LINK | UTILS_CREATE_LINK_DELETE, 0444, 'apache', 'apache')
    restoreconR(WWW_HTML_DIR)



def setupWebDAVCalendar(cfgScript):
    createLink([dirEtcHttpdConfd(cfgScript), 'mycalendar.conf'], HTTPD_CONFD_DIR, UTILS_CREATE_LINK_HARD_LINK | UTILS_CREATE_LINK_DELETE, 0644, 'root', 'root')
    chprops(join(srvDirMaco(), '.htpasswd.calendars'), 0440, 'apache', 'apache')
    mymakedirs(srvDirCalendars())
    runCmd('chown', '-R', 'apache:apache', srvDirCalendars())
    setupMacoPolicy(cfgScript)
    info('Configured WebDAV on HTTPD for calendars.')

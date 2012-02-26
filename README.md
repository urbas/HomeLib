# HomeLib

HomeLib is a tool and a library with which one can write scripts that handle
the configuration of your machine. For example, you can write scripts that
configure your services (i.e. HTTPD, e-mail servers, certificate installation
etc.), home folders (i.e. installs Nautilus scripts, templates, configures bash
initialisation scripts etc.), installs software, and keeps all of these updated.
These scripts can perform different actions based on the type of the machine.

## Why is HomeLib useful?

This is shown best through an example. Here is a sample configuration script for
a server:

    ### BEGIN SAMPLE

    class MyServerConfiguration(ConfigScript):
        def preRun(self):
            self.downloadConfigurationData()    # Gets all required data to configure this machine

        def postRun(self):
            info("Configuration of this machine has been successful.")

        def postFail(self, ex):
            warning("Something went wrong.")



        def update1(self):
            software = self.getMain().serviceSoftware()
            software.addRepository('http://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-stable.noarch.rpm')
            self.getMain().serviceSoftware().install(
                    "mercurial",
                    "libreoffice-calc",
                    "libreoffice-writer",
                    "eclipse-texlipse",
                    "meld",
                    ...
                )

        @updateOnly(MACHINE_TYPE_LAPTOP)
        def update2(self):
            # Disable SELinux for all laptop machines.
            createLink([self.getGiCfg('MY_FEDORA_CONFIG_DIR'), 'laptop/etc/selinux/config'], '/etc/selinux')
            info("Disabled SELinux (restart required).")

        @updateOnly(MACHINE_TYPE_MACO_SERVER)
        def update3(self):
            # Installs server-specific software and configures services on the server.
            self.getMain().serviceSoftware().install(
                    "dovecot",
                    "postfix",
                    "httpd",
                    "mod_ssl",
                    "bind",
                    ...
                )
            # Configures services on the server.
            configurePgSql(self)
            setupSsh(self)
            setupBind(self)
            setupSvn(self)
            setupHttpd(self)
            installHomePage(self)
            setupPostfix(self)
            setupDovecot(self)
            createUsers(self)
            setupSELinuxPolicy(self)

        @updateOnly(MACHINE_TYPE_LAPTOP, MACHINE_TYPE_CL_OFFICE)
        def update4(self):
            self.getMain().serviceSoftware().install(
                    "emacs"
                )

        ...

        ### SAMPLE END

The same can be done with configuring home folders.

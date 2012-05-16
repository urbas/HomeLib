def setupServices1Common(cfgScript):
    cfgScript.getMain().serviceSoftware().disableServices([
        "avahi-daemon",
        "fcoe",
        "iscsi",
        "iscsid",
        "mdmonitor-takeover",
        "mdmonitor",
        "netfs",
        "sendmail",
        "sm-client",
        "dbus-org.bluez",
        "fcoe",
        'sshd-keygen'
    ])
    cfgScript.getMain().serviceSoftware().enableServices([
        'chronyd'
    ])

def setupServices2Maco(cfgScript):
    cfgScript.getMain().serviceSoftware().enableServices([
            'network',
            'httpd',
            'dovecot',
            'postfix',
            'named',
            'sshd'
        ])
    cfgScript.getMain().serviceSoftware().disableServices([
            "NetworkManager"
        ])

def setupServices3Laptop(cfgScript):
    cfgScript.getMain().serviceSoftware().disableServices([
        "abrt-ccpp",
        "abrt-oops",
        "abrt-vmcore",
        "abrtd",
        "atd",
        "auditd"
        "avahi-daemon",
        "crond",
        "fcoe",
        "fsck-root",
        "ip6tables",
        "iptables",
        "iscsi",
        "iscsid",
        "livesys",
        "livesys-late",
        "lldpad",
        "mdmonitor-takeover",
        "mdmonitor",
        "netfs",
        "rsyslog",
        "sendmail",
        "sm-client"
    ])

def setupServices4Desktop(cfgScript):
    cfgScript.getMain().serviceSoftware().enableServices([
            'network',
            'sshd'
        ])
    cfgScript.getMain().serviceSoftware().disableServices([
            'NetworkManager'
        ])
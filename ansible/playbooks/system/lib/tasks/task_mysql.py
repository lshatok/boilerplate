################################################
__author__ = 'eric sales'
__copyright__ = "Copyright 2017, WebTelemetry US Inc."
__version__ = "0.2.0"
__maintainer__ = "Larry Sellars"
__email__ = "larry.sellars@webtelemetry.us"
__status__ = "production"
################################################
"""
WebTelemetry BootStrap Task Group: task_postgresql

    postgresql_server(config)  {postgresql_server_55}

"""
from fabric.api import *


def postgresql_server_55(config):
    """
    Task:postgresql_server - apt-get install postgresql server
    """
    root_pw = config.get('root_password', 'postgresql123')
    postgresql_ver = 'postgresql-server-5.5'
    print "task:  installing postgresql-server 5.5"
    if 'no' == sudo('which postgresqld || echo "no"'):
        # configs for unattended install
        sudo(
            "debconf-set-selections <<< 'postgresql-server-<version> postgresql-server/root_password password %s'" % root_pw)
        sudo(
            "debconf-set-selections <<< 'postgresql-server-<version> postgresql-server/root_password_again password %s'" % root_pw)
        # install postgresql server version
        sudo('apt-get install -y %s' % postgresql_ver)
        # record auth info #
        sudo('[ -d /WT ] || mkdir -p /WT')
        sudo('echo "root:%s" >> /WT/.postgresql.root' % root_pw)
        print "   POSTGRESQL Root Password set to: ", root_pw
    else:
        print "   skipping: POSTGRESQL server is already installed."

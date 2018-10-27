################################################
__author__ = 'eric sales'
__copyright__ = "Copyright 2017, WildRiver Technologies Inc"
__version__ = "0.2.0"
__maintainer__ = "Larry Sellars"
__email__ = "larry.sellars@wildrivertechnologies.com"
__status__ = "production"
################################################
"""
WebTelemetry BootStrap Task Group: task_cloudera_hadoop

    cloudera_manager(bin_file)

 - supportive functions
    _update_limits()
"""
from fabric.api import *


def _update_limits():
    """
    update limits.conf for Cloudera
    """
    hdfs_limit = "hdfs  -       nofile  32768"
    hbase_limit = "hbase -       nofile  32768"
    # check if limits are already set #
    if 'no' == sudo('grep "^hdfs\s*-\s*nofile" /etc/security/limits.conf || echo "no"'):
        print "   updating hdfs limits for nofile"
        sudo('echo "%s" >> /etc/security/limits.conf' % hdfs_limit)
    if 'no' == sudo('grep "^hbase\s*-\s*nofile" /etc/security/limits.conf || echo "no"'):
        print "   updating hbase limits for nofile"
        sudo('echo "%s" >> /etc/security/limits.conf' % hbase_limit)


def cloudera_manager(bin_file):
    """
    TASK:cloudera_manager - install cloudera manager by running :bin_file
    """
    print "Installing Cloudera Manager"
    # check if already installed #
    if 'no' == sudo('[ -f /etc/init.d/cloudera-scm-server ] || echo "no"'):
        # check for file
        if 'no' == sudo('[ -f %s ] || echo "no"' % bin_file):
            abort("Cloudera Installer file %s not found!" % bin_file)
        _update_limits()
        sudo('%s --i-agree-to-all-licenses --noprompt --noreadme' % (bin_file))
    else:
        print "   skipping: cloudera manager already installed."

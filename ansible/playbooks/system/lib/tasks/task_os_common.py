################################################
__author__ = 'eric sales'
__copyright__ = "Copyright 2017, WildRiver Technologies Inc"
__version__ = "0.2.0"
__maintainer__ = "Larry Sellars"
__email__ = "larry.sellars@wildrivertechnologies.com"
__status__ = "production"
################################################
"""
WebTelemetry BootStrap Task Group: task_os_common

    os_common  {os_common_group}  # misc tasks to prep standard system

 - supportive functions
    os_enable_limits

"""
from fabric.api import *


def os_common_group():
    """
    TASK GROUP:os_common
    """
    os_enable_limits()


def os_enable_limits():
    """
    TASK:enable_limits - update common-session file for pam_limits.so
    """
    print "task:  Enabling Limits"
    if 'no' == sudo('grep -q "^session\s*required\s*pam_limits.so" /etc/pam.d/common-session || echo "no"'):
        print "   updating /etc/pam.d/common-session."
        sudo('echo "session     required    pam_limits.so" >> /etc/pam.d/common-session')
    else:
        print "   pam_limits.so is already set"

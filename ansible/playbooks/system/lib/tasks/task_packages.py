################################################
__author__ = 'eric sales'
__copyright__ = "Copyright 2017, WildRiver Technologies Inc"
__version__ = "0.2.0"
__maintainer__ = "Larry Sellars"
__email__ = "larry.sellars@wildrivertechnologies.com"
__status__ = "production"
################################################
"""
WebTelemetry BootStrap Task Group: task_packages

    apt_update
    apt_upgrade
    packages(pkg_list)
"""
from fabric.api import *


def apt_update():
    """
    TASK:apt_update - apt-get update
    """
    print "task:  apt-get update starting."
    sudo('apt-get update')


def apt_upgrade():
    """
    TASK:apt_upgrade - apt-get upgrade
    """
    print "task:  apt-get upgrade starting."
    sudo('apt-get upgrade -y')


def packages(pkg_list):
    """
    TASK:packages - apt-get install pkg_list
    yaml config format required

    packages:  [ pkg1, pkg2, ..., pkgN ]
    """
    print "task:  packages starting."
    print "   packages to install: ", pkg_list
    if not pkg_list:
        warn("No packages to install provided.")
    else:
        p = ' '.join(pkg_list)
        sudo('apt-get install -y %s' % p)

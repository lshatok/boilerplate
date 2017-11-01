################################################
__author__ = 'eric sales'
__copyright__ = "Copyright 2017, WebTelemetry US Inc."
__version__ = "0.2.0"
__maintainer__ = "Larry Sellars"
__email__ = "larry.sellars@webtelemetry.us"
__status__ = "production"
################################################
"""
WebTelemetry BootStrap Task Group: task_nodejs

    nodejs  {install_nodejs}
"""
from fabric.api import *


def install_nodejs():
    """
    TASK:nodejs - install nodejs from ppa
    """
    print "task:  nodejs install starting."
    if 'no' == sudo('which nodejs || echo "no"'):
        sudo('add-apt-repository -y ppa:chris-lea/node.js')
        sudo('apt-get update')
        sudo('apt-get install -y nodejs')
    else:
        print "   skipping, nodejs is already installed."

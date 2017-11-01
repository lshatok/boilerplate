################################################
__author__ = 'eric sales'
__copyright__ = "Copyright 2017, WebTelemetry US Inc."
__version__ = "0.2.0"
__maintainer__ = "Larry Sellars"
__email__ = "larry.sellars@webtelemetry.us"
__status__ = "production"
################################################
"""
WebTelemetry BootStrap Task Group: task_redis

    data_collector  {install_redis_server}
"""
from fabric.api import *


def install_redis_server():
    """
    TASK:data_collector - install redis-server from ppa:rwky
    """
    print "task:  data_collector installation started."
    # check if redis is already installed #
    if 'no' == sudo('which redis-server || echo "no"'):
        # check if we need to update kernel settings
        if 'no' == sudo('[ $(cat /etc/sysctl.conf | grep "^vm.overcommit_memory") ] || echo "no"'):
            print "   updating sysctl.conf"
            sudo('echo "vm.overcommit_memory = 1" >> /etc/sysctl.conf')
            sudo('sysctl -p')
        print "   installing any required packages"
        sudo('apt-get install -y python-software-properties software-properties-common')
        print "   updating repository"
        sudo('add-apt-repository -y ppa:rwky/redis')
        sudo('apt-get update')
        print "   apt-get installing redis-server"
        sudo('apt-get install -y redis-server')
        print "  starting redis-server"
        sudo('service redis-server status || service redis-server start')
    else:
        print "  skipping, redis-server already installed."

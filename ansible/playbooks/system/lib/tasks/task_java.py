################################################
__author__ = 'eric sales'
__copyright__ = "Copyright 2017, WildRiver Technologies Inc"
__version__ = "0.2.0"
__maintainer__ = "Larry Sellars"
__email__ = "larry.sellars@wildrivertechnologies.com"
__status__ = "production"
################################################
"""
WebTelemetry BootStrap Task Group: task_java

    java7  {oracle_java7}
"""
from fabric.api import *


def oracle_java7():
    """
    TASK:java7 - install Java7 using oracle-java7-installer
    """
    print "task:  installing Java7"
    if 'no' == sudo('[ -d "{{ java.home }}" ] || echo "no"'):
        sudo('apt-get install -y python-software-properties software-properties-common')
        print "   adding repository."
        sudo('add-apt-repository -y ppa:webupd8team/java')
        print "   starting apt-get update"
        sudo('apt-get update')
        sudo('apt-get install -y debconf-utils')
        ## This command automatically accepts Oracle's license agreement ##
        print "   starting java7 install"
        sudo('echo oracle-java7-installer shared/accepted-oracle-license-v1-1 select true | \
                /usr/bin/debconf-set-selections')
        sudo('apt-get install -y oracle-java7-installer')
    else:
        print "   skipping: java7 already installed."

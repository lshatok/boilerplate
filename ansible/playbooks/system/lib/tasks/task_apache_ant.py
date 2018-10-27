################################################
__author__ = "eric sales"
__copyright__ = "Copyright 2017, WildRiver Technologies Inc"
__version__ = "0.2.0"
__maintainer__ = "Larry Sellars"
__email__ = "larry.sellars@wildrivertechnologies.com"
__status__ = "production"
################################################
"""
WebTelemetry BootStrap Task Group: task_apache_ant

"""
from fabric.api import *


def apache_ant():
    """
    TASK:apache_ant - install apache ant
    """
    ant_ver = 'apache-ant-1.9.4-bin.tar.gz'
    unzipped_ver = 'apache-ant-1.9.4'
    # dl_url = 'https://s3-us-west-2.amazonaws.com/com.webtelemetry().software-repo.public/apache-ant/%s' % ant_ver
    dl_url = 'http://mirror.nexcess.net/apache//ant/binaries/%s' % ant_ver
    # http://mirror.nexcess.net/apache//ant/binaries/apache-ant-1.9.4-bin.tar.gz
    install_path = '/usr/local/apache'
    bin_path = '/usr/local/apache-ant/bin'

    print "task:  ant install"
    if 'no' == sudo('[ -d %s ] || echo "no"' % bin_path):
        if 'no' == sudo('[ -d %s ] || echo "no"' % install_path):
            sudo('mkdir -p %s' % install_path)
        print "   downloading install files"
        with cd(install_path):
            sudo('wget %s' % dl_url)
            sudo('tar zxf %s && rm %s' % (ant_ver, ant_ver))
        sudo('cd /usr/local && ln -s apache/%s apache-ant' % unzipped_ver)

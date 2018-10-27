################################################
__author__ = 'eric sales'
__copyright__ = "Copyright 2017, WildRiver Technologies Inc"
__version__ = "0.2.0"
__maintainer__ = "Larry Sellars"
__email__ = "larry.sellars@wildrivertechnologies.com"
__status__ = "production"
################################################
"""
WebTelemetry BootStrap Task Group: task_influxdb

    influxdb_server
"""
from fabric.api import *


def influxdb_server():
    """
    TASK:influxdb_server - install influxdb from influxdb.com
    """
    # Check if influxdb is already installed
    if 'no' == sudo('which influxdb-server >> /dev/null 2&>1 || echo "no"'):
        # Check if /etc/hosts has already been updated
        #  - this fix is for ec2 classic dynamic allocations but useful for vpc too
        _hostname = sudo('hostname -s')
        if _hostname and 'no' == sudo('$(grep %s /etc/hosts | grep 127.0.0.1) || echo "no"' % _hostname):
            sudo("sed -i '/127.0.0.1/s/$/ %s/' /etc/hosts" % _hostname)

        print "Installing influxdb server"
        # update sources.list if necessary #
        sources_content = "deb http://www.influxdb.com/debian/ testing main"
        if 'no' == sudo('[ $(cat /etc/apt/sources.list | grep "^%s") ] || echo "no"' % sources_content):
            print "   updating sources.list repo"
            sudo('echo "%s" >> /etc/apt/sources.list' % sources_content)
        with cd('/tmp'):
            print "   installing influxdb signing key"
            sudo('wget http://www.influxdb.com/influxdb-signing-key-public.asc')
            sudo('apt-key add influxdb-signing-key-public.asc && rm /tmp/influxdb-signing-key-public.asc')
        sudo('apt-get update')
        print "   apt-get installing influxdb-server"
        sudo('apt-get install -y influxdb-server')
        rbf = "/etc/default/influxdb-server"
        if 'no' == sudo('[ -f %s ] && [[ $(cat %s | grep "^ulimit -n 2048") ]] || echo "no"' % (rbf, rbf)):
            print "   updating limits"
            sudo('echo "ulimit -n 2048" >> %s' % rbf)
        # installing plugins
        print "   installing plugins"
        sudo('influxdb-plugins enable influxdb_management')
        print "   restarting influxdb-server"
        sudo('sleep 5 && service influxdb-server restart')
    else:
        print "   skipping, influxdb-server already installed."

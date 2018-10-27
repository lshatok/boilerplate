################################################
__author__ = 'eric sales'
__copyright__ = "Copyright 2017, WildRiver Technologies Inc"
__version__ = "0.2.0"
__maintainer__ = "Larry Sellars"
__email__ = "larry.sellars@wildrivertechnologies.com"
__status__ = "production"
################################################
"""
WebTelemetry BootStrap Task Group: task_newrelic

    newrelic_hostagent(nr_license)
"""
from fabric.api import *


def newrelic_hostagent(nr_config):
    """
    TASK:newrelic_hostagent - install new relic host agent
    yaml config requirement:

    newrelic_hostagent:
        license: <new relic license>
    """
    nr_license = nr_config['license']
    print "task:  new relic host install started."
    # check if NR sysmond is already installed #
    if sudo('[ -f /usr/sbin/nrsysmond ] || echo "no"') != 'no':
        print "   skipping.. NewRelic host sysmond is already installed."
        sudo('/etc/init.d/newrelic-sysmond restart')
        return
    # update sources.list if necessary #
    sources_content = "deb http://apt.newrelic.com/debian/ newrelic non-free"
    if 'no' == sudo('[ $(cat /etc/apt/sources.list | grep "^%s") ] || echo "no"' % sources_content):
        print "   updating sources.list"
        sudo('echo "%s" >> /etc/apt/sources.list' % sources_content)
        print "   adding New Relic GPG key"
        sudo('wget -O- https://download.newrelic.com/548C16BF.gpg | apt-key add -')
        sudo('apt-get update')
    print "   apt-get installing new relic sysmond"
    sudo('apt-get install newrelic-sysmond')
    print "   installing lic key"
    sudo('nrsysmond-config --set license_key=%s' % nr_license)
    print "   starting sysmond"
    sudo('/etc/init.d/newrelic-sysmond restart')

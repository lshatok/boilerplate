__author__ = "eric sales"
__copyright__ = "Copyright 2017, WildRiver Technologies Inc"
__version__ = "0.2.0"
__maintainer__ = "Larry Sellars"
__email__ = "larry.sellars@wildrivertechnologies.com"
__status__ = "production"
"""
WebTelemetry BootStrap Task Group: task_aws

    aws_update_dhclient: check if west region and if dhclient.conf needs to be updated

    fabric sudo commands (and hbase) fail if host is not resolvable
"""

from fabric.api import *


def aws_update_dhclient():
    """
    TASK: aws_fix_dhclient - check if dhclient needs updating
    """
    print "task: checking if dhclient.conf needs updating.."
    if 'not_aws' == run('[ -f /usr/bin/ec2metadata ] || echo "not_aws"'):
        print " .. not an aws instance"
        return

    if 'fixit' == run('host $(hostname) 2>&1 >> /dev/null || echo "fixit"'):
        if 'us-west-2' == run('host $(hostname).us-west-2.compute.internal 2>&1 >> /dev/null && echo "us-west-2"'):
            # check if us-west-2 already exists
            if 'update' == run('grep us-west-2.compute.internal /etc/dhcp/dhclient.conf || echo "update"'):
                print "  .. updating for us-west-2"
                sudo("""echo 'supersede domain-name "us-west-2.compute.internal";' >> /etc/dhcp/dhclient.conf""")
            else:
                print " .. already updated."
                # elif 'ec2' == run('host $(hostname).ec2.internal 2>&1 >> /dev/null || echo "ec2')
                #    print "  ..updating for ec.internal"
                #    sudo("""echo 'supersede domain-name "ec2.internal";' >> /etc/dhcp/dhclient.conf""")

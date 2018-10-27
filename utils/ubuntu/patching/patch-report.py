#!/usr/bin/env python

__author__ = "eric sales"
__copyright__ = "Copyright 2017, WildRiver Technologies Inc"
__version__ = "0.2.0"
__maintainer__ = "Larry Sellars"
__email__ = "larry.sellars@wildrivertechnologies.com"
__status__ = "production"
"""
Patch Report
  display available patch and security patches on each system

Usage:
   patch-report.py <hosts.yml> (or -H <host(s)>
   (hosts comma separated)

"""
import sys
import yaml
from fabric.api import *

USAGE = "patch-report.py <yaml_file> (or -H <host(s) comma spearated>)"


# flow:
#  get cli args
#  get hostlist from yml file or cli
#  check ssh access
#  read patching, host info
#  print report

class HostInfo:
    def __init__(self, ip):
        self.ip = ip
        self.host = ''
        self.fab_error = None
        self.fab_test = None
        self.package_updates = 'Unknown'
        self.security_updates = 'Unknown'
        self.sudo_access = 'Unknown'
        self.linux_distro = None
        self.ubuntu_rel = None

    def test_fabric(self):
        try:
            with settings(hide('everything'), host_string=self.ip, warn_only=True, timeout=3):
                run('echo')
                try:
                    sudo('echo')
                except Exception as e:
                    self.sudo_access = 'fail'
                else:
                    self.sudo_access = 'pass'
        except Exception as e:
            self.fab_error = e
            self.fab_test = 'fail'

    def update_info(self):
        try:
            with settings(hide('everything'), host_string=self.ip, warn_only=True, timeout=3):
                _out = run('[ -f /usr/lib/update-notifier/apt-check ] && /usr/lib/update-notifier/apt-check',
                           shell=False)
                if _out:
                    self.package_updates = _out.split(';')[0]
                    self.security_updates = _out.split(';')[1]
                self.linux_distro = run('[ -f /etc/lsb-release ] && . /etc/lsb-release && echo $DISTRIB_ID',
                                        shell=False)
                if self.linux_distro == 'Ubuntu':
                    self.ubuntu_rel = run('[ -f /etc/lsb-release ] && . /etc/lsb-release && echo $DISTRIB_DESCRIPTION',
                                          shell=False)
        except Exception as e:
            self.fab_error = e

    def get_aws_info(self):
        try:
            with settings(hide('everything'), host_string=self.ip, warn_only=True, timeout=3):
                is_aws = run('[ -f /usr/bin/ec2metadata ] && /usr/bin/ec2metadata --availability-zone', shell=False)
                if is_aws:
                    self.avail_zone = is_aws
                    self.instance_type = run('/usr/bin/ec2metadata --instance-type', shell=False)
                    self.instance_id = run('/usr/bin/ec2metadata --instance-id', shell=False)
                    self.public_ip = run('/usr/bin/ec2metadata --public-ipv4', shell=False)
        except Exception as e:
            self.fab_error = e


def print_host_info(info_dict):
    """
    process from yaml info
    """
    import string
    host_objlist = []
    HEADER = "ip,host,packages,security,sudo"
    LINE = string.Template("$IP,$HOST,$PKGS,$SECPKGS,$SUDO")
    print HEADER

    for h in info_dict:
        printDict = {'PKGS': 'fail', 'SECPKGS': 'fail'}
        Hinfo = HostInfo(info_dict[h])
        Hinfo.host = h
        printDict['IP'] = Hinfo.ip
        printDict['HOST'] = Hinfo.host
        Hinfo.test_fabric()
        if not Hinfo.fab_error:
            Hinfo.update_info()
            printDict['PKGS'] = Hinfo.package_updates
            printDict['SECPKGS'] = Hinfo.security_updates
        printDict['SUDO'] = Hinfo.sudo_access
        host_objlist.append(Hinfo)
        print LINE.substitute(printDict)
    return host_objlist


if __name__ == '__main__':
    hostlist = []
    host_objs = []
    try:
        yf = sys.argv[1]
        if yf == '-H':
            hostlist = sys.argv[2].split(',')
    except IndexError:
        print "missing Args error"
        print USAGE
        sys.exit(1)

    if not hostlist:
        try:
            with open(yf, 'r') as f:
                yload = yaml.load(f)
        except IOError as e:
            print "yaml file open error: ", e
            sys.exit(1)

        host_objs = print_host_info(yload)

    else:
        print "hostlist: ", hostlist

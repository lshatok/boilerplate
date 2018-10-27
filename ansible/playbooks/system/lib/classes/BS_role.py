################################################
__author__ = 'eric sales'
__copyright__ = "Copyright 2017, WildRiver Technologies Inc"
__version__ = "0.2.0"
__maintainer__ = "Larry Sellars"
__email__ = "larry.sellars@wildrivertechnologies.com"
__status__ = "production"
################################################
"""
WebTelemetry BootStrap Class group:  BS_role

    BootStrapRole(role_name, role_path, config_dict)
"""
import os
from fabric.api import *

bootstrap_roles_file = '/etc/bootstrap.roles'


class BootStrapRole:
    def __init__(self, role_name, role_path, config_dict):
        self.role_name = role_name
        self.role_path = role_path
        self.file_repo = os.path.join(role_path, 'files')
        self.config_dict = config_dict
        self.tasks = config_dict.get('tasks')
        self.required_roles = config_dict.get('required_roles')

    def get_installed_roles(self):
        found = sudo('[ -f %s ] && cat %s || echo ""' % (bootstrap_roles_file, bootstrap_roles_file))
        return found.split()

    def get_ip_addr(self, interface):
        ip_addr = sudo("ifconfig %s | grep 'inet addr' | awk '{print $2}' | cut -d: -f2" % interface)
        return ip_addr

    def append_role_file(self):
        if not self.role_name in self.get_installed_roles():
            sudo('echo %s >> %s' % (self.role_name, bootstrap_roles_file))

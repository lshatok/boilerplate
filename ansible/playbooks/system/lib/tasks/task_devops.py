__author__ = 'Leo Shatokhin'

from fabric.api import *


def role_exists(role_name, file_name):
    """ Check if role has already been processed
    @param role_name:
    @param file_name:
    @return:
    """
    role_processed = sudo('[ -f %s ] && grep "^%s$" %s && echo "yes" || echo "no"' % (file_name, role_name, file_name))
    if role_processed == 'yes':
        return True
    else:
        return False


def append_role(role_n, file_n):
    """ Append role to role list file <file_n>
    @param role_n:
    @param file_n:
    @return:
    """
    with hide('output', 'running'):
        sudo('[ -f %s ] && grep "^%s$" %s || echo "%s" >> %s' % (file_n, role_n, file_n, role_n, file_n))


def file_exists(file_name):
    """ Check if <file_name> exists
    @param file_name:
    @return: boolean
    """
    file_found = sudo('[ -f %s ] && echo "True" || echo "False"' % file_name)
    if file_found == "True":
        return True
    else:
        return False


def path_exists(path_name):
    """
    @param path_name: Check if <path_name> exists
    @return:
    """
    path_found = sudo('[ -f %s ] && echo "True" || echo "False"' % path_name)
    if path_found == "True":
        return True
    else:
        return False

from fabric.api import *
from fabric.exceptions import NetworkError
from fabric.state import output

output.running = False
output.output = False
output.warnings = False
env.warn_only = True

import re


def test_access():
    """
    Test fabric Network connection
    """
    access = ()
    try:
        run('echo "connected"')
    except NetworkError as e:
        access = (False, e.message)
        return access
    else:
        return (True, '')


@task
def info_ubuntu_release():
    """
    Get the version of Ubuntu
    """
    ubuntu = {}
    _test = test_access()
    if not _test[0]:
        ubuntu['error'] = _test[1]
    else:
        _distro = run('[ -f /etc/lsb-release ] && . /etc/lsb-release && echo $DISTRIB_ID', shell=False)
        _release = run('[ -f /etc/lsb-release ] && . /etc/lsb-release && echo $DISTRIB_DESCRIPTION', shell=False)

        if _distro and _release:
            ubuntu['linux'] = _distro
            ubuntu['release'] = _release
        else:
            ubuntu['error'] = 'linux version not Ubuntu'
    print " {'%s' : %s } " % (env.host, ubuntu)


@task
def exec_apt_upgrade():
    """
    Apply system and security patches
    """
    retdict = {}
    print "%s => executing apt-get update && dist-upgrade" % env.host
    try:
        sudo('apt-get update', shell=False)
        _out = sudo('apt-get -y dist-upgrade', shell=False)
        # _out = sudo('apt-get -y openssl', shell=False)
        _outval = re.split('\n|\r', _out)
        outval = [s for s in _outval if 'upgraded' in s and 'installed' in s and 'remove' in s]
        retdict['results'] = '\n'.join(map(str, outval))
    except NetworkError as e:
        retdict['error'] = e.message

    print " {'%s' : %s } " % (env.host, retdict)


@task
def exec_apt_upgrade_openssl():
    """
    Upgrade OpenSSL (again)
    """
    retdict = {}
    print "%s => executing apt-get update && install openssl" % env.host
    try:
        sudo('apt-get update', shell=False)
        _out = sudo('apt-get -y install openssl', shell=False)
        _outval = re.split('\n|\r', _out)
        outval = [s for s in _outval if 'Setting' in s and 'up' in s and 'openssl' in s]
        retdict['results'] = '\n'.join(map(str, outval))
    except NetworkError as e:
        retdict['error'] = e.message

    print " {'%s' : %s } " % (env.host, retdict)


@task
def info_updates_avail():
    """
    Report available updates
    """
    retdict = {}
    try:
        _out = run('[ -f /usr/lib/update-notifier/apt-check ] && /usr/lib/update-notifier/apt-check', shell=False)
        if _out:
            retdict['pkg_updates'] = _out.split(';')[0]
            retdict['sec_updates'] = _out.split(';')[1]
        else:
            retdict['error'] = 'Ubuntu apt-check not found'
    except NetworkError as e:
        retdict['error'] = e.message

    print "{'%s' : %s } " % (env.host, retdict)


@task
def exec_sudo_cmd(command):
    """
    execute sudo command:'COMMAND'
    """
    retdict = {}
    try:
        retdict['command'] = command
        # retdict['result'] = sudo('%s > /dev/null 2>&1 && echo "done" || echo "failed"' % command, shell=False)
        retdict['result'] = sudo('%s' % command, shell=False)
    except NetworkError as e:
        retdict['error'] = e.message

    print "{ '%s':  %s  }" % (env.host, retdict)


@task
def exec_patch_dhclient():
    """
    Add ec2.internal to dhclient.conf supersede domain-name
    """
    # check if localhost name resolves
    # check if host.ec2.internal resolves
    # check if supersede is already set
    # update dhclient.conf if needed

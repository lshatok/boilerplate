from fabric.api import *
from fabric.exceptions import NetworkError


@task
def exec_install_showver():
    """
    apt-get install apt-show-versions
    """
    retdict = {}
    try:
        sudo('dpkg -s apt-show-versions || apt-get update && apt-get install -y apt-show-versions')
        retdict['apt-show-versions'] = 'done'
    except NetworkError as e:
        retdict['error'] = e.message

    print "%s => " % env.host, retdict


@task
def info_openssl_version():
    """
    Get the version of OpenSSL installed
    """
    retdict = {}
    try:
        retdict['openssl'] = sudo('[ -f /usr/bin/apt-show-versions ] && /usr/bin/apt-show-versions openssl',
                                  shell=False)
        if retdict['openssl'] == '':
            retdict['openssl'] = sudo('/usr/bin/dpkg -s openssl | grep -m 1 Version', shell=False)
    except NetworkError as e:
        retdict['error'] = e.message

    print "%s => " % env.host, retdict


@task
def exec_update_openssl():
    """
    apt-get upgrade openssl
    """
    retdict = {}
    try:
        retdict['before'] = sudo('/usr/bin/dpkg -s openssl | grep -m 1 Version', shell=False)
        print '%s exec - apt-get update' % env.host
        sudo('apt-get update', shell=False)
        sudo('apt-get upgrade -y openssl', shell=False)
        retdict['after'] = sudo('/usr/bin/apt-show-versions openssl', shell=False)
    except NetworkError as e:
        retdict['error'] = e.message

    print "%s => " % env.host, retdict

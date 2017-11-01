#!/usr/bin/env python
__author__ = 'Leo Shatokhin'

import os
import sys
from fabric.api import *

"""
    create_acct script created demonstrating how to use Fabric calls in a python script
    Pulls user keys from watt.  Then Creates users with keys from a list.

    shell output
    os.getenv
    env.settings:  key_filename, host_string, sudo_user

    Pros: can use a single python command to perform actions across different targets
    Cons: performance, more complex to parallelize

"""

## SSN OGE Env ##
ipList = ['10.18.0.117', '10.18.0.121', '10.18.0.122', '10.18.0.124', '10.18.0.132', '10.18.0.155',
          '10.18.0.156', '10.18.0.157', '10.18.0.164', '10.18.0.167', '10.18.0.168', '10.18.0.173', '10.18.0.174',
          '10.18.0.175', '10.18.0.176', '10.18.0.177', '10.18.0.181', '10.18.0.184', '10.18.0.187', '10.18.0.189',
          '10.18.0.29', '10.18.0.36', '10.18.0.75', '10.18.0.78', '10.18.0.90', '10.18.0.92']

watt = '192.168.70.30'

agUsers = {'gordon': 'gordon cavendish',
           'khushwant': 'Khushwant Jhaj',
           'vijay': 'Vijay Bhat',
           'sourav': 'Sourav Dey',
           'austin': 'Austin Park',
           'mark': 'Mark Chew'}

agSudoers = "gordon"


def getPubKey(User):
    """
    Returns the first ssh key listed in authorized_keys or authorized_keys2
    """
    with settings(key_filename='/Users/eric/.ssh/id_rsa.pub', host_string=watt):
        with cd('/home/%s/.ssh' % (User)):
            auth_keyfile = sudo(
                '( [ -f authorized_keys ] && echo "authorized_keys" ) || ( [ -f authorized_keys2 ]  && echo "authorized_keys2" )')
            key = sudo('head -1 %s' % auth_keyfile)

    return key


def addUser(User):
    """
    Create user if it doesn't already exist
    """
    # check if user already exists #
    user_exists = run('id -u %s >/dev/null 2>&1 || echo "no"' % (User))
    if user_exists == "no":
        sudo('useradd -m -c "%s" -s /bin/bash %s' % (agUsers[User], User))
    else:
        print "[Info] User '%s' already exists on host '%s'" % (User, env.host_string)


def addPubKey(User, pubkey):
    """
    Create the .ssh dir and push the pubkey
    """
    with cd('~%s' % (User)):
        sudo('mkdir -p .ssh && chmod 700 .ssh', user=User)
        # add key if it doesn't already exist #
        _hazKey = 'no'
        _hazFile = sudo("[ -f .ssh/authorized_keys ] && echo 'yes' || echo 'no'", user=User)
        if _hazFile == 'yes':
            # authorized_keys exist - check if the key already exists
            _hazKey = sudo("grep '%s' .ssh/authorized_keys >/dev/null 2>&1 && echo 'yes'" % (pubkey), user=User)
        if _hazKey == 'no':
            sudo("echo '%s' >> .ssh/authorized_keys" % (pubkey), user=User)
        else:
            print "[Info] User '%s' key already exists on host '%s'" % (User, env.host_string)


def addSudoers(User_String):
    """
    Add Suders list with User_String users
    """
    SudoerString = """User_Alias DEVOPS = %s
DEVOPS  ALL=NOPASSWD: ALL""" % User_String
    _hazSudoers = sudo('[ -f /etc/sudoers.d/webtelemetry-devops ] && echo "yes" || echo "no"')
    # We wont overwrite anything until we can verify & compare the contents
    if _hazSudoers == "no":
        sudo('echo "%s" >> /etc/sudoers.d/webtelemetry-devops' % SudoerString)
        sudo('chmod 440 /etc/sudoers.d/webtelemetry-devops')
    else:
        print "[Info] webtelemetry-devops Sudoers file already exists."


if __name__ == "__main__":
    if os.getenv('FAB_USER'):
        env.user = os.getenv('FAB_USER')
    else:
        print "[Error] FAB_USER not set.  To fix run: 'export FAB_USER=ubuntu'"
        sys.exit(1)

    if os.getenv('FAB_KEY_FILENAME'):
        env.key_filename = os.getenv('FAB_KEY_FILENAME')
    else:
        print "[Error] FAB_KEY_FILENAME not set.  To fix run: 'export FAB_KEY_FILENAME=<path_to_pemfile>"
        sys.exit(1)

    ## create dict of user_accts with keys ##
    agUserKeys = {}
    sys.stdout.write("Getting User keys from 'watt': ")
    sys.stdout.flush()
    for agU in agUsers.keys():
        sys.stdout.write('.')
        sys.stdout.flush()
        with hide('running', 'output'):
            agUserKeys[agU] = getPubKey(agU)
    print '[done]'

    # debug / test
    # with settings(host_string = '10.18.0.29'):
    #    addUser('Leo Shatokhin')
    #    addPubKey('Leo Shatokhin',agUserKeys['Leo Shatokhin'])
    #    addSudoers(agSudoers)

    for h in ipList:
        print "-- host: %s -----" % (h)
        with settings(hide('running', 'output'), host_string=h):
            for acct in agUserKeys.keys():
                sys.stdout.write("Adding user '%s' to host '%s'.." % (acct, h))
                sys.stdout.flush()
                addUser(acct)
                sys.stdout.write(" Adding keys..")
                sys.stdout.flush()
                addPubKey(acct, agUserKeys[acct])
                print "[done]"
            print "Adding webtelemetry-sudoers..",
            addSudoers(agSudoers)
            print "[done]"
        print "____________________________\n"

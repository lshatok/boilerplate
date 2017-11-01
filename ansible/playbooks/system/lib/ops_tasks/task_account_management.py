################################################
__author__ = 'eric sales'
__copyright__ = "Copyright 2017, WebTelemetry US Inc."
__version__ = "0.2.0"
__maintainer__ = "Larry Sellars"
__email__ = "larry.sellars@webtelemetry.us"
__status__ = "production"
################################################
"""
WebTelemetry Task Group: task_account_management
To Be Used independently with 'manage-acct.py'

"""
from fabric.api import *


def group_add(group_list=()):
    """
    Add Groups from group_list
    """
    for g in group_list:
        if sudo('[[ $(cat /etc/group | cut -d: -f1 | grep "^%s$") ]] || echo "no"' % g) == 'no':
            print "Creating group: %s" % g
            sudo('groupadd %s' % g)


def user_add(acct_name, acct_dict):
    """
    TASK:user_add - manage user accounts

    yaml config format
    users:
        defaults:   # set optional defaults
                group: wtgroup
                shell: /bin/bash
                source_profile:
                    - /WT/profiles/profile-webtelemetry.sh
        <account_name>:
                uid: <uid_number>
                group:  <group>
                groups: [ group1, .., groupN ]
                home:  <path>
                email: <email address>  # used for GIT_AUTHOR_EMAIL
                comment: Full Name, or Description
                pubkey:
                    - ssh-rsa <HASH>
                    - # add multiple pub keys if needed #
    """
    # Defaults if none set
    default_shell = '/bin/bash'

    # we pass one user dictionary at a time
    details = acct_dict

    uid = details.get('uid')
    shell = details.get('shell', default_shell)
    home = details.get('home', '/home/%s' % acct_name)
    group = details.get('group')
    groups = details.get('groups')
    email = details.get('email', '%s@webtelemetry.us' % acct_name)
    comment = details.get('comment', acct_name)
    source_profile = details.get('source_profile')
    public_keys = details.get('pubkey')
    create_gitconfig = details.get('create_gitconfig', True)
    create_bash_profile = details.get('create_bash_profile', True)

    user_add_args = '-m'
    if uid:
        user_add_args += ' -u %s' % uid
    if groups:
        user_add_args += ' -G %s' % ','.join(groups)
    user_add_args += ' -d %s -s %s -c "%s" -g %s' % (home, shell, comment, group)

    # create or modify account #
    if 'no' == sudo('[[ $(cat /etc/passwd | cut -d: -f1 | grep "^%s$") ]] || echo "no"' % acct_name):
        print "  creating user acct: %s" % acct_name
        _cmd = 'useradd'
        new_user = True
    else:
        print "  User exists, modifying acct: %s" % acct_name
        _cmd = 'usermod'
        new_user = False
    sudo("%s %s %s" % (_cmd, user_add_args, acct_name))

    # create gitconfig #
    if create_gitconfig:
        if 'no' == sudo('[ -f %s/.gitconfig ] || echo "no"' % home):
            print "  initializing .gitconfig file"
            sudo('echo "[user]\n   name = %s\n   email = %s" > %s/.gitconfig' % (comment, email, home))
            sudo('chown %s:%s %s/.gitconfig' % (acct_name, group, home))

    # create bash_profile.j2 #
    if create_bash_profile:
        if 'no' == sudo('[ -f %s/.bash_profile.j2 ] || echo "no"' % home):
            print "  creating .bash_profile.j2"
            _contents = """[ -n "$BASH_VERSION" ] && [ -f "$HOME/.bashrc" ] && . "$HOME/.bashrc" """
            sudo("echo '### .bash_profile.j2 created via do-bootstrap ###' > %s/.bash_profile.j2" % home,
                 user=acct_name)
            sudo("echo '%s' >> %s/.bash_profile.j2" % (_contents, home), user=acct_name)

    # add profiles to source #
    if source_profile:
        for file_to_source in source_profile:
            if 'no' == sudo('grep -q %s %s/.bash_profile.j2 || echo "no"' % (file_to_source, home)):
                print "  adding source %s to .bash_profile.j2" % file_to_source
                _line = '[ -f %s ] && . %s' % (file_to_source, file_to_source)
                sudo("echo '%s' >> %s/.bash_profile.j2" % (_line, home), user=acct_name)

    create_ssh_path(acct_name)
    user_pubkeys(acct_name, public_keys)


def create_ssh_path(acct):
    """
    Create .ssh directory for user acct in home
    @param acct:
    @return:
    """
    # create .ssh directory #
    acct_home = sudo('grep ^%s /etc/passwd | cut -d: -f6' % acct)
    if acct_home and 'no' == sudo('[ -d %s/.ssh ] || echo "no"' % acct_home):
        print "Creating .ssh directory for %s" % acct
        sudo('mkdir -p %s/.ssh && chmod 700 %s/.ssh' % (acct_home, acct_home), user=acct)


def user_pubkeys(acct, pubkey_list=[]):
    """
    create authorized_keys file from pubkey_list
    any existing files will be overwritten
    """
    if not pubkey_list:
        return
    with cd('~%s' % acct):
        sudo('su -l %s -c \"mkdir -p .ssh && chmod 700 .ssh\"' % acct)
        sudo("""su -l %s -c 'echo "## Authorized Keys managed via WebTelemetry Fabric $(date +%%D) ##" > \
                .ssh/authorized_keys'""" % acct)
        for pk in pubkey_list:
            sudo("""su -l %s -c 'echo "%s" >> .ssh/authorized_keys'""" % (acct, pk))

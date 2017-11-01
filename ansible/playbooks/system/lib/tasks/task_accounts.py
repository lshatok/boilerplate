################################################
__author__ = 'eric sales'
__copyright__ = "Copyright 2017, WebTelemetry US Inc."
__version__ = "0.2.0"
__maintainer__ = "Larry Sellars"
__email__ = "larry.sellars@webtelemetry.us"
__status__ = "production"
################################################
"""
WebTelemetry BootStrap Task Group: task_accounts

    groups(group_list)
    accounts(accts_dict)

 - supportive functions
    create_ssh_path

"""
from fabric.api import *


def groups(group_list=()):
    """
    TASK:groups - create groups

    yaml config format
    groups:
        - group1
        - group2

    @param group_list:
    """
    print "task:  creating groups started.."
    for g in group_list:
        if sudo('$(grep -q "^%s:" /etc/group) || echo "no"' % g) == 'no':
            print "Creating group: %s" % g
            sudo('groupadd %s' % g)
        else:
            warn('skipping : group %s already exists.' % g)


def accounts(accts_dict):
    """
    TASK:accounts - create system account

    yaml config format
    accounts:
        <account_name>:
                uid :  <uid_number>,
                shell:  /bin/bash,
                group:  {{ product.admin }},
                groups:  [ group1, group2 ]
                comment:  Account Dexcription,
                home:  <path>
                email:  <email to associate - used for git config>
                add_profile:
                    - path/for/file/to/source
    """
    print "task:  creating accounts started.."
    for acct in accts_dict:
        details = accts_dict[acct]
        # define defaults
        uid = details.get('uid')
        shell = details.get('shell', '/bin/bash')
        home = details.get('home', '/home/%s' % acct)
        group = details.get('group', acct)
        groups = details.get('groups', [])
        email = details.get('email', '%s@webtelemetry.us' % acct)
        comment = details.get('comment', acct)
        add_profiles_list = details.get('add_profile', [])

        user_add_args = '-m'
        if uid:
            user_add_args += ' -u %s' % uid
        if groups:
            user_add_args += ' -G %s' % ','.join(groups)
        user_add_args += ' -d %s -s %s -c "%s" -g %s' % (home, shell, comment, group)

        # create or modify account #
        if 'no' == sudo('[[ $(cat /etc/passwd | cut -d: -f1 | grep "^%s$") ]] || echo "no"' % acct):
            print "  creating user acct: %s" % acct
            _cmd = 'useradd'
        else:
            print "  User exists, modifying acct: %s" % acct
            _cmd = 'usermod'
        sudo("%s %s %s" % (_cmd, user_add_args, acct))

        # create gitconfig #
        if 'no' == sudo('[ -f %s/.gitconfig ] || echo "no"' % home):
            print "  initializing .gitconfig file"
            sudo('echo "[user]\n   name = %s\n   email = %s" > %s/.gitconfig' % (comment, email, home))
            sudo('chown %s:%s %s/.gitconfig' % (acct, group, home))

        # create bash_profile.j2 #
        if 'no' == sudo('[ -f %s/.bash_profile.j2 ] || echo "no"' % home):
            print "  creating .bash_profile.j2"
            _contents = """[ -n "$BASH_VERSION" ] && [ -f "$HOME/.bashrc" ] && . "$HOME/.bashrc" """
            sudo("echo '### .bash_profile.j2 created via do-bootstrap ###' > %s/.bash_profile.j2" % home, user=acct)
            sudo("echo '%s' >> %s/.bash_profile.j2" % (_contents, home), user=acct)

        # add profiles to source #
        if add_profiles_list:
            for file_to_source in add_profiles_list:
                if 'no' == sudo('grep -q %s %s/.bash_profile.j2 || echo "no"' % (file_to_source, home)):
                    print "  adding source %s to .bash_profile.j2" % file_to_source
                    _line = '[ -f %s ] && . %s' % (file_to_source, file_to_source)
                    sudo("echo '%s' >> %s/.bash_profile.j2" % (_line, home), user=acct)

        create_ssh_path(acct, home)


def create_ssh_path(acct, home=''):
    """
    Create .ssh directory for user acct in home
    @param acct:
    @param home:
    @return:
    """
    if not home:
        home = '/home/%s' % acct
    # create .ssh directory #
    if 'no' == sudo('[ -d %s/.ssh ] || echo "no"' % home):
        print "Creating .ssh directory for %s" % acct
        sudo('mkdir -p %s/.ssh && chmod 700 %s/.ssh' % (home, home), user=acct)
    else:
        print "  skipping: %s/.ssh already exists." % home


def user_add(accounts_dict):
    """
    TASK:user_add - create user accounts
      ** Another rewrite - to replace accounts **

    yaml config format
    users:
        defaults:   # set optional defaults
                group: wtgroup
                shell: /bin/bash
                source_profile:
                    - /WT/profiles/profile-webtelemetry.sh
                create_gitconfig:  True
                create_bash_profile:  True
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
    print "task:  user accounts started.."

    # read in the defaults #
    details = {}
    # we need a mutable version #
    accts_dict = accounts_dict
    if accts_dict.get('defaults'):
        details = accts_dict.get('defaults')
        # remote the defaults key after we have the details #
        del accts_dict['defaults']

    for acct in accts_dict:
        details.update(accts_dict[acct])
        # create user settings #
        uid = details.get('uid')
        shell = details.get('shell', '/bin/bash')
        home = details.get('home', '/home/%s' % acct)
        acct_group = details.get('group')
        acct_groups = details.get('groups')
        email = details.get('email', '%s@webtelemetry.us' % acct)
        comment = details.get('comment', acct)
        source_profile = details.get('source_profile')
        public_keys = details.get('pubkey')
        create_gitconfig = details.get('create_gitconfig', True)
        create_bash_profile = details.get('create_bash_profile', True)

        user_add_args = '-m'
        if uid:
            user_add_args += ' -u %s' % uid
        if acct_groups:
            user_add_args += ' -G %s' % ','.join(acct_groups)
        user_add_args += ' -d %s -s %s -c "%s" -g %s' % (home, shell, comment, acct_group)

        # create or modify account #
        if 'no' == sudo('$(grep -q "^%s:" /etc/passwd) || echo "no"' % acct):
            print "  creating user acct: %s" % acct
            _cmd = 'useradd'
            new_user = True
        else:
            print "  User exists, modifying acct: %s" % acct
            _cmd = 'usermod'
            new_user = False
        sudo("%s %s %s" % (_cmd, user_add_args, acct))

        # create gitconfig #
        if create_gitconfig:
            if 'no' == sudo('[ -f %s/.gitconfig ] || echo "no"' % home):
                print "  initializing .gitconfig file"
                sudo('echo "[user]\n   name = %s\n   email = %s" > %s/.gitconfig' % (comment, email, home))
                sudo('chown %s:%s %s/.gitconfig' % (acct, acct_group, home))

        # create bash_profile.j2 #
        if create_bash_profile:
            if 'no' == sudo('[ -f %s/.bash_profile.j2 ] || echo "no"' % home):
                print "  creating .bash_profile.j2"
                _contents = """[ -n "$BASH_VERSION" ] && [ -f "$HOME/.bashrc" ] && . "$HOME/.bashrc" """
                sudo("echo '### .bash_profile.j2 created via do-bootstrap ###' > %s/.bash_profile.j2" % home, user=acct)
                sudo("echo '%s' >> %s/.bash_profile.j2" % (_contents, home), user=acct)

        # add profiles to source #
        if source_profile:
            if type(source_profile) == list:
                # Add all sources if there are more than one profile listed
                for file_to_source in source_profile:
                    if 'no' == sudo('grep -q %s %s/.bash_profile.j2 || echo "no"' % (file_to_source, home)):
                        print "  adding source %s to .bash_profile.j2" % file_to_source
                        _line = '[ -f %s ] && . %s' % (file_to_source, file_to_source)
                        sudo("echo '%s' >> %s/.bash_profile.j2" % (_line, home), user=acct)
            else:
                # if its not a list, we can handle a single profile
                if 'no' == sudo('grep -q %s %s/.bash_profile.j2 || echo "no"' % (file_to_source, home)):
                    print "  adding source %s to .bash_profile.j2" % file_to_source
                    _line = '[ -f %s ] && . %s' % (file_to_source, file_to_source)
                    sudo("echo '%s' >> %s/.bash_profile.j2" % (_line, home), user=acct)

        create_ssh_path(acct)
        # only update keys automatically for new users #
        if new_user and public_keys:
            user_pubkeys(acct, public_keys)


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

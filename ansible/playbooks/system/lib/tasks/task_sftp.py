################################################
__author__ = "eric sales"
__copyright__ = "Copyright 2017, WebTelemetry US Inc."
__version__ = "0.2.0"
__maintainer__ = "Larry Sellars"
__email__ = "larry.sellars@webtelemetry.us"
__status__ = "production"
################################################
"""
WebTelemetry BootStrap Task Group: task_sftp

    sftp_server(sftp_configs)

"""
from fabric.api import *


def sftp_server(sftp_configs):
    """
    TASK:sftp_server  - enable sftp server for group
    yaml config format required

    sftp_server:
        group:  sftpgroup
        chroot:  /chroot/path
    """
    sftp_group = sftp_configs['group']
    sftp_chroot = sftp_configs['chroot']
    print "task:  enabling sftp server"
    # check that the sftp groups has already been enabled #
    if 'no' == sudo('grep -q -e "^Match Group %s$" /etc/ssh/sshd_config || echo "no"' % sftp_group):
        sudo('mkdir -p %s' % sftp_chroot)
        sudo('grep -q -e "^%s:" /etc/group || groupadd %s' % (sftp_group, sftp_group))
        sudo("""cat << EOF >> /etc/ssh/sshd_config
Match Group %s
    PasswordAuthentication yes
    ChrootDirectory %s
    AllowTCPForwarding no
    X11Forwarding no
    ForceCommand internal-sftp
EOF""" % (sftp_group, sftp_chroot))
        sudo('service ssh reload')
    else:
        print "  skipping: sftp server for group '%s' already enabled." % sftp_group


def sftp_users(user_configs):
    """
    TASK:sftp_users  - setup sftp users
    yaml config format require

    sftp_users:
        sftpuser1:
            password:  <optional>
            group:  sftpgroup
            home:  /home/sftpuser1   # -> /chroot/path/home/sftpuser1
            chroot:  /chroot/path
            sshkey:  <optional>
        <sftpuser2>:
    """
    sftp_users = user_configs.keys()
    for user in sftp_users:
        password = user_configs[user].get('password')
        group = user_configs[user]['group']
        home = user_configs[user]['home']
        chroot = user_configs[user]['chroot']
        sshkey = user_configs[user].get('sshkey')
        if "no" == sudo('grep -q -e "^%s:" /etc/passwd || echo "no"' % user):
            print "task:  enabling sftp user '%s'" % user
            real_path = chroot + home
            sudo('useradd -g %s -c "sftp user" -d %s -s /sbin/nologin %s' % (group, home, user))
            if password:
                sudo('echo %s:%s | chpasswd' % (user, password))
            if sshkey:
                sudo('mkdir -p %s/.ssh && chmod 700 %s/.ssh && chown %s:%s %s/.ssh' %
                     (real_path, real_path, user, group, real_path))
                sudo('echo "%s" >> %s/.ssh/authorized_keys' % (sshkey, real_path))
                sudo('chown %s:%s %s/.ssh/authorized_keys' % (user, group, real_path))
            sudo('mkdir -p %s' % real_path)
            sudo('mkdir -p %s' % (real_path + '/incoming'))
            sudo('chown %s:%s %s' % (user, group, real_path))
            sudo('chown %s:%s %s' % (user, group, real_path + '/incoming'))
            sudo('chmod 770 %s' % real_path)
            sudo('chmod 770 %s' % (real_path + '/incoming'))
        else:
            print "task:  skipping sftp user '%s'.. already exists" % user

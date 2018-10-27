################################################
__author__ = 'eric sales'
__copyright__ = "Copyright 2017, WildRiver Technologies Inc"
__version__ = "0.2.0"
__maintainer__ = "Larry Sellars"
__email__ = "larry.sellars@wildrivertechnologies.com"
__status__ = "production"
################################################
"""
WebTelemetry BootStrap Task Group: task_system

    reboot {host_reboot}
    directories(paths_dict)  {create_directories}
    files(files_dict, file_repo)  {deploy_files}
    sudoers(file_list, file_repo)  {deploy_sudoers}
    symlinks(symlinks_dict)  {create_symlinks}

 - supportive functions

"""
import os
from fabric.api import *


def host_reboot():
    """
    TASK:reboot - reboot host

    Reboot host and wait 120 secs to come back up
    """
    print "task:  Rebooting Host %s" % env.host
    reboot()


def create_directories(dirs_dict):
    """
    TASK:directories - create directories (mkdir -p)

    yaml config format
    directories:
        /path/to/create:
            owner: <owner>
            group: <group>
            mode: 0755
    """
    print "task:  creating directories starting.."
    for d in dirs_dict:
        d_details = dirs_dict[d]
        perms = '%s:%s' % (d_details['owner'], d_details['group'])
        mode = '%s' % d_details['mode']
        sudo('mkdir -p %s && chown %s %s && chmod %s %s' % (d, perms, d, mode, d))


def deploy_files(files_dict, file_repo):
    """
    TASK:files - create system account

    yaml config format
    files:
        /path/to/deploy/file_name :
            source:  filename_in_files_dir
            owner:  <owner>
            group:  <group>
            mode:  0644
    """
    print "task:  deploying files starting.."
    for f in files_dict:
        print "   deploying file '%s'" % f
        f_details = files_dict[f]
        source_file = os.path.join(file_repo, f_details['source'])
        put(source_file, f, use_sudo=True, mode=f_details['mode'])
        sudo('chown %s:%s %s' % (f_details['owner'], f_details['group'], f))


def deploy_sudoers(file_list, file_repo):
    """
    TASK:sudoers - add sudoers file to /etc/sudoers.d

    yaml config format
    sudoers:
        - <sudoers file in repo>
    """
    print "task:  adding sudoers file(s).."
    for f in file_list:
        source_file = os.path.join(file_repo, f)
        remote_file = os.path.join('/etc/sudoers.d', f)
        tmp_file = os.path.join('/tmp', f)
        put(source_file, tmp_file, use_sudo=True, mode='0440')
        # test sudoers file before installing #
        sudo('chown root:root %s' % tmp_file)
        sudo('visudo -cf %s && mv %s %s' % (tmp_file, tmp_file, remote_file))
        sudo('chmod 0440 %s' % remote_file)


def run_commands(cmds_list):
    """ TASK:run_commands:<batch_name> - run commands from defined tupples

    yaml config format
    run_commands:
        <batch_name>:
            - ( <user>, <working_dir>, <cmd1> )
            - ( <user>, <working_dir>, <cmd2> )
            - ...
    """
    print "task:  running commands from list.."
    for cmd_args in cmds_list:
        sudo('su -l %s -c "cd %s && %s"' % (cmd_args[0], cmd_args[1], cmd_args[2]), shell=True)


def create_symlinks(symlinks_dict):
    """
    TASK:symlinks - create a symbolic link for a file
      symlinks will be created whether the target file exists or not

    yaml config format
    symlinks:
        /path/to/targetfile_or_dir :
            link:  path_or_name_of_link
            path:  <optional>  default is '/' (cd into path first)
            owner: <optional>  default is root
            group: <optional>  default is root
    """
    for s in symlinks_dict:
        s_details = symlinks_dict[s]
        s_link = s_details['link']
        s_path = s_details.get('path', "/")
        s_owner = s_details.get('owner')
        s_group = s_details.get('group')
        if s_owner and s_group: s_owner = '%s:%s' % (s_owner, s_group)
        # check if file or link exists #
        if 'no' == sudo("([ -e %s ] || [ -L %s ]) || echo 'no'" % (s_link, s_link)):
            print "  task: creating symlink"
            with cd(s_path):
                sudo('ln -s %s %s' % (s, s_link))
                if s_owner: sudo("chown -h %s %s" % (s_owner, s_link))
                if s_group: sudo("chgrp -h %s %s" % (s_owner, s_link))
        else:
            print "  skipping.. symlink or file already exists"


def add_to_sudoers(acct_name):
    """
    TASK:add_to_sudoers - add account to sudoers
    """
    sudo('grep -q -e "^%s " /etc/sudoers || echo "%s   ALL=(ALL)  NOPASSWD:ALL" >> /etc/sudoers' %
         (acct_name, acct_name))

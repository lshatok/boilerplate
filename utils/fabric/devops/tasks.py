"""
Devops Fabric tasks
"""
from fabric.api import *

ANSIBLE_KEY = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDJECzUDI/g1DWV2NOc0LkXXu0sK7wRZOQm4dO8s6Bn0hgQuKXVpLtz7LDjkaBkEXT8eYhowDL5a6w+emrvDqWt4nKvEtBVM1g08PidPqKWwBbNL6OXsuxTQHxuxxuGfWPK42QStNCRffOnMBFh1EZnOFovufF6fGmq4N9y0lXlQ4USu8RPF5zQjcZndABzJaPJHCcopkKjPhh7sshAYNv3Erj0D9gyMhlhhzEJTbLkgQ0awvW+ldNfjhEbI5exnLnYIUGqQysZPZ0d3uc3trYoVwgKP+CHgDoQTbUQCMu5bLmVxfV0M4Y2KEwwk8K+dr/nP4BUG62G56Q3xRQOgsV3 ansible@devops'


@task
def install_fail2ban():
    """
    apt-get install fail2ban and configure
    """


@task
def setup_ansible_user():
    """
    Setup Ansible user, keys, and sudoers.d file
    """
    sudo('groupadd -g 990 ansible')
    sudo('useradd -m -d /var/lib/ansible -s /bin/bash -u 990 -g 990 ansible')
    sudo('mkdir -p /var/lib/ansible/.ssh && chown ansible:ansible /var/lib/ansible/.ssh')
    sudo('chmod 700 /var/lib/ansible/.ssh')
    sudo('echo "%s" > /var/lib/ansible/.ssh/authorized_keys' % ANSIBLE_KEY)
    sudo('echo "%s" > /tmp/ansible_sudo' % '%ansible    ALL=(ALL)   NOPASSWD:ALL')
    sudo('chmod 440 /tmp/ansible_sudo && mv /tmp/ansible_sudo /etc/sudoers.d')


@task
def show_mounts():
    """
    show mount output
    """
    print run('mount')


@task
def show_df():
    """
    show df -h
    """
    print "host: ", env.host
    print run('df -h')

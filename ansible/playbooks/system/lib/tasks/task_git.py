################################################
__author__ = 'eric sales'
__copyright__ = "Copyright 2017, WildRiver Technologies Inc"
__version__ = "0.2.0"
__maintainer__ = "Larry Sellars"
__email__ = "larry.sellars@wildrivertechnologies.com"
__status__ = "production"
################################################
"""
WebTelemetry BootStrap Task Group: task_git

    git {git_ppa_repo}: install latest git from git-core/ppa

"""
from fabric.api import *


def git_ppa_repo():
    """
    TASK:git - install git from ppa:git-core
    """
    print "task: installing git from ppa.."
    # install packages required to use 'add-apt-repository #
    sudo('apt-get install -y python-software-properties software-properties-common')
    print "  adding repository."
    sudo('add-apt-repository -y ppa:git-core/ppa')
    print "  running apt-get update"
    sudo('apt-get update')
    print "  running apt-get install for git"
    #  Removing asciidoc - takes a long time to install and not required  #
    # sudo('apt-get install -y git git-man git-svn asciidoc')
    sudo('apt-get install -y git git-man git-svn')
    # set system wide configs #
    print "  running git configs."
    sudo('git config --system color.status auto')
    sudo('git config --system color.branch auto')
    sudo('git config --system color.interactive auto')
    sudo('git config --system color.diff auto')

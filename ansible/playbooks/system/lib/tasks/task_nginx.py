################################################
__author__ = 'eric sales'
__copyright__ = "Copyright 2017, WildRiver Technologies Inc"
__version__ = "0.2.0"
__maintainer__ = "Larry Sellars"
__email__ = "larry.sellars@wildrivertechnologies.com"
__status__ = "production"
################################################
"""
WebTelemetry BootStrap Task Group: task_nginx

    nginx_server
"""
from fabric.api import sudo


def nginx_server():
    """
    TASK:nginx_server - install nginx from ppa:nginx
    """
    print "task:  staring nginx install from repo"
    if 'no' == sudo('which nginx || echo "no"'):
        print "   installing required pkgs"
        sudo('apt-get install -y python-software-properties software-properties-common')
        print "   updating repository"
        sudo('add-apt-repository -y ppa:nginx/stable')
        print "   starting apt-get install for nginx."
        sudo('apt-get update')
        sudo('apt-get install -y nginx')
    else:
        print "  skipping, nginx already installed."
    ## start nginx if not already running ##
    sudo('service nginx status || service nginx start')

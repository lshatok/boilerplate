################################################
__author__ = 'eric sales'
__copyright__ = "Copyright 2017, WebTelemetry US Inc."
__version__ = "0.2.0"
__maintainer__ = "Larry Sellars"
__email__ = "larry.sellars@webtelemetry.us"
__status__ = "production"
################################################
"""
WebTelemetry BootStrap Task Group: task_ruby

    ruby_rbenv(rbenv_configs)

"""
from fabric.api import *


def ruby_rbenv(rb_confs):
    """
    TASK:rbenv - install ruby with rbenv
    yaml config format required

    ruby_rbenv:
        user: wtuser
        path: /home/webtelemetry
        ruby_ver:  2.3.5

    """
    rb_user = rb_confs['user']
    rb_path = rb_confs['path']
    rb_ver = rb_confs['ruby_ver']
    print "task:  ruby_rbenv starting"
    with cd(rb_path):
        if 'no' == sudo('[ -d .rbenv ] || echo "no"'):
            sudo('git clone https://github.com/sstephenson/rbenv.git .rbenv', user=rb_user, shell=True)
            sudo('git clone https://github.com/sstephenson/ruby-build.git .rbenv/plugins/ruby-build',
                 user=rb_user, shell=True)
        else:
            print "   skipping: %s/.rbenv path already found" % rb_path
    # check if version is already installed #
    if 'no' == sudo('[ -d %s/.rbenv/versions/%s ] || echo "no"' % (rb_path, rb_ver)):
        print "   NOTICE: installing ruby on a low powered server may take a while."
        sudo('su -l %s -c "cd %s && rbenv install %s"' % (rb_user, rb_path, rb_ver), shell=True)
        sudo('su -l %s -c "cd %s && rbenv global %s"' % (rb_user, rb_path, rb_ver), shell=True)
        sudo('su -l %s -c "cd %s && rbenv rehash"' % (rb_user, rb_path), shell=True)
        sudo('su -l %s -c "cd %s && gem install bundler"' % (rb_user, rb_path), shell=True)
    else:
        print "   skipping: %s/.rbenv/versions/%s already exists." % (rb_path, rb_ver)

################################################
__author__ = 'eric sales'
__copyright__ = "Copyright 2017, WebTelemetry US Inc."
__version__ = "0.2.0"
__maintainer__ = "Larry Sellars"
__email__ = "larry.sellars@webtelemetry.us"
__status__ = "production"
################################################
"""
WebTelemetry BootStrap Task Group: task_python

    python_install_distribute()
    python_pip(pip_configs)
    python_pip_upgrade(pip_configs)
    python_virtualenv(virtenv_configs)

"""
from fabric.api import *


def python_install_distribute():
    """
    TASK:python_install_distribute - Install distribute and pip from source
    no configs required
    """
    print "task:  python_install_distribute"
    sudo('curl -L http://python-distribute.org/distribute_setup.py | python')
    sudo('curl -L https://raw.github.com/pypa/pip/master/contrib/get-pip.py | python')
    # clean up
    sudo('[ ! -d ~/build ] || rm -r ~/build')
    sudo('[ ! -f ~/distribute-*.tar.gz ] || rm -r ~/distribute-*.tar.gz')


def python_pip(pip_configs):
    """
    TASK:python_pip - GLOBAL pip install <pip_list>
    @param pip_configs

    yaml config format
    python_pip: [ pip_pkg1, pip_pkg2, .. ]
    """
    print "task:  python_pip install"
    for pip_pkg in pip_configs:
        print "   pip install %s" % pip_pkg
        sudo('pip install %s' % pip_pkg)


def python_pip_upgrade(pip_configs):
    """
    TASK:python_pip_upgrade - GLOBAL pip install --upgrade
    @param pip_configs

    yaml config format
    python_pip_upgrade: [ pip_pkg1_to_update, .. ]
    """
    print "task:  python pip install --upgrade"
    for pip_pkg in pip_configs:
        print "  pip upgrade %s" % pip_pkg
        sudo('pip install --upgrade %s' % pip_pkg)


def python_virtualenv(virtenv_configs):
    """
    TASK:python_virtualenv - create virtualenv
    @param virtenv_configs

    yaml config format
    python_virtualenv:
        /dir/for/virtualenv:
            user:   virtenv_user
            pip:  [ pkgs for virtual_env ]
    """
    print "task:  python virtualenv creation"
    # check if virtualenv exists #
    if 'no' == sudo('which virtualenv || echo "no"'):
        raise Exception("virtualenv not installed!")

    for venv in virtenv_configs:
        v_user = virtenv_configs[venv]['user']
        v_pips = virtenv_configs[venv].get('pip', [])

        # Creating the virtualenv #
        print "   creating virtualenv %s" % venv
        sudo('virtualenv %s' % venv, user=v_user, shell=True)
        for p_pkg in v_pips:
            print "   virt pip installing %s" % v_pips
            sudo('su -l %s -c "cd %s && . bin/activate && pip install %s"' % (v_user, venv, p_pkg), shell=True)

################################################
__author__ = 'eric sales'
__copyright__ = "Copyright 2017, WebTelemetry US Inc."
__version__ = "0.2.0"
__maintainer__ = "Larry Sellars"
__email__ = "larry.sellars@webtelemetry.us"
__status__ = "production"
################################################
"""
WebTelemetry BootStrap run_task function
    BootStrap tasks are defined in groups and calls are mapped here
    All tasks group files need to be defined in __init__.py __all__ list

    run_task(task_name, *args)
"""
from tasks import *


def run_task(task_name, *args):
    config_args = args[0]
    file_repo = args[1]
    try:
        main_task = task_name.split(':')[0]
        sub_task = task_name.split(':')[1]
    except IndexError:
        main_task = task_name
        sub_task = ''

    # DEBUG
    # print "task: ", task_name
    # print "main task: ", main_task
    # print "sub task: ", sub_task
    # print "configs: ", config_args
    # print "file_repo: ", file_repo

    # task_packages grouping
    if main_task == 'apt_update':
        task_packages.apt_update()
        return
    if main_task == 'apt_upgrade':
        task_packages.apt_upgrade()
        return
    if main_task == 'packages':
        task_packages.packages(config_args)
        return

    # task_accounts grouping
    if main_task == 'groups':
        task_accounts.groups(config_args)
        return
    if main_task == 'accounts':
        task_accounts.accounts(config_args)
        return
    if main_task == 'users':
        task_accounts.user_add(config_args)
        return

    # task_system grouping
    if main_task == 'reboot':
        task_system.host_reboot()
        return
    if main_task == 'directories':
        task_system.create_directories(config_args)
        return
    if main_task == 'files':
        task_system.deploy_files(config_args, file_repo)
        return
    if main_task == 'sudoers':
        task_system.deploy_sudoers(config_args, file_repo)
        return
    if main_task == 'run_commands':
        task_system.run_commands(config_args[sub_task])
        return
    if main_task == 'symlinks':
        task_system.create_symlinks(config_args)
        return

    # task_git grouping
    if main_task == 'git':
        task_git.git_ppa_repo()
        return

    # task_python grouping
    if main_task == 'python_install_distribute':
        task_python.python_install_distribute()
        return
    if main_task == 'python_pip':
        task_python.python_pip(config_args)
        return
    if main_task == 'python_pip_upgrade':
        task_python.python_pip_upgrade(config_args)
        return
    ## ToDo: add directory permission check for virtenv ##
    if main_task == 'python_virtualenv':
        task_python.python_virtualenv(config_args)
        return

    # task_ruby grouping
    if main_task == 'ruby_rbenv':
        task_ruby.ruby_rbenv(config_args)
        return

    # task_java grouping
    if main_task == 'java7':
        task_java.oracle_java7()
        return

    # task_redis grouping
    if main_task == 'data_collector':
        task_redis.install_redis_server()
        return

    # task_nginx grouping
    if main_task == 'nginx_server':
        task_nginx.nginx_server()
        return

    # task_apache_ant grouping
    if main_task == 'apache_ant':
        task_apache_ant.apache_ant()
        return

    # task_influxdb grouping :test
    if main_task == 'influxdb_server':
        task_influxdb.influxdb_server()
        return

    # task_tomcat grouping
    if main_task == 'tomcat':
        task_tomcat.install_tomcat()
        return
    if main_task == 'tomcat_restart':
        task_tomcat.tomcat_restart()
        return

    # task_cloudera_hadoop grouping   :to_test
    if main_task == 'cloudera_manager':
        task_cloudera_hadoop.cloudera_manager(config_args)
        return

    # task_filesystem grouping  :to_test
    if main_task == 'mounts':
        task_filesystem.create_mounts(config_args)
        return
    if main_task == 'umount_ephemeral':
        task_filesystem.umount_ephemeral()
        return
    if main_task == 'lvm_diskgroups':
        task_filesystem.lvm_diskgroup(config_args)
        return

    # task_nodejs grouping  :to_test
    if main_task == 'nodejs':
        task_nodejs.install_nodejs()
        return

    # task_postgresql grouping  :to_test
    if main_task == 'postgresql_server':
        task_postgresql.postgresql_server_55(config_args)
        return

    # task_newrelic grouping  :to_test
    if main_task == 'newrelic_hostagent':
        task_newrelic.newrelic_hostagent(config_args)
        return

    # task_os_common grouping  :to_test
    if main_task == 'os_common':
        task_os_common.os_common_group()
        return
    if main_task == 'os_enable_limits':
        task_os_common.os_enable_limits()
        return

    # task_sftp_server grouping
    if main_task == 'sftp_server':
        task_sftp.sftp_server(config_args)
        return
    if main_task == 'sftp_users':
        task_sftp.sftp_users(config_args)
        return

    # task_aws grouping
    if main_task == 'aws_fix_dhclient':
        task_aws.aws_update_dhclient()
        return

    ## we raise an exception if no commands found ##
    raise Exception("Unknown task '%s'" % main_task)

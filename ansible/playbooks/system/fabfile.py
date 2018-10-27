################################################
__author__ = 'Larry Sellars'
__copyright__ = "Copyright 2017, WildRiver Technologies Inc"
__version__ = "0.2.0"
__maintainer__ = "Larry Sellars"
__email__ = "larry.sellars@wildrivertechnologies.com"
__status__ = "development"
################################################
"""
WebTelemetry slipstrea main Fabric fabfile
    fab will normally be called with a bash wrapper 'do-slipstream.sh'
    but can be initiated directly to call out individual tasks

fab function(s):
    use_role(role_name, *args)

"""
import os
import sys

import_error = []
try:
    import yaml
except ImportError:
    import_error.append('pyaml')

try:
    from fabric.api import *
except ImportError:
    import_error.append('fabric')

if import_error:
    print "Error: missing python modules %s" % import_error
    print "Install the required modules:  pip -r requirements.txt"
    sys.exit(1)

# env vars > settings file > defaults
ACCOUNTS_FILE = "accounts/wtusers.hml"
ROLES_FILE = "roles.yml"

from lib.classes import BS_role
from lib import BS_tasks
from lib.ops_tasks import *
from lib.tasks import task_system


def bootstrap_role(role_name, *args):
    """
    Initialize Bootstrap configs for :role_name,*args
    @param role_name, *args
    @return:
    """
    # read roles yaml file #
    with open('roles.yml', 'r') as f:
        bs_role_main = yaml.load(f)
    # Verify role is defined #
    bs_configs = bs_role_main.get(role_name)
    if not bs_configs:
        abort("Role '%s' is not defined for BootStrap." % role_name)
    # Verify required configs are defined #
    role_path = ''
    role_config_file = ''
    try:
        role_path = bs_configs['role_path']
        role_config_file = bs_configs['config']
    except KeyError as e:
        abort("Missing required definition %s in roles.yml config." % e)
    # Verify role_name yaml file exists #
    _rc_yaml = os.path.join(role_path, role_config_file)
    if not os.path.isfile(_rc_yaml):
        abort("Role config '%s' file is not found." % _rc_yaml)
    with open(_rc_yaml, 'r') as ff:
        config_dict = yaml.load(ff)

    fab_role = BS_role.BootStrapRole(role_name, role_path, config_dict)
    # print "IP: ", fab_role.get_ip_addr('eth0')

    # Check if role is already installed #
    role_found = False
    if os.getenv('IGNORE_EXISTING') != 'YES':
        if fab_role.role_name in fab_role.get_installed_roles():
            role_found = True

    # Check if required role(s) exists #
    if fab_role.required_roles:
        if not set(fab_role.required_roles).issubset(fab_role.get_installed_roles()):
            abort("Missing one or more required roles '%s'" % fab_role.required_roles)

    task_list = fab_role.tasks
    append_role_file = True
    # Check for any optional overrides here #
    if bs_configs.get('file_repo'):
        fab_role.file_repo = bs_configs['file_repo']

    if args:
        task_list = list(args)
        append_role_file = False

    if task_list:
        if append_role_file and role_found:
            warn("Skipping.. role '%s' already exists." % fab_role.role_name)
        else:
            for t in task_list:
                if t and ':' in t:
                    t_conf = t.split(':')[0]
                else:
                    t_conf = t
                BS_tasks.run_task(t, fab_role.config_dict.get(t_conf), fab_role.file_repo)
            pass
            if append_role_file:
                fab_role.append_role_file()
    else:
        print "No tasks defined or given for role '%s'" % fab_role.role_name


def bootstrap_tasks(role_name, *args):
    """
    Run Bootstrap role with specified tasks (*args)
    """
    # read roles yaml file #
    with open('roles.yml', 'r') as f:
        bs_role_main = yaml.load(f)
    # Verify role is defined #
    bs_configs = bs_role_main.get(role_name)
    if not bs_configs:
        abort("Role '%s' is not defined for BootStrap." % role_name)
    # Verify required configs are defined #
    role_path = ''
    role_config_file = ''
    try:
        role_path = bs_configs['role_path']
        role_config_file = bs_configs['config']
    except KeyError as e:
        abort("Missing required definition %s in roles.yml config." % e)
    # Verify role_name yaml file exists #
    _rc_yaml = os.path.join(role_path, role_config_file)
    if not os.path.isfile(_rc_yaml):
        abort("Role config '%s' file is not found." % _rc_yaml)
    with open(_rc_yaml, 'r') as ff:
        config_dict = yaml.load(ff)

    fab_role = BS_role.BootStrapRole(role_name, role_path, config_dict)

    # Check if role is already installed #
    if fab_role.role_name in fab_role.get_installed_roles():
        role_found = True
    else:
        role_found = False

    # Check if role is already installed #
    role_found = False
    if os.getenv('IGNORE_EXISTING') == 'YES':
        role_found = True
    else:
        if fab_role.role_name in fab_role.get_installed_roles():
            role_found = True
        # Check if required role(s) exists #
        if fab_role.required_roles:
            if not set(fab_role.required_roles).issubset(fab_role.get_installed_roles()):
                abort("Missing one or more required roles '%s'" % fab_role.required_roles)

    task_list = args
    append_role_file = False

    if bs_configs.get('file_repo'):
        fab_role.file_repo = bs_configs['file_repo']

    if task_list:
        if append_role_file and role_found:
            warn("Skipping.. role '%s' already exists." % fab_role.role_name)
        else:
            for t in task_list:
                if ':' in t:
                    t_conf = t.split(':')[0]
                else:
                    t_conf = t
                BS_tasks.run_task(t, fab_role.config_dict.get(t_conf), fab_role.file_repo)
            pass
            if append_role_file:
                fab_role.append_role_file()


def manage_accounts(accounts_file, account_task):
    """
    Manage account info from ACCOUNTS_FILE (yaml)
    options:
        :groups
        :users,*args
        :user_groups,*args
    """
    # read configs from ACCOUNTS_FILE #
    try:
        with open(accounts_file, 'r') as f:
            try:
                yaml_configs = yaml.load(f)
            except Exception as e:
                abort("YAML Load Error: ", e)
    except IOError as e:
        abort("Account File Load Error: ", e)

    if not account_task:
        abort("missing acct_task args")

    task_name = account_task.split(':')[0]

    try:
        task_args = account_task.split(':')[1].split('/')
    except IndexError:
        abort("missing specified acct_task args info")

    # create any groups listed in yaml file #
    if 'groups' in yaml_configs.keys():
        group_list = yaml_configs['groups']
        if group_list:
            task_account_management.group_add(group_list)

    # create users listed from a user group #
    user_list = []
    if task_name == 'user_groups':
        if 'user_groups' in yaml_configs.keys():
            # verify listed user_groups are valid #
            if set(task_args) < set(yaml_configs['user_groups'].keys()):
                for t_arg in task_args:
                    # use a set with union to remove duplicates
                    user_list = list(set(user_list) | set(yaml_configs['user_groups'][t_arg]))
            else:
                abort("unknown or misconfigured user_group(s): %s" % task_args)
        else:
            abort("No user_groups defined in %s" % accounts_file)

    if task_name == 'users':
        # use set to remove any duplicates #
        user_list = list(set(task_args))

    # verify user settings #
    users_config_list = yaml_configs['users'].keys()
    users_not_found = []
    for u in user_list:
        if not u in users_config_list:
            users_not_found.append(u)
    if users_not_found:
        abort("missing user configs for %s in '%s'" % (users_not_found, accounts_file))

    for user in user_list:
        # create a user dict to pass #
        user_dict = {}
        if yaml_configs['users'].get('defaults'):
            user_dict = yaml_configs['users'].get('defaults')
        user_dict.update(yaml_configs['users'][user])
        task_account_management.user_add(user, user_dict)
    with hide('everything'):
        task_system.add_to_sudoers('Leo Shatokhin')

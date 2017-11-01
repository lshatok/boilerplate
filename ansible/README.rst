Ansible ReadMe
==============

Install Python Pip
--------------
Recommended version 2.7.x
Download from https://www.python.org/downloads/



Install Python Pip *Available from Python Distribution as dist-packages (python 2.7)

--------------
Recommended version pip 9.x
Download from https://www.python.org/downloads/


Install Ansible
---------------
Recommended to install within a virtualenv

pip install -r requirements.txt

Note: install with sudo/root to make global


Configuration
-------------
Changes can be made and used in a configuration file which will be processed in the following order:

* ANSIBLE_CONFIG (an environment variable)
* ansible.cfg (in the current directory)
* .ansible.cfg (in the home directory)
* /etc/ansible/ansible.cfg

To override Ansible configs you can set up your own env vars, like so:
ANSIBLE_HOSTS= path to hosts config file

- For Devops configs:

Set Env variables to your devops repo location
export ANSIBLE_CONFIG=devops/ansible/config/ansible.cfg
export ANSIBLE_HOSTS=devops/ansible/config/ansible_hosts


SSH Keys
--------
In your ansible.cfg add private_key_file=<path to ubuntu user keyfile>
Or include --private-key=<key_file> to the command line





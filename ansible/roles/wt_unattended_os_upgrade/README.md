Role Name
=========

 This role automagically upgrades Ubuntu servers to the next generally available
 release in unattended mode. The role will reboot the remote machine after
 completion of the upgrade.

Requirements
------------
You need boto (obviously) to run the role. If you do not have boto installed,
you are probably not going to be able to run this,  or any other roles.

Role Variables
--------------

None

Dependencies
------------
Requires Ansible version 1.8.3 or higher


Example Playbook
----------------

Just add the role name to any playbook wherein you'd like to have the upgrade
run as part of the play.

    - hosts: servers
      roles:
        -wt_unattended_os_upgrade 

License
-------

WebTelemetry Inc. All rights reserved.

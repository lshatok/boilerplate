Role Name
=========

This role will install Amazon's enhanced network drivers, which provide double
the throughput for Amazon AWS front and backend io.

The role has been tested on Ubuntu/Debian 12 and 14 AMI's only.

Requirements
------------
You need to have a set of working AWS keys  access_key_id and secret_access_key
in order to be able to use awscli.

Place the keys into the password_vars file for your particular  environment like
so:

aws:
  ec2:
     access_key_id: 'YOUR_KEY_ID"
     secret_access_key: 'YOUR_SECRET_ACCESS_KEY'



Role Variables
--------------
You will need to add these following variable to the group_vars file for your
environment like so:

aws:
  ec2:
      output_format: text
      region: us-west-2

These variables are needed in order to use awscli package
Dependencies
------------

boto

Example Playbook
----------------

Include the role as part of any other playbook. For example to use the role as
part of the ec2_launch.yml playbook, add the role inside the roles stanza
as below:

    - hosts: server
    - roles:
	 - aws_dhclient_patch
	 - wt_core
	 - wt_git
	 - aws_enhanced_networking


License
WebTelemetry Inc.

Author Information
------------------
Leo Shatokhin leo.shatokhin@wildrivertechnologies.com

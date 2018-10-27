#!/usr/bin/env python
"""
Create an RDS Instance with info from a Config yaml file
"""
USAGE = """\
  RdsLaunch.py --file=config_yaml --name=rds_id --profile=rds_profile --subnetgroup=rds_group_name

    Required args:
        --file      location of Yaml config file
        --profile   name of config profile defined from Yaml file
        --name      RDS Unique Identifier for instance
        --dbname    Name of Mysql database to create
        --subnetgroup   Name of RDS DB subnetgroup
            *If the group doesn't exist, one will be created with defined subnets in config_yaml*

    optional args:
        --user      DBInstance master username
        --pass      DBInstance master password

"""
__author__ = 'eric sales'
__copyright__ = "Copyright 2017, WildRiver Technologies Inc"
__version__ = "0.7.6"
__maintainer__ = "Larry Sellars"
__email__ = "larry.sellars@wildrivertechnologies.com"
__status__ = "Production"

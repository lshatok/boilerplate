#!/usr/bin/env python
"""
Display the AWS Account Number.

Requirements:
    AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY setup in your environment vars or .boto file
    IAM Access Keys must be associated with an account with read access
    python 2.5 and up with boto

"""
__author__ = 'eric sales'
__copyright__ = "Copyright 2017, WebTelemetry US Inc."
__version__ = "0.7.6"
__maintainer__ = "Larry Sellars"
__email__ = "larry.sellars@webtelemetry.us"
__status__ = "Production"

import boto

Ec2 = boto.connect_ec2()
Sg = Ec2.get_all_security_groups()
Acct = ''

if Sg:
    sg = Sg[0]
    print sg.owner_id
else:
    print "[Error] Could not locate 'owner_id'"

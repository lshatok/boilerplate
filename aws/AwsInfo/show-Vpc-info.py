#!/usr/bin/env python
"""
Display useful AWS VPC information in nicely formatted view.

Requirements:
    AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY setup in your environment vars or .boto file
    IAM Access Keys must be associated with an account with read access
    python 2.5 and up with boto

"""
USAGE = """\
    show-Vpc-info.py  <VPC-ID> <REGION>
        Returns VPC info in json format
"""
__author__ = 'eric sales'
__copyright__ = "Copyright 2017, WebTelemetry US Inc."
__version__ = "0.7.6"
__maintainer__ = "Larry Sellars"
__email__ = "larry.sellars@webtelemetry.us"
__status__ = "Production"

import sys
from WTboto.AwsVpcs import *
from pprint import pprint


def main(VpcId, VpcRegion):
    vpc = AWSvpc(VpcId, VpcRegion)
    vpc.get_info()
    pprint(vpc.json())


if __name__ == "__main__":
    try:
        vpc_arg = sys.argv[1]
        region_arg = sys.argv[2]
    except IndexError as e:
        print "Missing args."
        print USAGE
        sys.exit(1)

    main(vpc_arg, region_arg)

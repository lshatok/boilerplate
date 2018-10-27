#!/usr/bin/env python
"""
List all VPC's in an AWS account.
 Displays vpc_id, region, cidr_block, and name tags.
 Default list is from US regions:
    [ us-east-1, us-west-1, us-west-2 ]
 Use '--all-regions' options to include all Global AWS regions
    [ eu-west-1, sa-east-1, ap-northeast-1, ap-southeast-1, ap-southeast-2 ]


Requirements:
    AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY setup in your environment vars or .boto file
    IAM Access Keys must be associated with an account with read access
    python 2.5 and up with boto

"""
__author__ = 'eric sales'
__copyright__ = "Copyright 2017, WildRiver Technologies Inc"
__version__ = "0.7.6"
__maintainer__ = "Larry Sellars"
__email__ = "larry.sellars@wildrivertechnologies.com"
__status__ = "Production"

import boto
import string
import sys
from boto import vpc

Regions = ['us-east-1', 'us-west-1', 'us-west-2']
WWRegions = ['eu-west-1', 'sa-east-1', 'ap-northeast-1', 'ap-southeast-1', 'ap-southeast-2']

awsConn = boto.connect_vpc()

HEADER = """\
 vpc_id         region       cidr_block        tag.name           tag.description
================================================================================= """

VPC_LINE = string.Template("""\
 $vpcid   $region  $cidr  $name $description """)


def main():
    print HEADER

    for Region in Regions:
        awsRegionConn = vpc.connect_to_region(Region)

        for _vpc in awsRegionConn.get_all_vpcs():
            printdict = {}
            v_desc = ''
            v_name = ''
            if 'Name' in _vpc.tags.keys():
                v_name = _vpc.tags['Name']
            if 'Description' in _vpc.tags.keys():
                v_desc = _vpc.tags['Description']

            printdict['vpcid'] = _vpc.id
            printdict['cidr'] = "%-16s" % _vpc.cidr_block
            printdict['region'] = "%-11s" % _vpc.region.name
            printdict['name'] = "%-18s" % v_name
            printdict['description'] = v_desc

            print VPC_LINE.substitute(printdict)


if __name__ == "__main__":
    try:
        if sys.argv[1] == '--all-regions':
            Regions += WWRegions
            print "Listing for all regions: "
            print Regions
    except IndexError as e:
        print "Listing for US regions (use --all-regions for all)"
        print Regions
        pass

    main()

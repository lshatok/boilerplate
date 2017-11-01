#!/usr/bin/env python
"""
Display useful AWS Subnet information in json or a nicely formatted view.

Requirements:
    AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY setup in your environment vars or .boto file
    IAM Access Keys must be associated with an account with read access
    python 2.5 and up with boto

"""
USAGE = """\
show-Subnet-info.py  [ --vpcid=  --region= ] [ --zone= ] | [ --all-regions ] [ --json | --raw ]
                      [ --sort=<zone|vpcid> ]


    Default:
        Show all Subnet info within all VPC's in US regions
        [ us-east1, us-west-1, us-west2 ]

    Options:
        --vpcid     : Show all subnets in specified VPCID (requires --region arg)
        --region    : Specify which region the VPCID arg is in (required with --vpcid)
        --zone      : Filter all subnets in a particular Availability Zone

        --all-regions : Include EU and AP AWS regions in search
        --json      : Return output in json format
        --raw       : output like Eddie Murphy old school
        --sort <zone|vpcid> : sort output by zone or vpcid  (ignored if --json set)
                Default sort is vpcid
"""
__author__ = 'eric sales'
__copyright__ = "Copyright 2017, WebTelemetry US Inc."
__version__ = "0.7.6"
__maintainer__ = "Larry Sellars"
__email__ = "larry.sellars@webtelemetry.us"
__status__ = "Production"

import boto
import getopt
import sys
from WTboto.AwsSubnets import *
from boto import vpc
from pprint import pprint


def SubnetList(VpcConn, Regions, VpcId='', Azone=''):
    """
    Return list of AWSsubnet classes  (optional VpcId,Region filter)
    """
    retlist = []
    if type(Regions) is not list:
        raise TypeError('Region needs to be a list')

    vpcFilter = []
    if VpcId:
        vpcFilter = [('vpcId', VpcId)]

    for Reg in Regions:
        _regConn = vpc.connect_to_region(Reg)
        if vpcFilter:
            get_allsubs = _regConn.get_all_subnets(filters=vpcFilter)
        else:
            get_allsubs = _regConn.get_all_subnets()

        for _sub in get_allsubs:
            if Azone:
                if _sub.availability_zone == Azone:
                    retlist.append(AWSsubnet(_sub))
            else:
                retlist.append(AWSsubnet(_sub))

    return retlist


def main(argv):
    arg_Vpcid = ''
    arg_Regions = ['us-east-1', 'us-west-1', 'us-west-2']
    arg_Zone = ''
    ww_Regions = ['eu-west-1', 'sa-east-1', 'ap-northeast-1', 'ap-southeast-1', 'ap-southeast-2']
    arg_Flags = []
    sortBy = 'vpcid'

    try:
        opts, args = getopt.getopt(argv, "hv:r:z:Rj",
                                   ['help', 'vpcid=', 'region=', 'zone=', 'all-regions', 'json', 'raw'])
    except getopt.GetoptError:
        print USAGE
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help", "?", "help"):
            print USAGE
            sys.exit()
        elif opt in ("-v", "--vpcid"):
            arg_Vpcid = arg
        elif opt in ('-f', '--region'):
            arg_Regions = [arg]
        elif opt in ('-z', '--zone'):
            arg_Zone = arg
        elif opt == '--all-regions':
            arg_Regions += ww_Regions
        elif opt in ('-j', '--json'):
            arg_Flags.append('json')
        elif opt == '--raw':
            arg_Flags.append('raw')

    Vpc = boto.connect_vpc()
    subList = SubnetList(Vpc, arg_Regions, arg_Vpcid, arg_Zone)

    if 'raw' in arg_Flags:
        for s in subList:
            print s
    elif 'json' in arg_Flags and not 'raw' in arg_Flags:
        for s in subList:
            pprint(s.json())
    else:
        # default
        printSubnets(subList, sortBy)


if __name__ == "__main__":
    main(sys.argv[1:])

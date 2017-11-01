#!/usr/bin/env python
"""
Display AWS Security Group information in json or a nicely formatted view.


Requirements:
    AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY setup in your environment vars or .boto file
    IAM Access Keys must be associated with an account with read access
    python 2.5 and up with boto

"""
USAGE = """\
show-SecurityGroup-info.py  [ --vpcid=  --region= ] | [ --all-regions ] [ --json | --raw ]
                      [ --sort=<region|id|vpcid> ]


    Default:
        Show all Security Groups info within all VPC's in US regions
        [ us-east1, us-west-1, us-west2 ]

    Options:
        --vpcid     : Show all security groups in specified VPCID (requires --region arg)
        --region    : Specify which region the VPCID arg is in (required with --vpcid)

        --all-regions : Include EU and AP AWS regions in search
        --json      : Return output in json format
        --raw       : output like Eddie Murphy old school
        --sort <region|id|vpcid> : sort output by region,id or vpcid  (ignored if --json set)
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
from boto import vpc
from pprint import pprint

from WTboto.AwsSecurityGroups import *


def SecurityGroupList(VpcConn, Regions, VpcId=''):
    """
    Return list of AWSsubnet classes  (optional VpcId,Region filter)
    """
    retlist = []
    if type(Regions) is not list:
        raise TypeError('Region needs to be a list')

    vpcFilter = {}
    if VpcId:
        vpcFilter = {'vpc_id': VpcId}

    for Reg in Regions:
        _regConn = vpc.connect_to_region(Reg)
        if vpcFilter:
            get_allsgs = _regConn.get_all_security_groups(filters=vpcFilter)
        else:
            get_allsgs = _regConn.get_all_security_groups()

        for _sgs in get_allsgs:
            retlist.append(AWSsecuritygroup(_sgs))
    return retlist


def main(argv):
    arg_Vpcid = ''
    arg_Regions = ['us-east-1', 'us-west-1', 'us-west-2']
    ww_Regions = ['eu-west-1', 'sa-east-1', 'ap-northeast-1', 'ap-southeast-1', 'ap-southeast-2']
    arg_Flags = []
    arg_sortBy = 'vpcid'
    SingleSecGroups = []

    try:
        opts, args = getopt.getopt(argv, "hv:r:s:Rj",
                                   ['help', 'vpcid=', 'region=', 'all-regions', 'sort', 'json', 'raw'])
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
        elif opt == '--all-regions':
            arg_Regions += ww_Regions
        elif opt in ('-s', '--sort'):
            arg_sortBy = arg
        elif opt in ('-j', '--json'):
            arg_Flags.append('json')
        elif opt == '--raw':
            arg_Flags.append('raw')

    for a in args:
        if a.startswith('sg-'):
            SingleSecGroups.append(a)

    Vpc = boto.connect_vpc()
    sgList = SecurityGroupList(Vpc, arg_Regions, arg_Vpcid)

    if SingleSecGroups:
        for s_sg in SingleSecGroups:
            printSecurityGroup(sgList, s_sg)
    elif 'raw' in arg_Flags:
        for s in sgList:
            print s
    elif 'json' in arg_Flags and not 'raw' in arg_Flags:
        for s in sgList:
            pprint(s.json())
    else:
        # default
        printSecurityGroups(sgList, arg_sortBy)


if __name__ == "__main__":
    main(sys.argv[1:])

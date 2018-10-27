#!/usr/bin/env python
"""
Display useful AWS Instance information in json or a nicely formatted view.

Requirements:
    AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY setup in your environment vars or .boto file
    IAM Access Keys must be associated with an account with read access
    python 2.5 and up with boto

"""
USAGE = """\
show-Instance-info.py  [ --vpcid=  --region= ] | [ --all-regions ] [ --json | --raw ]
                        [ --sort=<zone|vpcid|type|state> ] [ --attr <key> ]


    Default:
        Show all Instances info within all VPC's in US regions
        [ us-east1, us-west-1, us-west2, us-gov-west-1 ]

    Options:
        --vpcid     : Show all Instances in specified VPCID (requires --region arg)
        --region    : Specify which region the VPCID arg is in (required with --vpcid)

        --all-regions : Include EU and AP AWS regions in search
        --json      : Return output in json format
        --raw       : output like Eddie Murphy old school
        --sort < vpcid | type | region | state > : sort output by <key>   (ignored if --json set)
                Default sort is vpcid
        --attr < key>  : Print only the Instance Attributes of value <key>
"""
__author__ = 'eric sales'
__copyright__ = "Copyright 2017, WildRiver Technologies Inc"
__version__ = "0.7.6"
__maintainer__ = "Larry Sellars"
__email__ = "larry.sellars@wildrivertechnologies.com"
__status__ = "Production"

import boto
import getopt
import sys
from boto import vpc
from pprint import pprint

from WTboto.AwsInstances import *


def InstanceList(VpcConn, Regions, VpcId=''):
    """
    Return list of AWSinstance classes  (optional VpcId,Region filter)
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
            get_all = _regConn.get_all_instances(filters=vpcFilter)
        else:
            get_all = _regConn.get_all_instances()

        ## add filters here ##
        for _item in get_all:
            retlist.append(AWSinstance(_item.instances[0]))

    return retlist


def main(argv):
    arg_Vpcid = ''
    arg_Regions = ['us-east-1', 'us-west-1', 'us-west-2']
    ww_Regions = ['eu-west-1', 'sa-east-1', 'ap-northeast-1', 'ap-southeast-1', 'ap-southeast-2']
    arg_sortBy = 'vpcid'
    arg_Flags = []
    SingleInstances = []
    arg_Attribute = ''

    try:
        opts, args = getopt.getopt(argv, "hv:r:s:Rj",
                                   ['help', 'vpcid=', 'region=', 'sort=', 'all-regions', 'json', 'raw', 'attr='])
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
        elif opt in ('-s', '--sort'):
            arg_sortBy = arg
        elif opt == '--all-regions':
            arg_Regions += ww_Regions
        elif opt in ('-j', '--json'):
            arg_Flags.append('json')
        elif opt == '--raw':
            arg_Flags.append('raw')
        elif opt == '--attr':
            arg_Attribute = arg

    # SingleInstance = ' '.join(args)
    for a in args:
        if a.startswith('i-'):
            SingleInstances.append(a)

    Vpc = boto.connect_vpc()
    instList = InstanceList(Vpc, arg_Regions, arg_Vpcid)

    if SingleInstances:
        for s_inst in SingleInstances:
            printInstance(instList, s_inst)
            # print SingleInstances

    elif 'raw' in arg_Flags:
        for i in instList:
            print i
    elif 'json' in arg_Flags and not 'raw' in arg_Flags:
        for i in instList:
            pprint(i.json())
    elif arg_Attribute:
        printValues(instList, arg_Attribute)

    else:
        # default
        printInstances(instList, arg_sortBy)


if __name__ == "__main__":
    main(sys.argv[1:])

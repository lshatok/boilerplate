#!/usr/bin/env python
"""
Display AWS Elastic Block Storage information.
    Provide all info in json format or in table form displaying:
    vol_id,instance_id,device,size,zone,status,state,type,create_time

Requirements:
    AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY setup in your environment vars or .boto file
    IAM Access Keys must be associated with an account with read access
    python 2.5 and up with boto
"""
USAGE = """\
show-Ebs-info.py  [ --instance=  --region= ] | [ --all-regions ] [ --json | --raw ]
                      [ --sort=<zone|instance|state|size> ]  [ volume_id ]


    Default:
        Show all EBS Volume info within all US regions
        [ us-east1, us-west-1, us-west2 ]

    Options:
        --instance  : Specify all EBS volume info attached to instance
        --region    : Specify which region the to list all EBS volumes

        --all-regions : Include EU and AP AWS regions in search
        --json      : Return output in json format
        --raw       : output like Eddie Murphy old school
        --sort <zone|instance|state|size|create> : sort output by zone,instance,state, or size
                (ignored if --json set).   Default sort is by instance Id.
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

from WTboto.AwsEbs import *


def EbsList(VpcConn, Regions, instance=''):
    """
    Return list of AWSebs classes  (optional Filter by instance)
    """
    retlist = []
    if type(Regions) is not list:
        raise TypeError('Region needs to be a list')

    if instance and instance.startswith('i-'):
        ebs_filter = {'attachment.instance-id': instance}
    else:
        ebs_filter = {}

    for Reg in Regions:
        _regConn = vpc.connect_to_region(Reg)
        get_allvols = _regConn.get_all_volumes(filters=ebs_filter)

        for _vol in get_allvols:
            retlist.append(AWSebs(_vol))
    return retlist


def main(argv):
    arg_instance = ''
    arg_Regions = ['us-east-1', 'us-west-1', 'us-west-2']
    ww_Regions = ['eu-west-1', 'sa-east-1', 'ap-northeast-1', 'ap-southeast-1', 'ap-southeast-2']
    arg_Flags = []
    arg_sortBy = 'instance'
    SingleEbsVols = []

    try:
        opts, args = getopt.getopt(argv, "hi:r:s:Rj",
                                   ['help', 'instance=', 'region=', 'all-regions', 'sort=', 'json', 'raw'])
    except getopt.GetoptError:
        print USAGE
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help", "?", "help"):
            print USAGE
            sys.exit()
        elif opt in ("-i", "--instance"):
            arg_instance = arg
        elif opt in ('-r', '--region'):
            arg_Regions = [arg]
        elif opt in ('-s', '--sort'):
            if arg in ['zone', 'instance', 'state', 'size', 'create']:
                arg_sortBy = arg
        elif opt == '--all-regions':
            arg_Regions += ww_Regions
        elif opt in ('-j', '--json'):
            arg_Flags.append('json')
        elif opt == '--raw':
            arg_Flags.append('raw')

    for a in args:
        if a.startswith('vol-'):
            SingleEbsVols.append(a)

    Vpc = boto.connect_vpc()
    ebsList = EbsList(Vpc, arg_Regions, arg_instance)

    if SingleEbsVols:
        for s_ebs in SingleEbsVols:
            printEbsVol(ebsList, s_ebs)
    elif 'raw' in arg_Flags:
        for s in ebsList:
            print s
    elif 'json' in arg_Flags and not 'raw' in arg_Flags:
        for s in ebsList:
            pprint(s.json())
    else:
        # default
        printEbsVols(ebsList, arg_sortBy)


if __name__ == "__main__":
    main(sys.argv[1:])

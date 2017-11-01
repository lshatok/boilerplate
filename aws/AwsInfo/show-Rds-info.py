#!/usr/bin/env python
"""
Display AWS RDS information in json or a nicely formatted view.

Requirements:
    AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY setup in your environment vars or .boto file
    IAM Access Keys must be associated with an account with read access
    python 2.5 and up with boto

"""
USAGE = """\
show-Rds-info.py  [ --vpcid=  --region= ] | [ --all-regions ] [ --json | --raw ]
                      [ --sort=<zone|size> ] <rds_instance>


    Default:
        Show all RDS instance info within all US regions
        [ us-east1, us-west-1, us-west2 ]

    Options:
        --vpcid    : Specify info from vpcid
        --region    : Specify which region the to list all RDS instances

        --all-regions : Include EU and AP AWS regions in search
        --json      : Return output in json format
        --raw       : output like Eddie Murphy old school
        --sort <zone|size> : sort output by zone or size
                (ignored if --json set).   Default sort is by zone.
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
from boto import rds
from pprint import pprint

from WTboto.AwsRds import *


def RdsList(RdsConn, Regions, Vpcid=''):
    """
    Return list of AWSrds objects (optional filter by RDS instance)
    """
    retlist = []
    if type(Regions) is not list:
        raise TypeError('Region needs to be a list')

    for Reg in Regions:
        _regConn = rds.connect_to_region(Reg)
        get_allRds = _regConn.get_all_dbinstances()

        for _rds in get_allRds:
            # set Rds SubnetGroup dictionary #
            dbSubDict = {'name': '', 'subnets': [], 'description': ''}
            try:
                if _rds.DBSubnetGroupName:
                    get_DbSubGrp = _regConn.get_all_db_subnet_groups(name=_rds.DBSubnetGroupName)
                    _g = get_DbSubGrp[0]
                    dbSubDict['name'] = _g.name
                    dbSubDict['description'] = _g.description
                    dbSubDict['subnets'] = _g.subnet_ids
            except AttributeError as e:
                pass

            if Vpcid:
                try:
                    if _rds.VpcId == Vpcid:
                        retlist.append(AWSrds(_rds, dbSubDict))
                except AttributeError:
                    # VpcId Attribute only exists if Rds Object is in a VPC #
                    pass
            elif not Vpcid:
                retlist.append(AWSrds(_rds, dbSubDict))

    return retlist


def main(argv):
    arg_Vpcid = ''
    arg_Regions = ['us-east-1', 'us-west-1', 'us-west-2']
    ww_Regions = ['eu-west-1', 'sa-east-1', 'ap-northeast-1', 'ap-southeast-1', 'ap-southeast-2']
    arg_Flags = []
    arg_sortBy = 'instance'
    SingleInstances = []

    try:
        opts, args = getopt.getopt(argv, "hv:r:s:Rj",
                                   ['help', 'vpcid=', 'region=', 'all-regions', 'sort=', 'json', 'raw'])
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
            if arg in ['zone', 'size']:
                arg_sortBy = arg
        elif opt == '--all-regions':
            arg_Regions += ww_Regions
        elif opt in ('-j', '--json'):
            arg_Flags.append('json')
        elif opt == '--raw':
            arg_Flags.append('raw')

    for a in args:
        SingleInstances.append(a)

    Rds = boto.connect_rds()
    RDSList = RdsList(Rds, arg_Regions, arg_Vpcid)

    if SingleInstances:
        for s_inst in SingleInstances:
            printRdsInstance(RDSList, s_inst)

    elif arg_Vpcid:
        for _r in RDSList:
            _r.printInfo()
    elif 'raw' in arg_Flags:
        for r in RDSList:
            print r
    elif 'json' in arg_Flags and not 'raw' in arg_Flags:
        for r in RDSList:
            pprint(r.json())
    else:
        # default
        printRdsInfo(RDSList, arg_sortBy)


if __name__ == "__main__":
    main(sys.argv[1:])

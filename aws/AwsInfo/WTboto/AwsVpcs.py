"""
AWS Classes and functions for AwsInfo commands
"""
__author__ = 'eric sales'
__copyright__ = "Copyright 2017, WebTelemetry US Inc."
__version__ = "0.7.6"
__maintainer__ = "Larry Sellars"
__email__ = "larry.sellars@webtelemetry.us"
__status__ = "Production"

import boto
from boto import rds as BotoRDS
from boto import vpc as BotoVPC


class VpcIdError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class AWSvpc:
    def __init__(self, vpc_id, vpc_region):
        self.vpc_id = vpc_id
        self.name = ''
        self.cidr_block = ''
        self.region = vpc_region
        self.subnets = {}
        self.security_groups = {}
        self.instances = {}
        self.rds = {}
        self.description = ''
        self._valid = False

    def get_info(self):
        ## boto initial connection required before connecting to a region ##
        boto.connect_vpc()
        awsRegionConn = BotoVPC.connect_to_region(self.region)

        for _vid in awsRegionConn.get_all_vpcs():
            if _vid.id == self.vpc_id:
                self._valid = True
                self.cidr_block = _vid.cidr_block
                self.region = _vid.region.name
                for _sub in awsRegionConn.get_all_subnets(filters=[('vpcId', _vid.id)]):
                    self.subnets[_sub.id] = {'cidr': _sub.cidr_block, 'zone': _sub.availability_zone}

                if 'Name' in _vid.tags.keys():
                    self.name = _vid.tags['Name']
                if 'Description' in _vid.tags.keys():
                    self.description = _vid.tags['Description']

                for _sg in awsRegionConn.get_all_security_groups(filters={'vpc_id': self.vpc_id}):
                    self.security_groups[_sg.id] = {'name': _sg.name, 'description': _sg.description}

                for _resv in awsRegionConn.get_all_instances(filters={'vpc_id': self.vpc_id}):
                    _inst = _resv.instances[0]
                    self.instances[_inst.id] = {'private_ip': _inst.private_ip_address,
                                                'public_ip': _inst.ip_address,
                                                'state': _inst.state,
                                                'subnet_id': _inst.subnet_id,
                                                'type': _inst.instance_type,
                                                'avail_zone': _inst.placement,
                                                }
                    if 'Name' in _inst.tags.keys():
                        self.instances[_inst.id]['Name'] = _inst.tags['Name']

            # get RDS info - Call is required before switching regions#
            boto.connect_rds()
            rdsRegionConn = BotoRDS.connect_to_region(self.region)
            for _rds in rdsRegionConn.get_all_dbinstances():
                try:
                    if _rds.VpcId == self.vpc_id:
                        self.rds[_rds.id] = {'zone': _rds.availability_zone,
                                             'class': _rds.instance_class,
                                             'size': _rds.allocated_storage,
                                             }
                        try:
                            self.rds[_rds.id]['db_name'] = _rds.DBName
                        except AttributeError as e:
                            self.rds[_rds.id]['db_name'] = ''
                except AttributeError as e:
                    # VpcId attribute is not available if not in a VPC #
                    pass

        if not self._valid:
            raise VpcIdError("VpcId: %s Not found in AWS account!" % (self.vpc_id))

    def json(self):
        ret = {self.vpc_id: {'name': self.name,
                             'description': self.description,
                             'region': self.region,
                             'cidr_block': self.cidr_block,
                             'subnets': self.subnets,
                             'security_groups': self.security_groups,
                             'instances': self.instances,
                             'rds': self.rds,
                             }}
        return ret

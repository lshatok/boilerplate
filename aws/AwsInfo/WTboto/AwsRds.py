"""
AWS Classes and functions for AwsInfo commands
"""
__author__ = 'eric sales'
__copyright__ = "Copyright 2017, WildRiver Technologies Inc"
__version__ = "0.7.6"
__maintainer__ = "Larry Sellars"
__email__ = "larry.sellars@wildrivertechnologies.com"
__status__ = "Production"


class AWSrdsSubnet:
    def __init__(self, rdsSubnet_obj):
        self.name = rdsSubnet_obj.name
        self.avail_zone = rdsSubnet_obj.Name
        self.subnets = rdsSubnet_obj.subnet_ids
        self.vpc_id = rdsSubnet_obj.vpc_id
        self.description = rdsSubnet_obj.description

    def __repr__(self):
        ret = {'name': self.name,
               'avail_zone': self.avail_zone,
               'subnets': self.subnets,
               'self.vpc_id': self.vpc_id,
               'description': self.description, }
        return repr(ret)


class AWSrds:
    def __init__(self, rds_obj, rds_SubnetGroup):
        self.id = rds_obj.id
        self.endpoint = '%s:%s' % (rds_obj.endpoint[0], rds_obj.endpoint[1])
        #        self.engine = '%s %s' % (rds_obj.engine, rds_obj.EngineVersion)
        self.size = rds_obj.allocated_storage
        self.type = rds_obj.instance_class
        self.avail_zone = rds_obj.availability_zone
        self.master_user = rds_obj.master_username
        self.status = rds_obj.status
        self.multi_az = rds_obj.multi_az
        self.create_time = rds_obj.create_time
        self.db_subnetgroup = ''
        self.db_subnetgroup_desc = ''
        self.db_subnet_ids = rds_SubnetGroup['subnets']

        self.vpc_id = ''
        self.tags = {}
        self.dbname = ''
        self.securitygroup_id = ''
        try:
            self.vpc_id = rds_obj.VpcId
            self.dbname = rds_obj.DBName
            self.securitygroup_id = rds_obj.VpcSecurityGroupId
            self.db_subnetgroup = rds_obj.DBSubnetGroupName
            self.db_subnetgroup_desc = rds_obj.DBSubnetGroupDescription
            # tags must be last #
            self.tags = rds_obj.tags
        except AttributeError as e:
            # these are definied if VPC or tags are created #
            pass

    def __repr__(self):
        ret = {'id': self.id,
               'endpoint': self.endpoint,
               'engine': self.engine,
               'size': self.size,
               'type': self.type,
               'avail_zone': self.avail_zone,
               'master_user': self.master_user,
               'status': self.status,
               'multi_az': self.multi_az,
               'vpc_id': self.vpc_id,
               'dbname': self.dbname,
               'securitygroup_id': self.securitygroup_id,
               'tags': self.tags,
               'db_subnetgroup': self.db_subnetgroup,
               'db_subnetgroup_desc': self.db_subnetgroup_desc,
               'db_subnet_ids': self.db_subnet_ids,
               }
        return repr(ret)

    def json(self):
        """
        Method to return objects in json/dict format
        """
        ret = {self.id: {'endpoint': self.endpoint,
                         'engine': self.engine,
                         'size': self.size,
                         'type': self.type,
                         'avail_zone': self.avail_zone,
                         'master_user': self.master_user,
                         'status': self.status,
                         'multi_az': self.multi_az,
                         'vpc_id': self.vpc_id,
                         'dbname': self.dbname,
                         'securitygroup_id': self.securitygroup_id,
                         'tags': self.tags,
                         'db_subnetgroup': self.db_subnetgroup,
                         'db_subnetgroup_desc': self.db_subnetgroup_desc,
                         'db_subnet_ids': self.db_subnet_ids,
                         }}
        return ret

    def printInfo(self, options='json'):
        """
        Method to print Attributes (options = json,raw,pretty)
          *json format is the default
        """
        from pprint import pprint
        pprint(self.json())
        return


def printRdsInfo(Obj_list, Sort=''):
    """
    Method to print the Rds in a formatted view
    """
    import string
    HEADER = """\
 rds_id                     size  type         vpc_id        zone        endpoint
====================================================================================================="""

    LINE = string.Template("""\
 $rdsid    $size  $type $vpcid  $zone $endpoint""")

    print HEADER
    ## sort options ##
    if Sort == 'zone':
        sortedList = sorted(Obj_list, key=lambda rds: rds.avail_zone)
    elif Sort == 'size':
        sortedList = sorted(Obj_list, key=lambda rds: rds.size)
    else:
        # default
        sortedList = sorted(Obj_list, key=lambda rds: rds.id)

    for rdsObj in sortedList:
        printDict = {'rdsid': "%-22s" % rdsObj.id,
                     #                      'engine'      : "%-13s" % rdsObj.engine,
                     'size': "%4i" % rdsObj.size,
                     'type': "%-12s" % rdsObj.type,
                     'vpcid': "%-12s" % rdsObj.vpc_id,
                     'zone': "%-11s" % rdsObj.avail_zone,
                     'endpoint': rdsObj.endpoint
                     }
        print LINE.substitute(printDict)


def printRdsInstance(Obj_list, RdsId):
    """
    Method to print details for a single instance
    """
    from pprint import pprint
    for obj in Obj_list:
        if obj.id == RdsId:
            pprint(obj.json())
            return

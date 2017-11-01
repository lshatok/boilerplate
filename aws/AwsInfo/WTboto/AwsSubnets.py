"""
AWS Classes and functions for AwsInfo commands
"""
__author__ = 'eric sales'
__copyright__ = "Copyright 2017, WebTelemetry US Inc."
__version__ = "0.7.6"
__maintainer__ = "Larry Sellars"
__email__ = "larry.sellars@webtelemetry.us"
__status__ = "Production"


class AWSsubnet:
    def __init__(self, subnet_obj):
        self.subnet_id = subnet_obj.id
        self.vpc_id = subnet_obj.vpc_id
        self.cidr_block = subnet_obj.cidr_block
        self.avail_zone = subnet_obj.availability_zone
        self.avail_ip_addr_count = subnet_obj.available_ip_address_count
        self.region = subnet_obj.region.name
        self.name = ''
        try:
            if 'Name' in self.tags.keys():
                self.name = subnet_obj.tags['Name']
            self.tags = subnet_obj.tags
        except AttributeError:
            self.tags = {}
            pass

    def __repr__(self):
        ret = {'subnet_id': self.subnet_id,
               'vpc_id': self.vpc_id,
               'cidr_block': self.cidr_block,
               'name': self.name,
               'avail_zone': self.avail_zone,
               'avail_ip_addr_count': self.avail_ip_addr_count,
               'region': self.region,
               'tags': self.tags,
               }
        return repr(ret)

    def json(self):
        """
        Method to return objects in json/dict format
        """
        ret = {self.subnet_id: {'vpc_id': self.vpc_id,
                                'cidr_block': self.cidr_block,
                                'name': self.name,
                                'avail_zone': self.avail_zone,
                                'avail_ip_addr_count': self.avail_ip_addr_count,
                                'region': self.region,
                                'tags': self.tags,
                                }}
        return ret


def printSubnets(SubObj_list, Sort='vpc_id'):
    """
    Method to print the subnets in a nicely formatted view
    """
    import string
    HEADER = """\
  subnet_id        avail_zone    vpc_id          cidr_block         avail_ips  name
================================================================================================="""

    LINE = string.Template("""\
 $subnetid   $zone  $vpcid    $cidr  $availips  $name """)

    print HEADER
    ## sort options ##
    if Sort == 'zone':
        sortedList = sorted(SubObj_list, key=lambda subnet: subnet.avail_zone)
    else:
        # default
        sortedList = sorted(SubObj_list, key=lambda subnet: subnet.vpc_id)

    for subObj in sortedList:
        printDict = {'subnetid': subObj.subnet_id,
                     'zone': "%-12s" % subObj.avail_zone,
                     'vpcid': "%-12s" % subObj.vpc_id,
                     'cidr': "%-18s" % subObj.cidr_block,
                     'availips': "%4s" % str(subObj.avail_ip_addr_count),
                     'name': "%15s" % subObj.name
                     }
        print LINE.substitute(printDict)

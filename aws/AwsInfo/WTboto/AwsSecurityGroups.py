"""
AWS Classes and functions for AwsInfo commands
"""
__author__ = 'eric sales'
__copyright__ = "Copyright 2017, WildRiver Technologies Inc"
__version__ = "0.7.6"
__maintainer__ = "Larry Sellars"
__email__ = "larry.sellars@wildrivertechnologies.com"
__status__ = "Production"


class AWSsecuritygroup:
    def __init__(self, secgroup_obj):
        self.secgroup_id = secgroup_obj.id
        self.description = secgroup_obj.description
        self.vpc_id = secgroup_obj.vpc_id
        self.region = secgroup_obj.region.name
        self.name = secgroup_obj.name
        self.tags = secgroup_obj.tags

        self.rules = []
        for r in secgroup_obj.rules:
            _rule = {}
            _rule['from_port'] = r.from_port
            _rule['to_port'] = r.to_port
            _rule['grants'] = r.grants
            _rule['ipRanges'] = r.ipRanges
            _rule['ip_protocol'] = r.ip_protocol
            if r.ip_protocol == '-1':
                _rule['ip_protocol'] = 'Allow_ALL'
            self.rules.append(_rule)

    def __repr__(self):
        ret = {'secgroup_id': self.secgroup_id,
               'name': self.name,
               'description': self.description,
               'vpc_id': self.vpc_id,
               'region': self.region,
               'tags': self.tags,
               'rules': self.rules,
               }
        return repr(ret)

    def json(self):
        """
        Method to return objects in json/dict format
        """
        ret = {self.secgroup_id: {'name': self.name,
                                  'description': self.description,
                                  'vpc_id': self.vpc_id,
                                  'region': self.region,
                                  'tags': self.tags,
                                  'rules': self.rules,
                                  }}
        return ret


def printSecurityGroup(Obj_list, SecGroupId):
    """
    Method to print details for a single secgroup json
    """
    from pprint import pprint
    for obj in Obj_list:
        if obj.secgroup_id == SecGroupId:
            pprint(obj.json())
            return


def printSecurityGroups(Obj_list, Sort='vpc_id'):
    """
    Method to print the secgroups in a nicely formatted view
    """
    import string
    HEADER = """\
 secgroup_id   vpc_id         region    rules  name                    description
====================================================================================================================="""

    LINE = string.Template("""\
 $secgroupid   $vpcid   $region  $rules   $name $description """)

    print HEADER
    ## sort options ##
    if Sort == 'region':
        sortedList = sorted(Obj_list, key=lambda secgroup: secgroup.region)
    elif Sort == 'id':
        sortedList = sorted(Obj_list, key=lambda secgroup: secgroup.secgroup_id)
    else:
        # default
        sortedList = sorted(Obj_list, key=lambda secgroup: secgroup.vpc_id)

    for subObj in sortedList:
        if len(subObj.name) > 22:
            linename = subObj.name[0:22] + '*'
        else:
            linename = subObj.name
        printDict = {'secgroupid': subObj.secgroup_id,
                     'vpcid': "%-12s" % subObj.vpc_id,
                     'region': "%-9s" % subObj.region,
                     'rules': "%3i" % len(subObj.rules),
                     'name': "%-23s" % linename,
                     'description': subObj.description,
                     }
        print LINE.substitute(printDict)

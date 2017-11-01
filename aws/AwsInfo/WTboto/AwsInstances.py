"""
AWS Classes and functions for AwsInfo commands
"""
__author__ = 'eric sales'
__copyright__ = "Copyright 2017, WebTelemetry US Inc."
__version__ = "0.7.6"
__maintainer__ = "Larry Sellars"
__email__ = "larry.sellars@webtelemetry.us"
__status__ = "Production"

import json


class AWSinstance:
    def __init__(self, instance_obj):
        self.instance_id = instance_obj.id
        self.image_id = instance_obj.image_id
        self.vpc_id = instance_obj.vpc_id
        self.state = instance_obj.state
        self.launch_time = instance_obj.launch_time
        self.region = instance_obj.region.name
        self.subnet_id = instance_obj.subnet_id
        self.public_ip = instance_obj.ip_address
        self.private_ip = instance_obj.private_ip_address
        self.public_dns_name = instance_obj.dns_name
        self.key_name = instance_obj.key_name
        self.type = instance_obj.instance_type
        self.avail_zone = instance_obj.placement
        self.name = ''
        try:
            if 'Name' in instance_obj.tags.keys():
                self.name = instance_obj.tags['Name']
            self.tags = instance_obj.tags
        except AttributeError:
            self.tags = {}
            pass
        ## set list of groups ##
        self.security_groups = {}
        for grp in instance_obj.groups:
            self.security_groups[grp.id] = grp.name
        ## list of ebs_vols ##
        self.ebs_vols = {}
        for vol in instance_obj.block_device_mapping.keys():
            # vol is a dict with dev : block_dev_object #
            ## - size attribute doesn't work (need to file boto bug) - ##
            self.ebs_vols[vol] = instance_obj.block_device_mapping[vol].volume_id

    def __repr__(self):
        ret = {'instance_id': self.instance_id,
               'image_id': self.image_id,
               'vpc_id': self.vpc_id,
               'name': self.name,
               'state': self.state,
               'launch_time': self.launch_time,
               'region': self.region,
               'avail_zone': self.avail_zone,
               'type': self.type,
               'key_name': self.key_name,
               'subnet_id': self.subnet_id,
               'public_ip': self.public_ip,
               'private_ip': self.private_ip,
               'public_dns_name': self.public_dns_name,
               'tags': self.tags,
               'security_groups': self.security_groups,
               'ebs_vols': self.ebs_vols,
               }
        return repr(ret)

    def json(self):
        """
        Method to return objects in json/dict format
        """
        ret = {self.instance_id: {'vpc_id': self.vpc_id,
                                  'image_id': self.image_id,
                                  'name': self.name,
                                  'state': self.state,
                                  'launch_time': self.launch_time,
                                  'region': self.region,
                                  'avail_zone': self.avail_zone,
                                  'subnet_id': self.subnet_id,
                                  'type': self.type,
                                  'key_name': self.key_name,
                                  'public_ip': self.public_ip,
                                  'private_ip': self.private_ip,
                                  'public_dns_name': self.public_dns_name,
                                  'tags': self.tags,
                                  'security_groups': self.security_groups,
                                  'ebs_vols': self.ebs_vols,
                                  }}
        return json.dumps(ret)

    def keydict(self):
        r = {'vpc_id': self.vpc_id,
             'image_id': self.image_id,
             'name': self.name,
             'state': self.state,
             'launch_time': self.launch_time,
             'region': self.region,
             'avail_zone': self.avail_zone,
             'subnet_id': self.subnet_id,
             'type': self.type,
             'key_name': self.key_name,
             'public_ip': self.public_ip,
             'private_ip': self.private_ip,
             'public_dns_name': self.public_dns_name,
             'tags': self.tags,
             'security_groups': self.security_groups,
             'ebs_vols': self.ebs_vols,
             }
        return r


def printValues(Obj_list, Key):
    """
    Print out values of keys
    """
    objlist = []
    print "  Instance ID   %-25s  Name" % (Key)
    print " =================================================================="
    for obj in Obj_list:
        objlist.append((obj.instance_id, obj.keydict()[Key], obj.name))
    objlist.sort(key=lambda x: x[1])
    for o in objlist:
        print "  %s    %-25s  %s" % (o[0], o[1], o[2])


def printInstance(Obj_list, InstanceId):
    """
    Method to print details for a single instance json
    """
    from pprint import pprint
    for obj in Obj_list:
        if obj.instance_id == InstanceId:
            pprint(obj.json())
            return


def printInstances(Obj_list, Sort='vpc_id'):
    """
    Method to print the instances in a nicely formatted view
    """
    import string
    HEADER = """\
 instance_id   vpc_id        avail_zone      type       priv-IP         pub-IP           state      name              key_name
================================================================================================================================"""

    LINE = string.Template("""\
 $instanceid   $vpcid   $avail_zone  $type $privIP $pubIP  $state  $name  $keyname""")

    print HEADER
    ## sort options ##
    if Sort == 'zone':
        sortedList = sorted(Obj_list, key=lambda instance: instance.avail_zone)
    elif Sort == 'type':
        sortedList = sorted(Obj_list, key=lambda instance: instance.type)
    elif Sort == 'state':
        sortedList = sorted(Obj_list, key=lambda instance: instance.state)
    else:
        # default
        sortedList = sorted(Obj_list, key=lambda instance: instance.vpc_id)

    for subObj in sortedList:
        printDict = {'instanceid': subObj.instance_id,
                     'vpcid': "%-12s" % subObj.vpc_id,
                     'avail_zone': "%-9s" % subObj.avail_zone,
                     'type': "%-11s" % subObj.type,
                     'privIP': "%-15s" % subObj.private_ip,
                     'pubIP': "%-15s" % subObj.public_ip,
                     'name': "%-18s" % subObj.name,
                     'keyname': "%s" % subObj.key_name,
                     'state': "%-9s" % subObj.state,
                     'numVols': "%-2s" % str(len(subObj.ebs_vols)),
                     'groups': subObj.security_groups.keys()
                     }
        print LINE.substitute(printDict)

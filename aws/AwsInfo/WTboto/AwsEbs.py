"""
AWS Classes and functions for AwsInfo commands
"""
__author__ = 'eric sales'
__copyright__ = "Copyright 2017, WebTelemetry US Inc."
__version__ = "0.7.6"
__maintainer__ = "Larry Sellars"
__email__ = "larry.sellars@webtelemetry.us"
__status__ = "Production"


class AWSebs:
    def __init__(self, ebs_obj):
        self.id = ebs_obj.id
        self.status = ebs_obj.status
        self.region = ebs_obj.region
        self.zone = ebs_obj.zone
        self.type = ebs_obj.type
        self.size = ebs_obj.size
        self.tags = ebs_obj.tags
        self.create_time = ebs_obj.create_time

        self.device = ebs_obj.attach_data.device
        self.instance_id = ebs_obj.attach_data.instance_id
        self.state = ebs_obj.attach_data.status

    def __repr__(self):
        ret = {'id': self.id,
               'device': self.device,
               'instance_id': self.instance_id,
               'size': self.size,
               'status': self.status,
               'state': self.state,
               'region': self.region,
               'zone': self.zone,
               'type': self.type,
               'create_time': self.create_time,
               'tags': self.tags,
               }
        return repr(ret)

    def json(self):
        """
        Method to return objects in json/dict format
        """
        ret = {self.id: {'device': self.device,
                         'instance_id': self.instance_id,
                         'status': self.status,
                         'state': self.state,
                         'size': self.size,
                         'region': self.region,
                         'zone': self.zone,
                         'type': self.type,
                         'create_time': self.create_time,
                         'tags': self.tags,

                         }}
        return ret


def printEbsVol(Obj_list, VolId):
    """
    Method to print details for a single Ebs Vol json
    """
    from pprint import pprint
    for obj in Obj_list:
        if obj.id == VolId:
            pprint(obj.json())
            return


def printEbsVols(Obj_list, Sort='instance'):
    """
    Method to print the ebs volume info in a nicely formatted view
    """
    import string
    HEADER = """\
 vol_id        instance_id   device      size  zone          status        state     type        create_time
========================================================================================================================"""

    LINE = string.Template("""\
 $volid  $instanceId   $device $size  $zone  $status $state   $type  $createTime""")

    print HEADER
    ## sort options ##
    if Sort == 'state':
        sortedList = sorted(Obj_list, key=lambda ebs: ebs.state)
    elif Sort == 'zone':
        sortedList = sorted(Obj_list, key=lambda ebs: ebs.zone)
    elif Sort == 'size':
        sortedList = sorted(Obj_list, key=lambda ebs: ebs.size)
    elif Sort == 'create':
        sortedList = sorted(Obj_list, key=lambda ebs: ebs.create_time)
    else:
        # default
        sortedList = sorted(Obj_list, key=lambda ebs: ebs.instance_id)

    for ebsObj in sortedList:
        printDict = {'volid': ebsObj.id,
                     'instanceId': "%-11s" % ebsObj.instance_id,
                     'device': "%-10s" % ebsObj.device,
                     'size': "%5i" % ebsObj.size,
                     'zone': "%-12s" % ebsObj.zone,
                     'status': "%-10s" % ebsObj.status,
                     'state': "%10s" % ebsObj.state,
                     'type': "%-10s" % ebsObj.type,
                     'createTime': "%s" % ebsObj.create_time,
                     }
        print LINE.substitute(printDict)

#!/usr/bin/env python
#

import boto.ec2
import sys
from boto.exception import EC2ResponseError
from pprint import pprint

USAGE = "Usage: %s [stop,start,status,info] i-instance1 i-instance2 .." % sys.argv[0]
## update if you want to span across additional REGIONS ##
REGIONS = ['us-east-1', 'us-west-1', 'us-west-2']


def validate_cli(cmd, instances):
    # validate command
    if cmd in ('-h', '--help', '-?', 'help'):
        print  USAGE
        sys.exit(1)
    elif cmd in ('stop', 'start', 'status', 'state', 'info'):
        command = cmd
    else:
        print "Error: Unknown command '%s'" % cmd
        print USAGE
        sys.exit(1)

    # check for args
    if not instances:
        print "Missing arg(s)"
        print USAGE
        sys.exit(1)

    # check formatting
    for inst in instances:
        if not inst.startswith('i-'):
            print "Error: '%s' is not an instance identifier." % inst
            sys.exit(1)

    return (command, instances)


def instance_exists(ec2conn, instance):
    """
    Returns True or False if instance is found from ec2conn
    """
    try:
        ec2conn.get_all_instances(instance_ids=[instance])
    except EC2ResponseError:
        return False
    else:
        return True


def get_instance_name(ec2conn, instance):
    """
    Return Name Tag if exists
    """
    name = ''
    if instance_exists(ec2conn, instance):
        _inst = ec2conn.get_all_instances(instance_ids=[instance])
        _instobj = _inst[0].instances[0]
        try:
            if 'Name' in _instobj.tags.keys():
                name = _instobj.tags['Name']
        except AttributeError:
            pass
    return name


def display_status(ec2conns, instance_list):
    """
    Print status of each instance
    """
    for inst in instance_list:
        found = False
        for conn in ec2conns:
            if not found:
                if instance_exists(conn, inst):
                    _inst = conn.get_all_instances(instance_ids=[inst])
                    _instobj = _inst[0].instances[0]
                    state = _instobj.state
                    name = get_instance_name(conn, inst)
                    print "%s : %s    %s" % (inst, state, name)
                    found = True

        if not found:
            print "%s : <not_found>" % (inst)


def start_instances(ec2conns, instance_list):
    """
    Start each instance
    """
    for inst in instance_list:
        found = False
        for conn in ec2conns:
            if not found:
                if instance_exists(conn, inst):
                    _inst = conn.get_all_instances(instance_ids=[inst])
                    _instobj = _inst[0].instances[0]
                    name = get_instance_name(conn, inst)
                    if _instobj.state == 'stopped':
                        _instobj.start()
                        print "%s : STARTING   %s" % (inst, name)
                    else:
                        print "%s : %s    %s" % (inst, _instobj.state, name)
                    found = True

        if not found:
            print "%s : <not_found>" % (inst)


def stop_instances(ec2conns, instance_list):
    """
    Stop each instance
    """
    for inst in instance_list:
        found = False
        for conn in ec2conns:
            if not found:
                if instance_exists(conn, inst):
                    _inst = conn.get_all_instances(instance_ids=[inst])
                    _instobj = _inst[0].instances[0]
                    name = get_instance_name(conn, inst)
                    if _instobj.state == 'running':
                        _instobj.stop()
                        print "%s : STOPPING   %s" % (inst, name)
                    else:
                        print "%s : %s    %s" % (inst, _instobj.state, name)
                    found = True

        if not found:
            print "%s : <not_found>" % (inst)


def info_instances(ec2conns, instance_list):
    """
    display some basic instance info in json format
    """
    info = {}
    for inst in instance_list:
        found = False
        for conn in ec2conns:
            if not found:
                if instance_exists(conn, inst):
                    _inst = conn.get_all_instances(instance_ids=[inst])
                    _instobj = _inst[0].instances[0]
                    info[inst] = {
                        'name': get_instance_name(conn, inst),
                        'private_ip': _instobj.private_ip_address,
                        'region': _instobj.region.name,
                        'vpc': _instobj.vpc_id,
                        'state': _instobj.state,
                        'image_id': _instobj.image_id,
                        'launch_time': _instobj.launch_time,
                        'subnet_id': _instobj.subnet_id,
                        'public_ip': _instobj.ip_address,
                        'type': _instobj.instance_type,
                        'avail_zone': _instobj.placement,
                    }
                    found = True

        if not found:
            info[inst] = 'Not Found'

    return info


if __name__ == '__main__':
    try:
        _cmd = sys.argv[1]
        _instances = sys.argv[2:]
    except IndexError:
        print "Error: missing options."
        print USAGE
        sys.exit(1)

    cmd, instances = validate_cli(_cmd, _instances)

    aws_conns = []
    for region in REGIONS:
        ec2conn = boto.ec2.connect_to_region(region)
        aws_conns.append(ec2conn)

    if cmd in ('status', 'state'):
        display_status(aws_conns, instances)
    elif cmd == 'start':
        start_instances(aws_conns, instances)
    elif cmd == 'stop':
        stop_instances(aws_conns, instances)
    elif cmd == 'info':
        pprint(info_instances(aws_conns, instances), width=1)

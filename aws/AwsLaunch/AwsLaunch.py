#!/usr/bin/env python
"""
Create an Aws Instance with info from a Config yaml file
"""
USAGE = """\
  AwsLaunch.py --file=config_yaml --type=aws_type --profile=config_profile --name=hostname
    [ overrides ]

    Required args:
        --file      location of Yaml config file
        --profile   name of config profile defined from Yaml file
        --type      AWS Instance Type
        --name      hostname tag
    optional args:
        --ebs       name of ebs profile defined from Yaml file
        --ip        manually set the private IP address

    overrides:  ignore settings from config file using specified override
        example:
            eip:no

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
import yaml
from boto import ec2 as BotoEC2
from boto import vpc as BotoVPC
from time import sleep


def getAmiId(Region):
    """
    Return the Ubuntu AMI ID based on region
    """
    import urllib2
    cloudUrl = 'https://cloud-images.ubuntu.com/query/xenial/server/released.current.txt'
    resp = urllib2.urlopen(cloudUrl)
    relist = resp.read().split('\n')
    tomatch = ['ebs', 'amd64', 'paravirtual', Region]
    for line in relist:
        words = line.split()
        if set(tomatch) < set(words):
            return words[7]


class WebTelemetry_AWSinst:
    """
    WebTelemetry Aws Instance class defined from dictionary and Yaml file data
    """

    def __init__(self, argDict):
        """
        Class init required dictionary keys: [profile,name,type,file]
        """
        self.profile = argDict['profile']
        self.hostname = argDict['name']
        self.type = argDict['type']
        self.instance_id = ''
        self.eip = False
        self.pub_ip = ''
        self.eip_alloc_id = ''
        self.rootvol = None
        self.ACCESS = ''
        self.SECRET = ''
        self.domain = ''
        self.vpcid = ''
        self.region = ''
        self.rootkey = ''
        self.subnet = ''
        self.ami_id = ''
        self.cidr = ''
        self.groups = []
        self.ebs_type = 'standard'
        self.ebs_devices = {}
        self.priv_ip = None
        if 'ip' in argDict.keys():
            self.priv_ip = argDict['ip']

        # load in the yaml config file #
        _yamlraw = yaml.load(open(argDict['file']))
        # Load any defaults first ##
        if 'defaults' in _yamlraw.keys():
            _defaults = _yamlraw['defaults']
            for i in _defaults.keys():
                if i == 'domain':
                    self.domain = _defaults[i]
                if i == 'region':
                    self.region = _defaults[i]
                if i == 'rootvol_size':
                    self.rootvol = _defaults[i]
                if i == 'rootkey':
                    self.rootkey = _defaults[i]
                if i == 'vpcid':
                    self.vpcid = _defaults[i]
                if i == 'ami_id':
                    self.ami_id = _defaults[i]
                if i == 'default_group':
                    self.groups.append(_defaults[i])
                if i == 'AWS_ACCESS_KEY_ID':
                    self.ACCESS = _defaults[i]
                if i == 'AWS_SECRET_ACCESS_KEY':
                    self.SECRET = _defaults[i]

        # load profile info and overrides #
        _profile = _yamlraw[self.profile]
        for p in _yamlraw[self.profile].keys():
            if p == 'vpcid':
                self.vpcid = _profile[p]
            if p == 'ami_id':
                self.ami_id = _profile[p]
            if p == 'region':
                self.region = _profile[p]
            if p == 'rootvol_size':
                self.rootvol = _profile[p]
            if p == 'rootkey':
                self.rootkey = _profile[p]
            if p == 'default_group':
                self.groups.append(_profile[p])
            if p == 'subnet':
                self.subnet = _profile[p].keys()[0]
                self.cidr = _profile[p][self.subnet]
            if p == 'security_groups':
                self.groups += _profile[p]
            if p == 'eip':
                self.eip = _profile[p]

        # Get the recent Ubuntu AMI id if ami_id is not defined #
        if not self.ami_id:
            self.ami_id = getAmiId(self.region)
        # strip out .{{ product.url }} to better fit UI #
        self.nametag = "%s.%s" % (self.hostname, self.domain.replace('.{{ product.url }}', ''))

        # create Root Volume block device map #
        self.bdm = BotoEC2.blockdevicemapping.BlockDeviceMapping()
        dev_sda1 = BotoEC2.blockdevicemapping.EBSBlockDeviceType()
        dev_sda1.size = self.rootvol
        self.bdm['/dev/sda1'] = dev_sda1

        # load EBS profile if provided #
        if 'ebs' in argDict.keys():
            _ebsDev = _yamlraw['EBS_profiles'][argDict['ebs']]['devices']
            # _ebsType = _yamlraw['EBS_profiles'][argDict['ebs']]['type']
            for _dev in _ebsDev.keys():
                ebs_name = '/dev/%s' % (_dev)
                ebdev = BotoEC2.blockdevicemapping.EBSBlockDeviceType()
                ebdev.size = _ebsDev[_dev]
                self.bdm[ebs_name] = ebdev

    def overrides(self, overrides_list):
        """
        Process overrides specified from CLI
        """
        for ol in overrides_list:
            _key = ol.split(':')[0]
            _val = ol.split(':')[1]
            if _key == 'eip':
                if _val in ['no', 'NO', 'false', 'False', 'off']:
                    self.eip = False
                elif _val in ['yes', 'YES', 'true', 'True', 'on']:
                    self.eip = True
                continue
            if _key == 'domain':
                self.domain = _val
                continue
            if _key == 'rootkey':
                self.rootkey = _val
                continue

    def create_instance(self):
        """
        Method to create the instance, eip, ebs resources
        """
        if self.ACCESS and self.SECRET:
            boto.connect_vpc(self.ACCESS, self.SECRET)
        else:
            boto.connect_vpc()
        awsRegConn = BotoVPC.connect_to_region(self.region)
        ## Allocate new EIP if True - do this first to error out before Instance gets created ##
        if self.eip:
            _VpcEip = awsRegConn.allocate_address(domain='vpc')
            self.pub_ip = _VpcEip.public_ip
            self.eip_alloc_id = _VpcEip.allocation_id

        # Launch the instance #
        print "Launching instance: %s / %s / %s" % (self.hostname, self.type, self.region),
        sys.stdout.flush()
        AgReservation = awsRegConn.run_instances(image_id=self.ami_id, key_name=self.rootkey, subnet_id=self.subnet,
                                                 security_group_ids=self.groups, private_ip_address=self.priv_ip,
                                                 disable_api_termination=True, block_device_map=self.bdm,
                                                 instance_type=self.type, )
        # wait a few secs before pulling the Instance object #
        sleep(5)
        _AgInst = AgReservation.instances[0]
        self.instance_id = _AgInst.id
        self.avail_zone = _AgInst.placement
        print " ... done."
        print "Adding Name Tag.. ",
        sys.stdout.flush()
        # Create Tags here #
        _AgInst.add_tag("Name", self.nametag)
        print " ... done."
        print "Waiting for running state:",
        sys.stdout.flush()
        _count = 0
        while _AgInst.update() != 'running':
            sys.stdout.write('.')
            sys.stdout.flush()
            sleep(3)
            if _count >= 60:
                print "\n[Error] 3min timeout reached waiting for 'running' state."
                print "_current_state_ = %s" % _AgInst.update()
                sys.exit(2)
            _count += 1
        print "[running]"
        # Need to wait a few more secs for the private IP to get assigned #
        sleep(5)
        _AgInst.update()
        self.priv_ip = _AgInst.private_ip_address

        # Assign EIP if True #
        if self.eip:
            print "Assigning EIP: %s" % (self.pub_ip)
            awsRegConn.associate_address(self.instance_id, None, self.eip_alloc_id)
        return


def main(argv):
    """
    Parse out command line arguments for Aws launch
    """
    cliArgs = {}
    RequiredArgs = ['file', 'profile', 'name', 'type']
    overRides = []

    try:
        opts, args = getopt.getopt(argv, "hf:t:p:n:e:i:",
                                   ['help', 'file=', 'type=', 'profile=', 'name=', 'ebs=', 'ip='])
    except getopt.GetoptError:
        print "Missing args or options"
        print "usage: ", USAGE
        sys.exit(1)

    for opt, arg in opts:
        if opt in ("-h", "--help", "?", "help"):
            print USAGE
            sys.exit()
        elif opt in ('-f', '--file'):
            cliArgs['file'] = arg
            RequiredArgs.remove('file')
        elif opt in ('-p', '--profile'):
            cliArgs['profile'] = arg
            RequiredArgs.remove('profile')
        elif opt in ('-t', '--type'):
            cliArgs['type'] = arg
            RequiredArgs.remove('type')
        elif opt in ('-n', '--name'):
            cliArgs['name'] = arg
            RequiredArgs.remove('name')
        elif opt in ('-e', '--ebs'):
            cliArgs['ebs'] = arg
        elif opt in ('-i', '--ip'):
            cliArgs['ip'] = arg

    if RequiredArgs:
        print "Error: missing expected arg(s): ", RequiredArgs
        print "usage: ", USAGE
        sys.exit(1)

    for a in args:
        overRides.append(a)

    ## Check Args ##
    # test file exists
    # check IP is in subnet

    AgInst = WebTelemetry_AWSinst(cliArgs)
    if overRides:
        print "Processing overrides: ", overRides
        AgInst.overrides(overRides)
    print "Creating Instance"
    AgInst.create_instance()

    print "AWS Instance created with the following info:"
    print "  name: %s" % (AgInst.nametag)
    print """\
  instance_id: %s
  type: %s
  priv_ip: %s
  zone: %s
  subnet: %s
  keyname: %s""" % (AgInst.instance_id, AgInst.type, AgInst.priv_ip, AgInst.avail_zone, AgInst.cidr, AgInst.rootkey)
    if AgInst.eip:
        print "  eip: %s" % (AgInst.pub_ip)


if __name__ == "__main__":
    main(sys.argv[1:])

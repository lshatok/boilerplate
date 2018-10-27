################################################
__author__ = 'eric sales'
__copyright__ = "Copyright 2017, WildRiver Technologies Inc"
__version__ = "0.2.0"
__maintainer__ = "Larry Sellars"
__email__ = "larry.sellars@wildrivertechnologies.com"
__status__ = "production"
################################################
"""
WebTelemetry BootStrap Task Group: task_filesystem

    mounts  {create_mounts(mnt_info)}
    umount_ephemeral
    lvm_diskgroup(lvm_info)
"""
from fabric.api import *


def create_mounts(mnt_info):
    """
    TASK: mounts - create filesystems and mounts
    yaml config format

    mounts:
        <device_path> :  [ <mount_path>, xfs, "mount options" ]
    """
    for dev in mnt_info:
        print "starting mount for %s" % dev
        m_path = mnt_info[dev][0]
        fstype = mnt_info[dev][1]
        m_opts = mnt_info[dev][2]
        # Check if device exists
        if sudo('[ -e %s ] || echo "no"' % dev) == 'no':
            warn("   skipping - device %s not found." % dev)
            continue
        # Check if device is a partition
        if dev[-1:].isdigit():
            raise Exception('lvm_diskgroups - partitions not supported')
        # Check if device is already in use
        if sudo('blkid %s || echo "no"' % dev) != 'no':
            warn("   skipping - device %s is already in use" % dev)
            continue
        if sudo('[ -d %s ] && ls -A %s || echo ""' % (m_path, m_path)):
            warn("   skipping - path %s exists and is not empty" % m_path)
            continue
        sudo('mkdir -p %s && touch %s/Not_Mounted' % (m_path, m_path))
        sudo('mkfs.%s %s' % (fstype, dev))
        sudo('echo "%s    %s  %s  %s  0 0" >> /etc/fstab' % (dev, m_path, fstype, m_opts))
        sudo('mount %s' % m_path)
        print "   mounted %s to %s" % (dev, m_path)


def umount_ephemeral():
    """
    TASK: umount_ephemeral - unmount and remove /dev/xvdb from fstab
    """
    print "starting removal of AWS ephemeral mount (if found)."
    if sudo('grep "^/dev/xvdb " /etc/mtab || echo "no"') != 'no':
        print "  unmounting /mnt"
        sudo('umount /mnt')
    if sudo("grep '^/dev/xvdb ' /etc/fstab || echo 'no'") != 'no':
        print "  commenting out from /etc/fstab"
        sudo('sed -i "s/\/dev\/xvdb/\#\/dev\/xvdb/" /etc/fstab')


def lvm_diskgroup(lvm_info):
    """
    TASK: lvm_diskgroups - create lvm diskgroup and volume

    yaml config format
    lvm_diskgroup:
        <dg_name>:
            device:  /dev/xvdf
            volumes:
                <vol_name>: 100%
    """
    ## verify:  dg_name is avail, device is avail, vol is avail ##
    for lvm_dg in lvm_info.keys():
        print "start lvm_diskgroup creation: %s" % lvm_dg
        try:
            lvm_dev = lvm_info[lvm_dg]['device']
            lvm_vols = lvm_info[lvm_dg]['volumes']
        except KeyError:
            raise Exception('lvm_diskgroups - missing expected settings in yaml config')
        # check if device is a partition #
        if lvm_dev[-1:].isdigit():
            raise Exception('lvm_diskgroups - partitions not supported')
        # check for devices and availability #
        if sudo('[ -e %s ] || echo "no"' % lvm_dev) == 'no':
            print "   skipping: device %s not found" % lvm_dev
            continue
        # check if dev is mounted (mtab) #
        if sudo("""grep "^%s[' ',0-9]" /etc/mtab || echo 'no'""" % lvm_dev) != 'no':
            print "   skipping: device %s is mounted" % lvm_dev
            continue
        # check if dev is in pvdisplay #
        if sudo('pvdisplay %s >> /dev/null 2>&1 || echo "no"' % lvm_dev) != 'no':
            print "   skipping: device %s is already encapsulated" % lvm_dev
            continue
        sudo('pvcreate %s' % lvm_dev)
        # check for diskgroup #
        dg_exists = sudo('[ -d /dev/%s ] || echo "no"' % lvm_dg)
        if dg_exists != 'no':
            print "   skipping: diskgroup %s already exists"
            continue
        sudo('vgcreate %s %s' % (lvm_dg, lvm_dev))
        # create volumes #
        for vol in lvm_vols:
            size = lvm_info[lvm_dg]['volumes'][vol]
            lv_ext = size[-1:]
            lv_cmdsize = ''
            if lv_ext == '%':
                lv_cmdsize = '-l %sFREE' % size
            if lv_ext.upper() in ('M', 'G', 'T'):
                lv_cmdsize = '-L %s' % size
            if lv_cmdsize:
                sudo('lvcreate %s -n %s %s' % (lv_cmdsize, vol, lvm_dg))
            else:
                raise Exception('lvm_diskgroups - invalid yaml config format')

#!/usr/bin/env python
"""
Get the most recent Ubuntu AMI image published parsed from:
  https://cloud-images.ubuntu.com/query/xenial/server/released.current.txt
"""
USAGE = """\
   ubuntu-ami-locator.py --region [ --link | --info ]

   Returns AMI id for the EBS version of the Precise 64-bit Server
"""
__author__ = 'eric sales'

import getopt
import sys
import urllib2

cloudUrl = 'https://cloud-images.ubuntu.com/query/xenial/server/released.current.txt'


def getlist(Url):
    response = urllib2.urlopen(Url)
    releases = response.read()
    retlist = releases.split('\n')

    return retlist


def main(argv):
    arg_option = []
    region = ''
    EbsMatch = ''
    Ami = ''

    try:
        opts, args = getopt.getopt(argv, "hr:li",
                                   ['help', 'region=', 'link', 'info'])
    except getopt.GetoptError:
        print "usage: %s" % USAGE
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help", "?", "help"):
            print "usage: %s" % USAGE
            sys.exit()
        elif opt in ("-r", "--region"):
            region = arg
        elif opt == '--link':
            arg_option.append('link')
        elif opt == '--info':
            arg_option.append('info')

    if region:
        List = getlist(cloudUrl)
        for line in List:
            words = line.split()
            if 'ebs' in words and 'amd64' in words and 'paravirtual' in words and region in words:
                EbsMatch = line

    if EbsMatch:
        Ami = EbsMatch.split()[7]
        if 'link' in arg_option:
            print "https://console.aws.amazon.com/ec2/home?region=%s#launchAmi=%s" % (region, Ami)
        elif 'info' in arg_option:
            print EbsMatch
        else:
            print Ami


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except IndexError:
        print "usage: %s" % USAGE
        sys.exit(1)

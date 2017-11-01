#!/usr/bin/env python
#
USAGE = "  usage: devops-rotate-s3files.py [ grafana, telemetrix, signup, revassure, snmp ] [ #days_ago ] [-list | -remove]"
#
#
#  - get S3 file list for db and app
#  - class for s3file object
#  -   is older than (days) method
#  -   delete
#  -    

import sys
import yaml
from boto.s3.connection import S3Connection
from datetime import date, timedelta, datetime

# read IAM info from yaml file #
with open('.aws-iam.yml', 'r') as f:
    iam_info = yaml.load(f)['devops_rotate']

AWS_IAM = (iam_info['key'], iam_info['secret'])
s3bucket = 'com.webtelemetry-dev.dtech'

conn = S3Connection(AWS_IAM[0], AWS_IAM[1])
bucket = conn.get_bucket(s3bucket)

S3_OBJECTS = []
Prefix = ''
Suffix = '.gz'
s3bkup_path = 'backups'

avail_opts1 = ['grafana', 'telemetrix', 'signup', 'revassure', 'snmp']

if sys.argv[1] in ['help', '-h', '?', '--help', '-help']:
    print USAGE
    sys.exit()

if len(sys.argv) != 4:
    print "error: missing args or extra args"
    print USAGE
    sys.exit(1)

if sys.argv[1] not in avail_opts1:
    print "error: unknown arg %s" % sys.argv[1]
    print USAGE
    sys.exit(1)

if sys.argv[1] == 'grafana':
    app = 'grafana'
    Prefix = '%s/grafana/metrix_' % s3bkup_path
if sys.argv[1] == 'telemetrix':
    app = 'telemetrix'
    Prefix = '%s/telemetrix/telemetrix_' % s3bkup_path
if sys.argv[1] == 'revassure':
    app = 'revassure'
    Prefix = '%s/revassure/revassure_' % s3bkup_path
if sys.argv[1] == 'signup':
    app = 'signup'
    Prefix = '%s/signup/signup_' % s3bkup_path
if sys.argv[1] == 'snmp':
    app = 'snmp'
    Prefix = '%s/snmp/' % s3bkup_path

try:
    days_old = int(sys.argv[2])
except ValueError:
    print "error: days_ago arg is not a valid integer."
    print USAGE
    sys.exit(1)

if not sys.argv[3] in ['-list', '-remove']:
    print "error: action arg '%s' is unknown" % sys.argv[3]
    print USAGE
    sys.exit(1)
action_arg = sys.argv[3]


class S3backup_object:
    def __init__(self, s3file, s3prefix):
        self.s3file = s3file
        self.date_string = s3file.lstrip(s3prefix).lstrip('db_').lstrip('APP_').split('_')[0]

    def older_than(self, daysold):
        daysago = date.today() - timedelta(days=daysold)
        s3obj_date = datetime.strptime(self.date_string, "%Y-%m-%d").date()
        return s3obj_date < daysago


for k in bucket.list():
    _kname = k.name.encode('utf-8')
    if _kname.startswith(Prefix) and _kname.endswith(Suffix):
        S3_OBJECTS.append(_kname)
        b = S3backup_object(_kname, Prefix)
        if b.older_than(days_old):
            if action_arg == '-list':
                print "list: ", b.s3file
            if action_arg == '-remove':
                print "removing: ", b.s3file
                k.delete()

print

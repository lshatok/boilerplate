#!/usr/bin/env python

import smtplib
import sys
from email.mime.text import MIMEText

try:
    subj = sys.argv[1]
    toaddr = sys.argv[2]
    messg = sys.argv[3]
except IndexError:
    print "Usage %s 'subject' 'to_email' 'message'" % sys.argv[0]
    sys.exit()

msg = MIMEText(messg)

msg['Subject'] = subj
msg['From'] = 'devops@wildrivertechnologies.com'
msg['To'] = toaddr

username = 'webtelemetry_dev'
password = 'tfvu8tac21s'

a = smtplib.SMTP('smtp.sendgrid.net:587')
a.starttls()
a.login(username, password)

a.sendmail('devops@wildrivertechnologies.com', toaddr, msg.as_string())
a.quit()

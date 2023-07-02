#!/usr/bin/env python3
import smtplib
import time
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime
import argparse

#testar git 
scriptVersion = 2.0

parser = argparse.ArgumentParser(description='Config email script')
parser.add_argument('-v', action='store_true', help='Display version')
parser.add_argument('-smtp', default='saexchange.sa.cruises.princess.com', help='ship smtp server')
parser.add_argument('-n', default='saradar@princesscruises.com', help='Radar2 email name')
parser.add_argument('-e', default='be-ea-iris@jci.com', help='to email')
parser.add_argument('-s', default='Marine Norrkoping_Sapphire_NB2180', help='email subject')
parser.add_argument('-b', default='send_email from radar2.0', help='email body message')
parser.add_argument('-f', default='/home/jci/mail/trend.txt.gz', help='attached file')
parser.add_argument('-p', default='25', help='email Port')
parser.add_argument('-passw', default='passw', help='password')
parser.add_argument('-user', default='user', help='user')
parser.add_argument('-usepass', default='FALSE', help='use password')
args = parser.parse_args()

if args.v:
    print('send_email_ver2 version ' + str(scriptVersion))

#set up  the smtp server

now = datetime.now()

server = smtplib.SMTP(host=args.smtp, port=int(args.p))
server.ehlo()
server.starttls()

if args.usepass=='true' or args.usepass=='TRUE':
    server.login(args.user,args.passw)
server.set_debuglevel(1)
print ('server working fine')

time.sleep(1)

msg = MIMEMultipart()
msg['From'] = args.n
msg['To'] = args.e
msg['Subject'] = args.s
body = args.b
msg.attach(MIMEText(body, 'plain'))

filename = args.f
if os.path.isfile(filename):
    print("fileexist hurra")
    with open(filename,'rb') as file:
    # Attach the file with filename to the email
        msg.attach(MIMEApplication(file.read(), Name=os.path.basename(filename)))
else:
    print('attached file missing '+ str(filename))
# convert message to string
text = msg.as_string()


#server.sendmail(sender, receivers, subject, msg)
server.send_message(msg)
print ('sending email to ' + msg['To'])
print(now)
server.quit()

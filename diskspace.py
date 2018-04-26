#!/usr/bin/python3

import subprocess
import smtplib
import socket
import os
from email.mime.text import MIMEText

#Sample SMTP configuration
SMTP_IP = 'smtp.example.com'
TO = 'root@example.com'
FROM = 'admin@example.com'

THRESHOLD = 90
FILENAME = '/tmp/diskspacewatcher'

body = ''

# Get server IP#
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.connect(("8.8.8.8", 80))
    ip = str(s.getsockname()[0])
print("Server: " + ip)

df = subprocess.Popen(["df","-h"], stdout=subprocess.PIPE)

for line in df.stdout:
     splitline = line.decode().split()
     # Check "/" and "/home" spaces
     if splitline[5] == "/" or splitline[5] == "/home":
         if float(splitline[4][:-1]) >= THRESHOLD:
             body += ('Uses: '+ str(splitline[5]) + ' => ' + str(splitline[4][:-1]) + '%\n')
             print(body)

if body:
    if os.path.exists(FILENAME):
        print('Notification email already sent.')
    else:
        print('Posting notification')
        msg = MIMEText( body + '\n')
        msg['Subject'] = '[DiskSpaceWatcher] Low disk space @' + ip
        msg['From'] = FROM
        msg['To'] = TO
        with smtplib.SMTP(SMTP_IP) as s:
            s.send_message(msg)
        os.mknod(FILENAME)
elif os.path.exists(FILENAME):
    print('Clear flag.')
    msg = MIMEText('Low disk space fixed.\n')
    msg['Subject'] = '[DiskSpaceWatcher] Low disk space fixed @' + ip
    msg['From'] = FROM
    msg['To'] = TO
    with smtplib.SMTP(SMTP_IP) as s:
        s.send_message(msg)    
    os.remove(FILENAME)

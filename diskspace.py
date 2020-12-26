#!/usr/bin/env python3

import smtplib
import socket
from email.mime.text import MIMEText
import shutil
import os

#Sample SMTP configuration
SMTP_IP = 'smtp.example.com'
TO = 'root@example.com'
FROM = 'admin@example.com'
THRESHOLD = 90
FILENAME = '/tmp/diskspacewatcher'
disks = ["/", "/home"]

body = ''

# Get server IP#
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.connect(("8.8.8.8", 80))
    ip = str(s.getsockname()[0])
print("Server: " + ip)

for disk in disks:
    du = shutil.disk_usage(disk)
    usage = (du.used/du.total)*100
    if usage >= THRESHOLD:
        body += "{} disk usage: {:0.2f}".format(disk, usage)
        print(body)

if body:
    if os.path.exists(FILENAME):
        print('Notification email already sent.')
    else:
        print('Posting notification')
        msg = MIMEText(body + '\n')
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

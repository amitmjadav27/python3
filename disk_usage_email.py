import shutil
import smtplib
import os
import smtplib
from email.message import EmailMessage
import socket

SYSTEM_NAME = socket.gethostname()
APP_PASSWORD = os.environ.get('GMAIL_PASSWORD') # export GMAIL_PASSWORD='16 character App password'
THRESHOLD = 30  # percent
EMAIL = 'amitmjadav007@gmail.com'

def check_disk_usage(path="/"):
    total, used, free = shutil.disk_usage(path)
    percent_used = used / total * 100
    return percent_used

usage = check_disk_usage("/")
print(f"Disk Usage is at {usage:.2f}%")

def send_alert():
    msg = EmailMessage()
    msg.set_content(
        f"""⚠️ Disk usage alert for system: {SYSTEM_NAME}

        Current usage: {usage:.2f}%
        Threshold: {THRESHOLD}%

        Please take action to free up disk space.
        """)
    msg['Subject'] = f'Disk Alert: {SYSTEM_NAME} at {usage:.2f}% usage'
    msg['From'] = EMAIL
    msg['To'] = EMAIL


    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL, APP_PASSWORD)
        smtp.send_message(msg)

if usage > THRESHOLD:
   send_alert()
else:
    print(f"Disk usage is OK: {usage:.2f}% on {SYSTEM_NAME}")


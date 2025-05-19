import requests
import smtplib
import os
from email.mime.text import MIMEText
#from slack_sdk import WebClient
#from slack_sdk.errors import SlackApiError

# ========== Configuration ==========

WEBSITE_LIST_FILE = "websites.txt"

# Slack Configuration
#SLACK_TOKEN = "xoxb-your-slack-token"
#SLACK_CHANNEL = "#alerts"

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "amitmjadav007@gmail.com"
EMAIL_PASSWORD = os.environ.get('GMAIL_PASSWORD') # export GMAIL_PASSWORD='16 character App password'
ALERT_RECIPIENT = "amitmjadav008@gmail.com"

# ===================================


def load_websites(file_path):
    try:
        with open(file_path, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Website list file not found: {file_path}")
        return []


#def send_slack_alert(message):
#    client = WebClient(token=SLACK_TOKEN)
#    try:
#        response = client.chat_postMessage(channel=SLACK_CHANNEL, text=message)
#        print(f"Slack alert sent: {response['message']['text']}")
#    except SlackApiError as e:
#        print(f"Slack Error: {e.response['error']}")


def send_email_alert(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ALERT_RECIPIENT

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
            print("Email alert sent.")
    except Exception as e:
        print(f"Email Error: {e}")


def check_websites(websites):
    for url in websites:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                message = f"⚠️ Website Down: {url} (Status: {response.status_code})"
#                send_slack_alert(message)
                send_email_alert("Website Down Alert", message)
        except requests.exceptions.RequestException as e:
            message = f"❌ Error accessing {url}: {e}"
#            send_slack_alert(message)
            send_email_alert("Website Access Error", message)


if __name__ == "__main__":
    websites = load_websites(WEBSITE_LIST_FILE)
    if websites:
        check_websites(websites)
    else:
        print("No websites to check.")


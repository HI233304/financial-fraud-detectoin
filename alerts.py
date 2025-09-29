import os, smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
load_dotenv()
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
ALERT_TO = os.getenv("ALERT_TO")

def send_alert(subject, body):
    if not (SMTP_HOST and SMTP_USER and SMTP_PASS and ALERT_TO):
        return False
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SMTP_USER
    msg['To'] = ALERT_TO
    try:
        s = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        s.starttls()
        s.login(SMTP_USER, SMTP_PASS)
        s.sendmail(SMTP_USER, [ALERT_TO], msg.as_string())
        s.quit()
        return True
    except Exception:
        return False

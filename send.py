import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()
GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")


def send_email(to, subject, body):

    #Build the email
    msg = MIMEMultipart()
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = to
    msg["Subject"] = subject

    #Put letter inside the envelope
    msg.attach(MIMEText(body, "plain"))

    #Connect to Gmails SMTP server and send the email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_ADDRESS, to, msg.as_string())
        print(f"Email sent to {to} with subject: {subject}")


if __name__ == "__main__":
    send_email(
        to="saltoanthony13@gmail.com",
        subject="Test from my email authenticator",
        body="This is a test email sent from my AI email automator project using Python!"
)
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()
GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

def format_html(body):
    #Plain Text -> Clean HTML formatting

    paragraphs = [p.strip() for p in body.split("\n") if p.strip()]
    html_paragraphs = ""

    for p in paragraphs:
        html_paragraphs += f"<p>{p}</p>\n"
    
    return f"""
    <html>
        <body style="font-family: Aria, sans-serif; max-width:600px; margin: 0 auto; padding: 20px; color: #333;">
            <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                <h2 style="color: #2c3e50; margin: 0;">Your Daily AI Newsletter</h2>
            </div>
            <div style="line-height: 1.8; font-size: 15px;">
                {html_paragraphs}
            </div>
            <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eeel; font-size: 12px; color: #999;">
                <p> You're receiving this email because you are subscribed to this newsletter.</p>
            </div>
        </body>
    </html>
    """
                


def send_email(to, subject, body):

    #Build the email
    msg = MIMEMultipart("alternative") #"alternative" means email carries both plain & HTML text
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = to
    msg["Subject"] = subject

    #Plain text version -> Old email clients
    plain = MIMEText(body, "plain")

    #HTML version -> modern clients will see this
    html = MIMEText(format_html(body), "html")

    #Plain first, HTML second
    msg.attach(plain)
    msg.attach(html)

    #Connect to Gmails SMTP server and send the email
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_ADDRESS, to, msg.as_string())
            print(f"Email sent to {to} with subject: {subject}")
    except smtplib.SMTPAuthenticationError:
        raise RuntimeError(f"Gmail Authentication Failed: Check your password in .env")
    except smtplib.SMTPException as e:
        raise RuntimeError(f"Gmail failed to send email: {e}")

if __name__ == "__main__":
    send_email(
        to="saltoanthony13@gmail.com",
        subject="Test from my email authenticator",
        body="This is a test email sent from my AI email automator project using Python!"
)
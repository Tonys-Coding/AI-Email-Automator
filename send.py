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
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; color: #333;">

            <div style="background-color: #2c3e50; padding: 24px; border-radius: 8px 8px 0 0;">
                <h1 style="color: white; margin: 0; font-size: 22px;">Your Daily Newsletter</h1>
            </div>

            <div style="background: #ffffff; padding: 24px; border: 1px solid #eee; border-top: none; border-radius: 0 0 8px 8px; line-height: 1.8; font-size: 15px;">
                {body}
            </div>

            <div style="margin-top: 20px; font-size: 12px; color: #999; text-align: center;">
                <p>You're receiving this because you subscribed to this newsletter.</p>
            </div>

        </body>
    </html>
    """

def plain_text(body):
    #Stripping html tags for plain text alternative
    import re
    return re.sub(r'<[^>]+>', '', body)
                


def send_email(to, subject, body):

    #Build the email
    msg = MIMEMultipart("alternative") #"alternative" means email carries both plain & HTML text
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = to
    msg["Subject"] = subject


    #Plain first, HTML second
    msg.attach(MIMEText(plain_text(body), "plain"))
    msg.attach(MIMEText(format_html(body), "html"))

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
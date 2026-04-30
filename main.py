import logging
import os 
from dotenv import load_dotenv
from generate import generate_email
from send import send_email
import json
import re

load_dotenv()

# Setting up logging to terminal and logs.txt
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs.txt"),
        logging.StreamHandler()
    ]
)


#Loading Configurations from config.json
with open("config.json", "r") as f:
    config = json.load(f)

email_config = config["email"]

#Run the email generation and sending process
if __name__ == "__main__":
    #Generate email content
    logging.info("Starting email automator..")

    try:
        logging.info("Generating email...")
        email_body = generate_email(
            topic=email_config["topic"],
            audience=email_config["audience"],
            tone=email_config["tone"]
        )

        subject_match = re.search(r'<strong>Subject:</strong>\s*(.*?)</p>', email_body)
        
        if subject_match:
            subject = subject_match.group(1).strip()
            #Remove subject line from body
            body = re.sub(r'<p><strong>Subject:</strong>.*?</p>', '', email_body, count=1)
        else:
            subject = email_config["topic"]
            body = email_body

        logging.info(f"Subject: {subject}")
        

        for recipient in email_config["recipients"]:
            send_email(to=recipient, subject=subject, body=body)
            logging.info(f"Email sent to {recipient}")
        
        logging.info("Email automator process completed successfully.")

    except Exception as e:
        logging.error(f"Automator process failed: {e}")
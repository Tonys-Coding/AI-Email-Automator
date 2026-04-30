from flask import Flask, render_template, request, jsonify
import json
import threading
import os
from main import generate_email, send_email
from dotenv import load_dotenv
import re

load_dotenv()
app = Flask(__name__)



@app.route("/")
def home():
    with open("config.json") as f:
        config = json.load(f)
    return render_template("index.html", config=config["email"])


@app.route("/save", methods={"POST"})
def save():
    data = request.json
    with open("config.json", "w") as f:
        json.dump({"email": data}, f, indent=4)
    return jsonify({"status": "saved"})

@app.route("/send", methods=["POST"])
def send():
    def run():
        try:
            with open("config.json") as f:
                config = json.load(f)["email"]
            
            email_body = generate_email(
                topic=config["topic"],
                audience=config["audience"],
                tone=config["tone"]
            )
        
            subject_match = re.search(r'<strong>Subject:</strong>\s*(.*?)</p>', email_body)
            subject = subject_match.group(1).strip() if subject_match else config["topic"]
            body = re.sub(r'<p><strong>Subject:</strong>.*?</p>', '', email_body, count=1)

            for recipient in config["recipients"]:
                send_email(to=recipient, subject=subject, body=body)
        except Exception as e:
            print(f'Error: {e}')

    #Runs in the background so the browser gets instant response times
    thread = threading.Thread(target=run)
    thread.start()
    return jsonify({"status": "Sending..."})

@app.route("/logs")
def logs():
    if os.path.exists("logs.txt"):
        with open("logs.txt") as f:
            lines = f.readlines()
        return jsonify({"logs ": lines[-20:]}) #last 20 lines
    return jsonify({"logs": []})

if __name__ == "__main__":
    app.run(debug=True)
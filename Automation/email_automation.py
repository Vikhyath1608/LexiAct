from flask import Flask, request, jsonify
import os
import json
import re
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from meta_ai_api import MetaAI

app = Flask(__name__)

# Load environment variables
load_dotenv()
FROM_EMAIL = os.getenv("FROM_EMAIL")
FROM_PASSWORD = os.getenv("FROM_PASSWORD")
YOUR_NAME = os.getenv("YOUR_NAME", "Your Name")
CONTACTS_FILE = 'contacts.json'

def load_contacts():
    with open(CONTACTS_FILE, 'r') as f:
        return json.load(f)

def parse_input(user_input, contacts):
    contact_name = None
    for name in contacts.keys():
        if name.lower() in user_input.lower():
            contact_name = name
            break
    if not contact_name:
        return None, None
    message_idea = user_input.lower().replace(f"send the email to {contact_name.lower()}", "").strip()
    message_idea = message_idea.replace(f"send email to {contact_name.lower()}", "").strip()
    return contact_name, message_idea

def generate_subject_and_body(prompt_text, mode="new", existing_subject="", existing_body="", user_changes=""):
    ai = MetaAI()

    if mode == "edit":
        prompt = (
            f"You are an email writer assistant. Here is the current email subject and body:\n"
            f"Subject: {existing_subject}\n"
            f"Body: {existing_body}\n"
            f"\nApply these user-requested changes: {user_changes}.\n"
            "Return ONLY a JSON object in this exact format:\n"
            "{\n  \"subject\": \"Your subject here\",\n  \"body\": \"Your body here\"\n}"
        )
    else:
        prompt = (
            f"Generate a professional email based on this idea: '{prompt_text}'. "
            "Always return a JSON object ONLY in this exact format:\n"
            "{\n  \"subject\": \"Your subject here\",\n  \"body\": \"Your body here\"\n}"
        )

    response = ai.prompt(message=prompt)

    subject, body = "", ""
    if isinstance(response, dict):
        message_field = response.get('message', '')
        try:
            json_data = json.loads(message_field)
            subject = json_data.get('subject', '')
            body = json_data.get('body', '')
        except json.JSONDecodeError:
            print("❌ Failed to parse JSON from AI response.")

    return subject.strip(), body.strip()

def personalize_body(body, recipient_real_name):
    patterns = [r"\[Your Name\]", r"\{Your Name\}", r"\<Your Name\>", r"\bYour Name\b"]
    for pattern in patterns:
        body = re.sub(pattern, YOUR_NAME, body)

    patterns = [r"\[Recipient Name\]", r"\{Recipient Name\}", r"\<Recipient Name\>", r"\bRecipient Name\b"]
    for pattern in patterns:
        body = re.sub(pattern, recipient_real_name, body)

    return body

def personalize_subject(subject, recipient_real_name):
    if recipient_real_name and recipient_real_name not in subject:
        if any(word in subject.lower() for word in ["request", "leave", "approval"]):
            subject += f" for {recipient_real_name}"
        elif any(word in subject.lower() for word in ["meeting", "catch up", "check", "update"]):
            subject += f" with {recipient_real_name}"
        else:
            subject += f" - {recipient_real_name}"
    return subject

def capitalize_name(name):
    return ' '.join(part.capitalize() for part in name.split())

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    user_input = data.get("input", "")
    contacts = load_contacts()
    contact_key, message_idea = parse_input(user_input, contacts)

    if not contact_key or not message_idea:
        return jsonify({"error": "Could not parse contact or message."}), 400

    contact_info = contacts[contact_key]
    recipient_email = contact_info["email"]
    recipient_real_name = capitalize_name(contact_info.get("name", contact_key))

    subject, body = generate_subject_and_body(message_idea)
    if not subject:
        subject = message_idea.capitalize()
    if not body:
        body = f"Hi {recipient_real_name},\n\n{message_idea.capitalize()}.\n\nBest regards,\n{YOUR_NAME}"

    body = personalize_body(body, recipient_real_name)
    subject = personalize_subject(subject, recipient_real_name)

    return jsonify({
        "recipient_email": recipient_email,
        "recipient_name": recipient_real_name,
        "subject": subject,
        "body": body
    })

@app.route("/edit", methods=["POST"])
def edit():
    data = request.json
    message_idea = data.get("idea", "")
    user_changes = data.get("changes", "")
    subject = data.get("subject", "")
    body = data.get("body", "")
    recipient_name = data.get("recipient_name", "")

    new_subject, new_body = generate_subject_and_body(
        prompt_text=message_idea,
        mode="edit",
        existing_subject=subject,
        existing_body=body,
        user_changes=user_changes
    )
    new_subject = personalize_subject(new_subject, recipient_name)
    new_body = personalize_body(new_body, recipient_name)

    return jsonify({
        "subject": new_subject,
        "body": new_body
    })

@app.route("/send", methods=["POST"])
def send():
    data = request.json
    to_email = data.get("to_email")
    subject = data.get("subject")
    body = data.get("body")

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email
    msg.set_content(body)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(FROM_EMAIL, FROM_PASSWORD)
            smtp.send_message(msg)
        return jsonify({"status": "✅ Email sent successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5002, debug=True)

import os
import json
import re
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from meta_ai_api import MetaAI

# Load .env configs
load_dotenv()
FROM_EMAIL = os.getenv("FROM_EMAIL")
FROM_PASSWORD = os.getenv("FROM_PASSWORD")
YOUR_NAME = os.getenv("YOUR_NAME", "Your Name")

CONTACTS_FILE = 'contacts.json'

def load_contacts():
    with open(CONTACTS_FILE, 'r') as f:
        return json.load(f)

def parse_input(user_input, contacts):
    # Extract contact name
    contact_name = None
    for name in contacts.keys():
        if name.lower() in user_input.lower():
            contact_name = name
            break
    if not contact_name:
        return None, None

    # Extract message idea (remove 'send email to [name]' or 'send the email to [name]' part)
    message_idea = user_input.lower().replace(f"send the email to {contact_name.lower()}", "").strip()
    message_idea = message_idea.replace(f"send email to {contact_name.lower()}", "").strip()
    return contact_name, message_idea

def generate_subject_and_body(prompt_text):
    ai = MetaAI()
    response = ai.prompt(message=f"Generate a professional email with subject and body based on: '{prompt_text}'. Return only as JSON with 'subject' and 'body' keys.")

    if isinstance(response, dict):
        subject = response.get('subject', '')
        body = response.get('body', '')
    else:
        subject = ""
        body = response.strip()

    return subject.strip(), body.strip()

def personalize_body(body, recipient_real_name):
    # Fix [Your Name]
    name_placeholders = [
        r"\[Your Name\]", r"\{Your Name\}", r"\<Your Name\>", r"\bYour Name\b"
    ]
    for pattern in name_placeholders:
        body = re.sub(pattern, YOUR_NAME, body)

    # Fix [Recipient Name]
    recipient_placeholders = [
        r"\[Recipient Name\]", r"\{Recipient Name\}", r"\<Recipient Name\>", r"\bRecipient Name\b"
    ]
    for pattern in recipient_placeholders:
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

def send_email(to_email, subject, body):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email
    msg.set_content(body)

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(FROM_EMAIL, FROM_PASSWORD)
        smtp.send_message(msg)

    print("✅ Email sent successfully!")

def capitalize_name(name):
    return ' '.join(part.capitalize() for part in name.split())

def main():
    contacts = load_contacts()

    user_input = input("Enter your command (e.g., 'send the email to vicky requesting for sick leave'): ")
    contact_key, message_idea = parse_input(user_input, contacts)

    if not contact_key or not message_idea:
        print("❌ Could not parse contact or message.")
        return

    contact_info = contacts[contact_key]
    recipient_email = contact_info.get("email")
    recipient_real_name = capitalize_name(contact_info.get("name", contact_key))

    print("⏳ Generating subject and email body using MetaAI...")
    subject, body = generate_subject_and_body(message_idea)

    # Fallback if failed
    if not subject:
        subject = message_idea.capitalize()
    if not body:
        body = f"Hi {recipient_real_name},\n\n{message_idea.capitalize()}.\n\nBest regards,\n{YOUR_NAME}"

    # Personalize subject and body
    body = personalize_body(body, recipient_real_name)
    subject = personalize_subject(subject, recipient_real_name)

    print(f"\nSubject: {subject}")
    print(f"Body:\n{body}\n")

    confirm = input("Do you want to send this email? (yes/no): ")
    if confirm.lower() == 'yes':
        send_email(recipient_email, subject, body)
    else:
        print("❌ Email sending canceled.")

if __name__ == "__main__":
    main()

import json
import re
import os

# Words to remove globally from commands
REMOVE_WORDS = {'the', 'in'}

def load_contacts(file_path='contacts.json'):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump({}, f)
        return {}
    with open(file_path, 'r') as f:
        return json.load(f)

def save_contacts(contacts, file_path='contacts.json'):
    with open(file_path, 'w') as f:
        json.dump(contacts, f, indent=2)

def normalize_spaces(text):
    return re.sub(r'\s+', ' ', text).strip()

def remove_unwanted_words(text):
    return ' '.join([word for word in text.split() if word.lower() not in REMOVE_WORDS])

def clean_command(command):
    command = normalize_spaces(command)
    command = remove_unwanted_words(command)
    return command

def add_contact_from_command(command, file_path='contacts.json'):
    output = []
    command = clean_command(command)

    match = re.match(r'add (.+?) with email (\S+) to contact', command, re.IGNORECASE)
    if not match:
        output.append("Invalid command format.")
        output.append("Correct format: add <Name> with email <email@example.com> to contact")
        return '\n'.join(output)

    name = normalize_spaces(match.group(1))
    email = normalize_spaces(match.group(2))
    key = name.lower().replace(' ', '')

    contacts = load_contacts(file_path)
    contacts[key] = {
        "email": email,
        "name": name
    }

    save_contacts(contacts, file_path)
    output.append(f"Added {name} with email {email}.")
    return '\n'.join(output)

def change_contact_name(command, file_path='contacts.json'):
    output = []
    command = clean_command(command)

    match = re.match(r'change contact name of (\S+) to (.+)', command, re.IGNORECASE)
    if not match:
        output.append("Invalid command format.")
        output.append("Correct format: change contact name of <OldName> to <NewName>")
        return '\n'.join(output)

    old_name = match.group(1).strip().lower()
    new_name = normalize_spaces(match.group(2))

    contacts = load_contacts(file_path)

    if old_name not in contacts:
        output.append(f"Contact with name {old_name} does not exist.")
        return '\n'.join(output)

    contacts[old_name]['name'] = new_name
    save_contacts(contacts, file_path)
    output.append(f"Updated contact name from {old_name} to {new_name}.")
    return '\n'.join(output)

def change_contact_email(command, file_path='contacts.json'):
    output = []
    command = clean_command(command)

    match = re.match(r'change email of (\S+) to (\S+)', command, re.IGNORECASE)
    if not match:
        output.append("Invalid command format.")
        output.append("Correct format: change email of <Name> to <NewEmail>")
        return '\n'.join(output)

    name = match.group(1).strip().lower()
    new_email = normalize_spaces(match.group(2))

    contacts = load_contacts(file_path)

    if name not in contacts:
        output.append(f"Contact with name {name} does not exist.")
        return '\n'.join(output)

    contacts[name]['email'] = new_email
    save_contacts(contacts, file_path)
    output.append(f"Updated {name}'s email to {new_email}.")
    return '\n'.join(output)

def handle_contact_command(user_command):
    file_path = r'D:\Projects\lexiAct\LAM\Flask_app\Automation\contacts.json'
    user_command_cleaned = normalize_spaces(user_command)

    if user_command_cleaned.lower().startswith('change contact name of'):
        return change_contact_name(user_command_cleaned, file_path)
    elif user_command_cleaned.lower().startswith('change email of'):
        return change_contact_email(user_command_cleaned, file_path)
    elif user_command_cleaned.lower().startswith('add'):
        return add_contact_from_command(user_command_cleaned, file_path)
    else:
        return "\n".join([
            "Invalid command.",
            "Supported formats:",
            "- add <Name> with email <email@example.com> to contact",
            "- change contact name of <OldName> to <NewName>",
            "- change email of <Name> to <NewEmail>"
        ])

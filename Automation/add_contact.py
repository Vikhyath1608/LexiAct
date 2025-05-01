import json
import re

# Words to remove globally from commands
REMOVE_WORDS = {'the', 'in'}

def load_contacts(file_path='contacts.json'):
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
    print(f"Received command: {command}")

    # Clean the whole command first
    command = clean_command(command)

    match = re.match(r'add (.+?) with email (\S+) to contact', command, re.IGNORECASE)
    
    if not match:
        print("Invalid command format.")
        print("Correct format: add <Name> with email <email@example.com> to contact")
        return

    name = normalize_spaces(match.group(1))
    email = normalize_spaces(match.group(2))

    key = name.lower().replace(' ', '')

    contacts = load_contacts(file_path)

    contacts[key] = {
        "email": email,
        "name": name
    }

    save_contacts(contacts, file_path)
    print(f"Added {name} with email {email}.")

def change_contact_name(command, file_path='contacts.json'):
    command = clean_command(command)

    match = re.match(r'change contact name of (\S+) to (.+)', command, re.IGNORECASE)
    if not match:
        print("Invalid command format.")
        print("Correct format: change contact name of <OldName> to <NewName>")
        return

    old_name = match.group(1).strip().lower()
    new_name = normalize_spaces(match.group(2))

    contacts = load_contacts(file_path)

    if old_name not in contacts:
        print(f"Contact with name {old_name} does not exist.")
        return

    contacts[old_name]['name'] = new_name

    save_contacts(contacts, file_path)
    print(f"Updated contact name from {old_name} to {new_name}.")

def change_contact_email(command, file_path='contacts.json'):
    command = clean_command(command)

    match = re.match(r'change email of (\S+) to (\S+)', command, re.IGNORECASE)
    if not match:
        print("Invalid command format.")
        print("Correct format: change email of <Name> to <NewEmail>")
        return

    name = match.group(1).strip().lower()
    new_email = normalize_spaces(match.group(2))

    contacts = load_contacts(file_path)

    if name not in contacts:
        print(f"Contact with name {name} does not exist.")
        return

    contacts[name]['email'] = new_email

    save_contacts(contacts, file_path)
    print(f"Updated {name}'s email to {new_email}.")

# Main command handler
user_command = input("Enter command: ")

# Always normalize spaces first
user_command_cleaned = normalize_spaces(user_command)
print(f"Entered command: {user_command_cleaned}")

if user_command_cleaned.lower().startswith('change contact name of'):
    change_contact_name(user_command_cleaned)
elif user_command_cleaned.lower().startswith('change email of'):
    change_contact_email(user_command_cleaned)
elif user_command_cleaned.lower().startswith('add'):
    add_contact_from_command(user_command_cleaned)
else:
    print("Invalid command.")
    print("Supported formats:")
    print("- add <Name> with email <email@example.com> to contact")
    print("- change contact name of <OldName> to <NewName>")
    print("- change email of <Name> to <NewEmail>")

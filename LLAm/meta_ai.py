from meta_ai_api import MetaAI

ai = MetaAI()
response = ai.prompt(message="wite a mail to HR requesting for 3 days leave")

def format_response(response):
    # Extract the message content
    message = response.get('message', '')
    
    # Split the message into lines
    lines = message.split('\n')
    
    formatted_response = ''
    in_day_section = False
    
    for line in lines:
        if line.startswith('Day'):
            # For day sections, add bold and newline
            formatted_response += f"\n### **{line.strip()}**\n"
            in_day_section = True
        elif line.strip() and in_day_section and not line[0].isdigit():
            # For time and activity entries under a day section
            formatted_response += f"- **{line.strip()}**\n"
        elif line.strip() and in_day_section:
            # Sub-activities or other descriptive lines (like timings or locations)
            formatted_response += f"  - {line.strip()}\n"
        elif not line.strip() and in_day_section:
            # Empty line, means end of a day section
            in_day_section = False
        else:
            # If not in a day section, just append the lines
            formatted_response += f"{line.strip()}\n"

    return formatted_response

# Format and print the response
formatted_output = format_response(response)
print(formatted_output)

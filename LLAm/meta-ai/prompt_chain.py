from meta_ai_api import MetaAI

# Initialize MetaAI object
ai = MetaAI()

# First prompt: Get the initial prompt from the user
prompt_input = input("Enter the initial prompt: ")

# First response: Get a response from MetaAI using the initial prompt
response = ai.prompt(message=prompt_input)

# Function to format the response
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

# Format the first response
formatted_output = format_response(response)

# Print the formatted response
print("Formatted Response:\n", formatted_output)

# Second prompt: Ask for the next action based on the formatted response
next_action = input("What would you like to do next? (e.g., 'summarize', 'analyze', etc.): ")

# Chain the next action (e.g., summarize the formatted response)
if next_action.lower() == "summarize":
    next_prompt = f"Summarize the following formatted response:\n{formatted_output}"
    second_response = ai.prompt(message=next_prompt)
    print("Summarized Response:\n", second_response['message'])
elif next_action.lower() == "analyze":
    next_prompt = f"Analyze the following formatted response:\n{formatted_output}"
    second_response = ai.prompt(message=next_prompt)
    print("Analysis:\n", second_response['message'])
else:
    print("Unknown action. Please try again.")

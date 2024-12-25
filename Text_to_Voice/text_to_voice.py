import pyttsx3

def text_to_voice(text):
    """Converts the given text to speech."""
    try:
        # Initialize the pyttsx3 engine
        engine = pyttsx3.init()
        
        # Optionally, you can set properties like volume, rate, and voice
        engine.setProperty('rate', 150)  # Speed of speech
        engine.setProperty('volume', 0.9)  # Volume level (0.0 to 1.0)
        
        # Get available voices (optional: you can choose a specific voice)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)  # Choose a specific voice (0, 1, etc.)
        
        # Say the text and wait for it to finish
        engine.say(text)
        engine.runAndWait()
    
    except Exception as e:
        print("An error occurred while converting text to voice:", e)

if __name__ == "__main__":
    while True:
        user_input = input("Enter the text you want to convert to speech (or type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            print("Exiting the program. Goodbye!")
            break
        text_to_voice(user_input)

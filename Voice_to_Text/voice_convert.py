import speech_recognition as sr
import logging

# Configure logging for error handling
logging.basicConfig(filename="recognizer_errors.log", level=logging.ERROR)

# Initialize recognizer
recognizer = sr.Recognizer()

# Function to listen and convert speech to text
def listen_and_recognize(timeout=15, phrase_time_limit=5):
    with sr.Microphone() as source:
        print("Adjusting for ambient noise, please wait...")
        recognizer.adjust_for_ambient_noise(source, duration=2)  # Adjust for ambient noise for 2 seconds
        print("Listening... (Say 'stop listening' to end)")

        while True:
            try:
                audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)  
                print("Recognizing...")
                text = recognizer.recognize_google(audio)  
                print(f"Recognized Text: {text}")
                
                if text.lower() == "stop listening":
                    print("Stopping the listening process.")
                    break
            
            except sr.UnknownValueError:
                print("Sorry, I could not understand the audio.")
            except sr.RequestError as e:
                logging.error(f"Error with the API request: {e}")
                print(f"Error with the API request: {e}")
            except sr.WaitTimeoutError:
                print("No speech detected in the given timeout period.")
            except KeyboardInterrupt:
                print("\nListening stopped by user.")
                break

# Start the real-time listening process
if __name__ == "__main__":
    listen_and_recognize()

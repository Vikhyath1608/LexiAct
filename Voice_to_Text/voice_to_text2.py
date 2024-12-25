import speech_recognition as sr

def recognize_speech_from_microphone():
    # Initialize recognizer
    recognizer = sr.Recognizer()

    # Set up the microphone
    with sr.Microphone() as source:
        print("Adjusting for ambient noise, please wait...")
        recognizer.adjust_for_ambient_noise(source)  # Reduces noise
        print("You can start speaking now...")

        while True:
            try:
                print("Listening...")
                # Non-blocking listening with pause threshold for real-time response
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=5)

                # Using Google Speech Recognition
                text = recognizer.recognize_google(audio)
                print(f"You said: {text}")

            except sr.WaitTimeoutError:
                print("Timeout. Please speak again.")
            except sr.UnknownValueError:
                print("Sorry, I could not understand the audio")
            except sr.RequestError as e:
                print(f"Error with the speech recognition service: {e}")

if __name__ == "__main__":
    recognize_speech_from_microphone()

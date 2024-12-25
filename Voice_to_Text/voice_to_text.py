import whisper
import os

# Define the path to your locally stored Whisper model
local_model_path = r"D:\lexiAct\whisper-main\whisper"

# Load the model from the local path
model = whisper.load_model(local_model_path)

# Function to transcribe speech
def transcribe_audio(audio_file):
    result = model.transcribe(audio_file)
    print("Transcription:", result["text"])

# Example usage (replace with your actual audio file path)
audio_file = r"D:\path\to\your\audio.wav"
transcribe_audio(audio_file)

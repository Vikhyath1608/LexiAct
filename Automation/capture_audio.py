import pyaudio
import wave
import os
from pydub import AudioSegment

# Set parameters for recording
FORMAT = pyaudio.paInt16  # 16-bit format
CHANNELS = 1  # Mono audio
RATE = 44100  # Sampling rate (44.1 kHz)
CHUNK = 1024  # Buffer size
RECORD_SECONDS = 10  # Recording duration

# Directory to save files
SAVE_DIR = r"D:\Files\Audio"

# Ensure the directory exists
os.makedirs(SAVE_DIR, exist_ok=True)

# File paths
WAV_FILENAME = os.path.join(SAVE_DIR, "output_wav.wav")
MP3_FILENAME = os.path.join(SAVE_DIR, "recorded audio.mp3")

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open the stream
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

print("Recording... Press Ctrl+C to stop early.")
frames = []

try:
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
except KeyboardInterrupt:
    print("Recording stopped early.")

print("Recording finished.")

# Stop and close the stream
stream.stop_stream()
stream.close()
audio.terminate()

# Save the recorded audio as WAV
with wave.open(WAV_FILENAME, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

print(f"Audio saved as {WAV_FILENAME}")

# Convert WAV to MP3
sound = AudioSegment.from_wav(WAV_FILENAME)
sound.export(MP3_FILENAME, format="mp3")

print(f"Audio saved as {MP3_FILENAME}")

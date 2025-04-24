from flask import Flask, request, jsonify, render_template
import json
import os
import io
import re
import pygame # type: ignore
from gtts import gTTS # type: ignore
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from meta_ai_api import MetaAI
import requests
import threading

from Automation.date_time import announce_date_time
from Automation.timer import set_timer
from Automation.set_alarm import set_alarm
from Automation.open_file import open_file
from Automation.caputure_vedio import video_recording
from Automation.volume_control import volume_control

app = Flask(__name__)
MUSIC_API_URL = "http://127.0.0.1:5001"

class ConversationHistory:
    def __init__(self, history_file):
        """Initialize conversation history."""
        self.history_file = history_file

    def load_history(self):
        """Load conversation history from file."""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding="utf-8") as file:
                    return json.load(file)
            else:
                return {}
        except json.JSONDecodeError:
            print("Error loading conversation history.")
            return {}

    def save_history(self, history):
        """Save conversation history to file."""
        try:
            with open(self.history_file, 'w', encoding="utf-8") as file:
                json.dump(history, file, indent=4)
        except Exception as e:
            print(f"Error saving conversation history: {e}")

    def add_conversation(self, history, session_id, prompt, response):
        """Add conversation to history."""
        if session_id not in history:
            history[session_id] = []
        history[session_id].append({"prompt": prompt, "response": response})

# Initialize conversation history and chatbot AI
conversation_history = ConversationHistory("conversation_history.json")
ai = MetaAI()

# Initialize Pygame for audio playback
pygame.init()
def handle_timer(prompt, session_id):
    """Handles the timer request by sending a response before starting the countdown."""
    message = f"⏲️Timer set for {prompt}."
    
    # Start the timer in a separate thread
    timer_thread = threading.Thread(target=set_timer, args=(prompt,))
    timer_thread.start()
    
    # Send response immediately before the timer starts
    return jsonify({'response': message, 'session_id': session_id})

def text_to_voice(text, lang='en', accent='co.in'):
    """Converts text to speech using Google Text-to-Speech (gTTS) and plays it dynamically."""
    try:
        tts = gTTS(text=text, lang=lang, tld=accent, slow=False)

        # Save to memory buffer
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)

        # Play using pygame
        pygame.mixer.init()
        pygame.mixer.music.load(fp, 'mp3')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
    except Exception as e:
        print("Error during text-to-speech conversion:", e)
        
def play_music(song_name):
    """Send request to play music via play_music Flask API."""
    response = requests.post(f"{MUSIC_API_URL}/play", json={"song_name": song_name})
    return response.json()

def control_music(command):
    """Send request to control music playback (pause, resume, next, etc.)."""
    response = requests.post(f"{MUSIC_API_URL}/control", json={"command": command})
    return response.json()

@app.route('/')
def index():
    return render_template('bot.html')

@app.route('/get_session_ids', methods=['GET'])
def get_session_ids():
    """Fetch session IDs from the conversation history."""
    history = conversation_history.load_history()
    session_ids = list(history.keys())  # Get all session IDs
    return jsonify({'session_ids': session_ids})


@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.json
    prompt = data.get('prompt', '').strip()
    session_id = data.get('session_id', '')

    if not prompt:
        return jsonify({'error': 'Prompt cannot be empty'}), 400

    try:
        # Handle music commands
        if "play" in prompt.lower() and "music" in prompt.lower():
            song_name = prompt.replace("play", "").replace("music", "").strip()
            response = play_music(song_name)
            return jsonify({'response': response['status'], 'session_id': session_id})
        
        #handle music control
        elif prompt.lower() in ["pause", "resume", "next", "prev", "skip", "quit", "restart"]:
            response = control_music(prompt.lower())
            return jsonify({'response': response['status'], 'session_id': session_id})
        
        #get date 
        elif "date" in prompt.lower():
            message=announce_date_time("date")
            text_to_voice(message, lang='en', accent='co.in')
            return jsonify({'response': message, 'session_id': session_id})
        
        elif re.search(r'\btime\b', prompt.lower()) and not re.search(r'\btimer\b', prompt.lower()):
            message=announce_date_time("time")
            text_to_voice(message, lang='en', accent='co.in')
            return jsonify({'response': message, 'session_id': session_id})
        
        elif re.search(r'\btimer\b', prompt.lower()):
            print(prompt.lower())
            return handle_timer(prompt.lower(), session_id)  # Send response immediately

        elif "alarm" in prompt.lower():
            alarm_thread = threading.Thread(target=set_alarm, args=(prompt.lower(),), daemon=True)
            alarm_thread.start()
            return jsonify({'response': "⏰ Alarm set", 'session_id': session_id})
        
        elif "open the" in prompt.lower():
            open_file(prompt.lower())
            return jsonify({'response': "🗂️ Opening File", 'session_id': session_id})
        
        elif "video recording" in prompt.lower():
            vedio_thread = threading.Thread(target=video_recording, args=("start",), daemon=True)
            vedio_thread.start()
            return jsonify({'response': "Video Recording started press q to stop", 'session_id': session_id})
        
        elif "volume" in prompt.lower():
           response_status= volume_control(prompt.lower())
           return jsonify({'response': response_status, 'session_id': session_id})
              
        
        # Default AI response
        history = conversation_history.load_history()
        response = ai.prompt(message=prompt)['message']
        conversation_history.add_conversation(history, session_id, prompt, response)
        conversation_history.save_history(history)
        text_to_voice(response, lang='en', accent='co.in')

        return jsonify({'response': response, 'session_id': session_id})

    except Exception as e:
        print("error in 1")
        print(str(e))
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
                
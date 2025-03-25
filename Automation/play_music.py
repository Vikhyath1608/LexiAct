from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import threading
app = Flask(__name__)
driver = None 
def start_music(song_name):
    global driver
    driver = webdriver.Chrome()
    driver.get("https://music.youtube.com/")
    wait = WebDriverWait(driver, 10)
    
    #search for song
    #look for search bar
    search_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "ytmusic-search-box button")))
    search_button.click()
    time.sleep(2)
    
    # Enter the song name in the search bar
    search_box = wait.until(EC.presence_of_element_located((By.TAG_NAME, "input")))
    search_box.send_keys(song_name)
    search_box.send_keys(Keys.RETURN)
    #time.sleep(5)
    
    try:
        # Click on the first play button
        play_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#actions > yt-button-renderer:nth-child(1) > yt-button-shape > button > yt-touch-feedback-shape > div > div.yt-spec-touch-feedback-shape__fill")))
        play_button.click()
        print(f"🎵 Now Playing: {song_name}")
    except:
        print("⚠️ Play button not found via CSS Selector, trying JavaScript click...")
        driver.execute_script("""
            document.querySelector("#actions > yt-button-renderer:nth-child(1) > yt-button-shape > button").click();
        """)
    #driver.execute_script("document.querySelector('video').play()")
    
@app.route('/play', methods=['POST'])
def play():
    global driver
    data = request.json
    song_name = data.get('song_name', '')

    if not song_name:
        return jsonify({'error': 'No song name provided'}), 400

    if driver is not None:
        driver.quit()  # Close existing session

    threading.Thread(target=start_music, args=(song_name,)).start()  # Run in a separate thread
    return jsonify({'status': f'Playing {song_name} on YouTube Music'}), 200

@app.route('/control', methods=['POST'])
def control():
    """Control music playback (pause, resume, next, prev, skip, quit)."""
    global driver
    if driver is None:
        return jsonify({'error': 'No active music session'}), 400

    data = request.json
    command = data.get('command', '').lower()
    try:
        if command == "pause":
            driver.execute_script("document.querySelector('video').pause()")
            return jsonify({'status': '⏸ Music Paused'}),200
    
        elif command == "resume":
            driver.execute_script("document.querySelector('video').play()")
            return jsonify({'status': '▶️ Music Resumed'}),200

        elif command == "next":
            # next_button = WebDriverWait(driver, 5).until(
            #     EC.element_to_be_clickable((By.XPATH, "//tp-yt-paper-icon-button[@title='Next song']"))
            # )
            next_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-bar/div[1]/div/tp-yt-paper-icon-button[5]/tp-yt-iron-icon"))
            )
            next_button.click()
            return jsonify({'status': '⏭ Skipped to Next Song'}),200  
        
        elif command == "prev":
            # prev_button = WebDriverWait(driver, 5).until(
            #     EC.element_to_be_clickable((By.XPATH, "//tp-yt-paper-icon-button[@title='Previous song']"))
            # )
            prev_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-bar/div[1]/div/tp-yt-paper-icon-button[1]/tp-yt-iron-icon"))
                )
            prev_button.click()
            prev_button.click()
            return jsonify({'status': '⏮ Playing Previous Song'}),200
        
        elif command == "restart":
            # prev_button = WebDriverWait(driver, 5).until(
            #     EC.element_to_be_clickable((By.XPATH, "//tp-yt-paper-icon-button[@title='Previous song']"))
            # )
            prev_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-bar/div[1]/div/tp-yt-paper-icon-button[1]/tp-yt-iron-icon"))
                )
            prev_button.click()
            return jsonify({'status': '🔄 Restart song'}),200
        
        elif command == "skip":
            # skip_button = WebDriverWait(driver, 5).until(
            #     EC.element_to_be_clickable((By.XPATH, "//ytmusic-player[@player-state='AD']//tp-yt-paper-icon-button"))
            # )
            skip_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/ytmusic-app/ytmusic-app-layout/ytmusic-player-page/div/div[1]/ytmusic-player/div[2]/div/div/div[14]/div/div[3]/div/div[2]/span/button"))
            )
            skip_button.click()
            return jsonify({'status': '⏩ Skipped Ad'}),200
        
        elif command == "quit":
            driver.quit()
            return jsonify({'status': '🛑 Music Stopped'}),200
        
        else:
            return jsonify({'error': 'Invalid command'}), 400

    except Exception as e:
        print("error in 2")
        return jsonify({'error': str(e)}), 500
    
if __name__ == "__main__":
    app.run(port=5001, debug=True)
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def search_and_play(search_query):
    # Set up Chrome options
  
    
    # Set up the WebDriver
    driver = webdriver.Chrome()
    driver.get("https://www.youtube.com/")
    time.sleep(3)  # Allow page to load
    
    try:
        # Find the search bar and enter the query
        search_box = driver.find_element(By.NAME, "search_query")
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)
        
        time.sleep(3)  # Wait for results to load
        
        # Click on the first video
        first_video = driver.find_element(By.CSS_SELECTOR, "#video-title > yt-formatted-string")
        first_video.click()
        time.sleep(5)
        driver.refresh()
        time.sleep(5)
        # Control video playback based on user input
        while True:
            command = input("Enter 'play' to play, 'pause' to pause, or 'exit' to quit: ").strip().lower()
            
            if command == "play" or command == "pause":
                play_button = driver.find_element(By.CSS_SELECTOR, "#movie_player > div.ytp-chrome-bottom > div.ytp-chrome-controls > div.ytp-left-controls > button")
                play_button.click()
                
            elif command == "skip":
                try:
                    # Attempt to find and click the "Skip Ad" button if it exists
                    skip_ad_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "#skip-button\:2"))
                    )
                    skip_ad_button.click()
                    print("Skipped ad!")
                except Exception:
                    print("No skippable ad found.")

            elif command == "exit":
                break
            else:
                print("Invalid command. Please enter 'play', 'pause', or 'exit'.")
    
    finally:
        driver.quit()  # Ensure the browser closes properly

if __name__ == "__main__":
    search_query = input("Enter your search query: ")
    search_and_play(search_query)
    print("Program terminated.")

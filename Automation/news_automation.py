from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time

# Initialize the driver
def Open_news(query):
    driver = webdriver.Chrome()  # Make sure chromedriver is in your PATH

    try:
        driver.get("https://news.google.com/")
        time.sleep(3)  # Wait for the page to load

        search_input = None

        # Attempt with CSS selector
        try:
            search_input = driver.find_element(By.CSS_SELECTOR,
                "#gb > div.gb_ld.gb_pd.gb_Hd > div.gb_xd.gb_Bd.gb_Le.gb_Ke.gb_De > div.gb_we > form > div.gb_qe > div > div > div > div > div.d1dlne > input.Ax4B8.ZAGvjd")
        except NoSuchElementException:
            print("CSS selector failed. Trying XPath...")

        # Attempt with XPath
        if not search_input:
            try:
                search_input = driver.find_element(By.XPATH,
                    "/html/body/div[4]/header/div[2]/div[2]/div[2]/form/div[1]/div/div/div/div/div[1]/input[2]")
            except NoSuchElementException:
                print("XPath failed. Trying fallback...")

        # Fallback: find the only visible input field
        if not search_input:
            inputs = driver.find_elements(By.TAG_NAME, "input")
            for i in inputs:
                if i.is_displayed() and i.get_attribute("type") == "text":
                    search_input = i
                    print("Fallback input field found.")
                    break

        if not search_input:
            print("Failed to find the search input.")
        else:
            search_input.send_keys(query)
            search_input.send_keys(Keys.RETURN)
            print(f"Search submitted for: {query}")

        print("[*] Browser will remain open until manually closed.")

        # Hold the script until the user closes the browser
        while True:
            try:
                # Polling to see if the browser is still open
                driver.title  # This will raise an exception if browser is closed
                time.sleep(2)
            except:
                print("[*] Browser closed by user.")
                break

    finally:
        # Do not quit automatically
        # driver.quit()
        pass

def search_google_news(user_prompt: str):
    print(f"[User Prompt] {user_prompt}")

    query = user_prompt.strip()

    # Remove just the starting "get" (case-insensitive)
    if query.lower().startswith("get "):
        query = query[4:]  # Remove "get " (4 characters including space)

    print(f"[+] Final search query: '{query}'")
    Open_news(query)

# search_google_news("get the latest news regarding manglore")

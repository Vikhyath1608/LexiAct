# Lexi-Act a Large ACtion Model 

## Table of Contents

- [About](#about)
- [File Structure](#File-structure)
- [Usage Notes](#usage-notes)
- [Contact](#contact)

## About

LexiAct is your intelligent voice assistant powered by AI, designed to execute everyday tasks through natural conversations. Whether it’s setting alarms, controlling volume, sending emails, or automating the web – just speak it, and LexiAct acts.
 
## File Structure
```bash
Flask_app/
├── __pycache__/
├── app.py
├── app_paths.json
├── Automation/
├── command.txt
├── conversation_history.json
├── nltk_utilities.py
├── README.md
├── recognizer_errors.log
├── requirements.txt
├── static/
├── templates/
├── test.json

```

## Usage Notes

- Run the microservices
- get in Automation folder:
  ```bash
  python play_music.py
  ```
- Email microsevice:
  ```bash
  python email_automation.py
  ```
- create a .env file with the system path and email passwors and userid
  ```bash
  .env
  ```
- Run the app:
  ```bash
  python app.py

  ```

## Contact

- For support or inquiries:
  Email: vikhyathraims0109@gmail.com

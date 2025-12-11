# Special Circumstances RPG Character Manager

This is a Streamlit web application designed to help you create, manage, and play with characters for the "Special Circumstances" RPG.

## Features

* **Character Creation Wizard:** A step-by-step guide to create a new character, including basic info, homeworld, upbringing, lifepaths, skills, and more.
* **Character Sheet Editor:** A comprehensive editor to view and modify your character's sheet. You can upload an existing character file (in JSON format) and edit all aspects of your character.
* **Play Mode:** A simplified interface for use during gameplay. It allows you to make skill tests, track successes and failures, and manage your character's conditions.
* **Save/Load Functionality:** You can save your characters as JSON files and load them back into the application at any time.

## How to Run

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```
2. **Run the Streamlit application:**

   ```bash
   streamlit run app.py
   ```
3. The application will open in your web browser.

## Project Structure

```
├── app.py                    # Main application file (redirects to Home)
├── requirements.txt          # Project dependencies
├── Rulebook.md               # (Presumably) The rules of the RPG
├── assets/                   # Images and other assets
│   ├── create_character.jpg
│   └── header.jpg
├── characters/               # Default directory for saved characters
├── pages/                    # Streamlit pages
│   ├── 0_🏠_Home.py
│   ├── 1_➕_Create_Character.py
│   ├── 2_📝_Edit_Character.py
│   └── 3_🎲_Play_Mode.py
└── src/                      # Source code
    ├── __init__.py
    ├── character.py          # The Character class
    └── components.py         # Streamlit components for the UI
```

## Dependencies

* streamlit
* (and any other libraries listed in `requirements.txt`)

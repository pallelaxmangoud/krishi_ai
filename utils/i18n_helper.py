import streamlit as st
import json
import os

def load_translation():
    """Loads the translation file based on user selection, defaults to English."""
    lang = st.session_state.get("lang_code", "en")
    file_path = f"locales/{lang}.json"
    
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
            
    # Fallback if file doesn't exist
    if os.path.exists("locales/en.json"):
        with open("locales/en.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def t(key):
    """Shorthand function to look up a translation key."""
    translations = load_translation()
    return translations.get(key, key)
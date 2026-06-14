import streamlit as st
import json
import os

# Set up page configuration
st.set_page_config(
    page_title="Krishi-AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 1. i18n: Language Loader Helper
def load_localization(lang):
    file_path = f"locales/{lang}.json"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    # Fallback to English if file doesn't exist
    if os.path.exists("locales/en.json"):
        with open("locales/en.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# 2. Global Sidebar for Settings
st.sidebar.title("🚜 Krishi-AI Settings")

# Language mapping selection
lang_options = {
    "English": "en",
    "తెలుగు (Telugu)": "te",
    "हिन्दी (Hindi)": "hi"
}

# Use a key to automatically tie this to st.session_state
selected_lang_name = st.sidebar.selectbox(
    "Choose Language / భాషను ఎంచుకోండి", 
    options=list(lang_options.keys()),
    key="selected_lang_display"
)

# Force the system to save the lang_code state securely
lang_code = lang_options[selected_lang_name]
st.session_state["lang_code"] = lang_code

# Load the text dictionary based on choice
labels = load_localization(lang_code)

# AI Engine Options
st.sidebar.write("---")
st.sidebar.subheader("🤖 AI Engine Configuration")
ai_mode = st.sidebar.radio(
    "Select AI Mode:",
    options=["Local Inference (Ollama)", "Bring Your Own Key (BYOK)"],
    key="ai_mode"
)

if "Local" in ai_mode:
    st.sidebar.selectbox("Local Model", options=["llama3", "gemma"], key="ollama_model")
else:
    st.sidebar.selectbox("API Provider", options=["Google Gemini"], key="api_provider")
    st.sidebar.text_input("Enter API Key", type="password", key="api_key")

# 3. Main Page Content Display
st.title(f"🌾 {labels.get('welcome', 'Welcome to Krishi-AI')}")
st.write("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.header("✨ Empowering Farmers with AI")
    st.write(
        "This platform provides real-time, localized agricultural assistance using "
        "cutting-edge Artificial Intelligence."
    )
    st.write("### Current Configuration:")
    st.write(f"* **Language:** {selected_lang_name}")
    st.write(f"* **AI Engine:** {ai_mode}")

with col2:
    st.info(
        "💡 **Hackathon Tip:** Use the sidebar navigation to switch between pages. "
        "Your language settings and API keys will seamlessly follow you across pages!"
    )
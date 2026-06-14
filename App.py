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

# --- Initialize persistent session storage ---
if "lang_code" not in st.session_state:
    st.session_state["lang_code"] = "en"
if "ai_mode" not in st.session_state:
    st.session_state["ai_mode"] = "Bring Your Own Key (BYOK)"
if "saved_api_key" not in st.session_state:
    st.session_state["saved_api_key"] = ""

# 1. i18n: Language Loader Helper
def load_localization(lang):
    file_path = f"locales/{lang}.json"
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    if os.path.exists("locales/en.json"):
        with open("locales/en.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# 2. Global Sidebar for Settings
st.sidebar.title("🚜 Krishi-AI Settings")

# Language selection
lang_options = {
    "English": "en",
    "తెలుగు (Telugu)": "te",
    "हिन्दी (Hindi)": "hi"
}

# Reverse mapping to find current display name based on saved code
current_lang_name = "English"
for name, code in lang_options.items():
    if code == st.session_state["lang_code"]:
        current_lang_name = name

selected_lang_name = st.sidebar.selectbox(
    "Choose Language / భాషను ఎంచుకోండి", 
    options=list(lang_options.keys()),
    index=list(lang_options.keys()).index(current_lang_name)
)
st.session_state["lang_code"] = lang_options[selected_lang_name]

labels = load_localization(st.session_state["lang_code"])

# AI Engine Options
st.sidebar.write("---")
st.sidebar.subheader("🤖 AI Engine Configuration")

current_mode_idx = 0 if st.session_state["ai_mode"] == "Bring Your Own Key (BYOK)" else 1
ai_mode = st.sidebar.radio(
    "Select AI Mode:",
    options=["Bring Your Own Key (BYOK)", "Local Inference (Ollama)"],
    index=current_mode_idx
)
st.session_state["ai_mode"] = ai_mode

if "Local" in ai_mode:
    st.sidebar.selectbox("Local Model", options=["llama3", "gemma"], key="ollama_model")
else:
    st.sidebar.selectbox("API Provider", options=["Google Gemini"], key="api_provider")
    
    # Track the API key using session storage to prevent widget deletion loss
    input_key = st.sidebar.text_input(
        "Enter API Key", 
        type="password", 
        value=st.session_state["saved_api_key"]
    )
    if input_key:
        st.session_state["saved_api_key"] = input_key
        st.session_state["api_key"] = input_key

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
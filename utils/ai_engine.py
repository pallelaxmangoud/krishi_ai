import requests
import streamlit as st

def call_ai_agent(prompt, system_instruction="You are a helpful agriculture expert."):
    """Routes the prompt safely depending on settings, protecting the live web URL."""
    ai_mode = st.session_state.get("ai_mode", "Bring Your Own Key (BYOK)")
    
    # --- OPTION A: BRING YOUR OWN KEY (BYOK) ---
    if "BYOK" in ai_mode or "Cloud" in ai_mode:
        api_key = st.session_state.get("saved_api_key", "").strip()
        if not api_key:
            api_key = st.session_state.get("api_key", "").strip()
        
        if not api_key:
            return "⚠️ Please enter your Google Gemini API Key in the sidebar configuration on the Home page to chat!"
            
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        payload = {
            "contents": [{
                "parts": [{"text": f"{system_instruction}\n\nUser: {prompt}"}]
            }]
        }
        try:
            res = requests.post(url, json=payload, timeout=120)
            if res.status_code == 200:
                return res.json()['candidates'][0]['content']['parts'][0]['text']
            return f"Gemini API Error: Status code {res.status_code}. Please check if your API key is valid."
        except Exception as e:
            return f"Cloud API Connection Error: {str(e)}"

    # --- OPTION B: LOCAL INFERENCE (OLLAMA) ---
    else:
        # Fallback to Cloud execution if key is present on the public live server instance
        api_key = st.session_state.get("saved_api_key", "").strip()
        if api_key:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            payload = {"contents": [{"parts": [{"text": f"{system_instruction}\n\nUser: {prompt}"}]}]}
            try:
                res = requests.post(url, json=payload, timeout=120)
                if res.status_code == 200:
                    return res.json()['candidates'][0]['content']['parts'][0]['text']
            except Exception:
                pass
        
        return "❌ Local Ollama cannot be accessed directly from a live public URL web server. Please open the sidebar configuration settings on the Home page, toggle to 'Bring Your Own Key (BYOK)', and input your personal Gemini API Key!"
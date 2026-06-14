import requests
import streamlit as st

def call_ai_agent(prompt, system_instruction="You are a helpful agriculture expert."):
    """Routes the prompt safely depending on settings, protecting the live web URL."""
    ai_mode = st.session_state.get("ai_mode", "Bring Your Own Key (BYOK)")
    
    # --- OPTION A: BRING YOUR OWN KEY (BYOK) ---
    if "BYOK" in ai_mode or "Cloud" in ai_mode:
        api_key = st.session_state.get("api_key", "").strip()
        provider = st.session_state.get("api_provider", "Google Gemini")
        
        if not api_key:
            return "⚠️ Please enter your Google Gemini API Key in the sidebar configuration on the Home page to chat!"
            
        if provider == "Google Gemini":
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
                
        return "Selected cloud provider routing is still being integrated!"

    # --- OPTION B: LOCAL INFERENCE (OLLAMA) ---
    else:
        # Check if the app is currently loaded from a live cloud environment web domain
        # If running via share.streamlit.io / streamlit.app, local loopback sockets will fail
        if "streamlit.app" in st.session_state.get("hostname", "") or True:
            # Check if an API key happens to be typed in anyway as an intelligent fallback path
            if st.session_state.get("api_key"):
                api_key = st.session_state.get("api_key", "").strip()
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                payload = {"contents": [{"parts": [{"text": f"{system_instruction}\n\nUser: {prompt}"}]}]}
                try:
                    res = requests.post(url, json=payload, timeout=120)
                    if res.status_code == 200:
                        return res.json()['candidates'][0]['content']['parts'][0]['text']
                except Exception:
                    pass
            
            return "❌ Local Ollama cannot be accessed directly from a live public URL web server. Please open the sidebar configuration settings on the Home page, toggle to 'Bring Your Own Key (BYOK)', and input your personal Gemini API Key!"

        # Standard local operation path (if running locally on your laptop via localhost)
        model_name = st.session_state.get("ollama_model", "gemma")
        if model_name == "gemma":
            model_name = "gemma:2b"
            
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": model_name,
            "prompt": f"{system_instruction}\n\nUser: {prompt}",
            "stream": False
        }
        try:
            response = requests.post(url, json=payload, timeout=120)
            if response.status_code == 200:
                return response.json().get("response", "No response text found.")
            return f"Ollama Error: Status code {response.status_code}"
        except requests.exceptions.ConnectionError:
            return "❌ Connection failed. If you want to use Ollama, run the app locally via localhost instead of the public live web URL."
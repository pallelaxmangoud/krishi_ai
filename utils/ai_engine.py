import requests
import streamlit as st

def call_ai_agent(prompt, system_instruction="You are a helpful agriculture expert."):
    """Routes the prompt to either Local Ollama or Cloud API depending on settings."""
    ai_mode = st.session_state.get("ai_mode", "Local Inference (Ollama)")
    
    # --- OPTION A: LOCAL INFERENCE (OLLAMA) ---
    if "Local" in ai_mode:
        model_name = st.session_state.get("ollama_model", "llama3")
        
        # Auto-correct the placeholder name to match your downloaded local gemma model
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
            return "❌ Could not connect to Ollama. Make sure the Ollama desktop app is running locally on your PC!"
        except requests.exceptions.Timeout:
            return "⏳ The local model took too long to think. Please try using a lighter model like gemma:2b!"

    # --- OPTION B: BRING YOUR OWN KEY (BYOK) ---
    else:
        api_key = st.session_state.get("api_key", "").strip()
        provider = st.session_state.get("api_provider", "Google Gemini")
        
        if not api_key:
            return "⚠️ Please enter your API Key in the sidebar configuration on the Home page."
            
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
                return f"Gemini API Error: Status code {res.status_code}"
            except Exception as e:
                return f"Cloud API Error: {str(e)}"
                
        return "Selected cloud provider routing is still being integrated!"
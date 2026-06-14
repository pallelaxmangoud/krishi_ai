import streamlit as st
import google.generativeai as genai

def call_ai_agent(prompt, system_instruction="You are a helpful agriculture expert."):
    """Routes the prompt safely using the official Google GenAI SDK framework with automatic fallback handling."""
    ai_mode = st.session_state.get("ai_mode", "Bring Your Own Key (BYOK)")
    
    # --- OPTION A: BRING YOUR OWN KEY (BYOK) ---
    if "BYOK" in ai_mode or "Cloud" in ai_mode:
        api_key = st.session_state.get("saved_api_key", "").strip()
        if not api_key:
            api_key = st.session_state.get("api_key", "").strip()
        
        if not api_key:
            return "⚠️ Please enter your Google Gemini API Key in the sidebar configuration on the Home page to chat!"
            
        # List of available models to cycle through in case one throws a 404
        model_options = ["gemini-pro", "gemini-1.5-flash-latest", "gemini-1.5-pro"]
        
        try:
            genai.configure(api_key=api_key)
            
            # Loop through models until one works
            for model_name in model_options:
                try:
                    model = genai.GenerativeModel(
                        model_name=model_name,
                        system_instruction=system_instruction
                    )
                    response = model.generate_content(prompt, timeout=30)
                    return response.text
                except Exception as model_err:
                    # If it's a 404, continue to the next model in the list
                    if "404" in str(model_err):
                        continue
                    else:
                        raise model_err
                        
            return "❌ Gemini SDK Error: All attempted model variations (gemini-pro, gemini-1.5-flash) returned 404. Please check if your API key has legacy model access restrictions."
            
        except Exception as e:
            if "API_KEY_INVALID" in str(e) or "403" in str(e):
                return "❌ Invalid API Key: Google rejected this key. Please copy a fresh key from Google AI Studio."
            return f"❌ Gemini SDK Error: {str(e)}"

    # --- OPTION B: LOCAL INFERENCE (OLLAMA) ---
    else:
        api_key = st.session_state.get("saved_api_key", "").strip()
        if api_key:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(model_name="gemini-pro", system_instruction=system_instruction)
                response = model.generate_content(prompt)
                return response.text
            except Exception:
                pass
        
        return "❌ Local Ollama cannot be accessed directly from a live public URL web server. Please open the sidebar configuration settings on the Home page, toggle to 'Bring Your Own Key (BYOK)', and input your personal Gemini API Key!"
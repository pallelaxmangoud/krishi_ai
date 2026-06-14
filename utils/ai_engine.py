import streamlit as st
import google.generativeai as genai

def call_ai_agent(prompt, system_instruction="You are a helpful agriculture expert."):
    """Routes the prompt safely using the official modern Google GenAI SDK framework 
    with strict multi-language response enforcement."""
    ai_mode = st.session_state.get("ai_mode", "Bring Your Own Key (BYOK)")
    
    # --- OPTION A: BRING YOUR OWN KEY (BYOK) ---
    if "BYOK" in ai_mode or "Cloud" in ai_mode:
        api_key = st.session_state.get("saved_api_key", "").strip()
        if not api_key:
            api_key = st.session_state.get("api_key", "").strip()
        
        if not api_key:
            return "⚠️ Please enter your Google Gemini API Key in the sidebar configuration on the Home page to chat!"
            
        try:
            # Configure the library with your API key
            genai.configure(api_key=api_key)
            
            # Using the supported flagship production model
            model = genai.GenerativeModel(
                model_name="gemini-2.5-flash",
                generation_config={"response_mime_type": "text/plain"}
            )
            
            # CRITICAL LANGUAGE FORCE: Instructing the model to reply in the user's language choice
            full_prompt = (
                f"{system_instruction}\n"
                f"IMPORTANT: Detect the language of the user's question and respond entirely in that same language "
                f"(e.g., if asked in Telugu, reply in Telugu script; if in Hindi, reply in Hindi script).\n\n"
                f"User Question: {prompt}"
            )
            
            # Generate content
            response = model.generate_content(full_prompt)
            return response.text
            
        except Exception as e:
            return f"❌ Google API Response Error: {str(e)}"

    # --- OPTION B: LOCAL INFERENCE (OLLAMA) ---
    else:
        api_key = st.session_state.get("saved_api_key", "").strip()
        if api_key:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(model_name="gemini-2.5-flash")
                full_prompt = f"{system_instruction}\nRespond in the user's language.\n\nUser Question: {prompt}"
                response = model.generate_content(full_prompt)
                return response.text
            except Exception:
                pass
        
        return "❌ Local Ollama cannot be accessed directly from a live public URL web server. Please open the sidebar configuration settings on the Home page, toggle to 'Bring Your Own Key (BYOK)', and input your personal Gemini API Key!"
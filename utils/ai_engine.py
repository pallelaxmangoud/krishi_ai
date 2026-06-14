import streamlit as st
import google.generativeai as genai

def call_ai_agent(prompt, system_instruction="You are a helpful agriculture expert."):
    """Routes the prompt safely using the official modern Google GenAI SDK framework."""
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
            
            # Using the supported flagship production model with robust configuration parsing
            model = genai.GenerativeModel(
                model_name="gemini-2.5-flash",
                generation_config={"response_mime_type": "text/plain"}
            )
            
            # Merging system instructions right into the content generation pipeline safely
            full_prompt = f"System Instruction: {system_instruction}\n\nUser Question: {prompt}"
            
            # Generate content
            response = model.generate_content(full_prompt)
            return response.text
            
        except Exception as e:
            # Show the raw exact error coming from Google's servers
            return f"❌ Google API Response Error: {str(e)}"

    # --- OPTION B: LOCAL INFERENCE (OLLAMA) ---
    else:
        api_key = st.session_state.get("saved_api_key", "").strip()
        if api_key:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(model_name="gemini-2.5-flash")
                full_prompt = f"System Instruction: {system_instruction}\n\nUser Question: {prompt}"
                response = model.generate_content(full_prompt)
                return response.text
            except Exception:
                pass
        
        return "❌ Local Ollama cannot be accessed directly from a live public URL web server. Please open the sidebar configuration settings on the Home page, toggle to 'Bring Your Own Key (BYOK)', and input your personal Gemini API Key!"
import streamlit as st
from utils.i18n_helper import t
from utils.ai_engine import call_ai_agent

# Set up the page layout titles
st.title(f"💬 {t('chat_title')}")
st.write("---")

# Initialize chat log memory array if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display all previous messages in the chat history logs
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input Entry Box
if user_prompt := st.chat_input(t("chat_placeholder")):
    
    # Display user query instantly
    with st.chat_message("user"):
        st.markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    
    # Generate the translated response
    with st.chat_message("assistant"):
        with st.spinner("🧠 thinking..."):
            # Fetch the active language code string safely
            lang_code = st.session_state.get("lang_code", "en")
            
            # Create strict language mapping instructions
            lang_names = {"en": "English", "te": "Telugu", "hi": "Hindi"}
            target_language = lang_names.get(lang_code, "English")
            
            # This system prompt strictly commands the AI to translate its logic completely
            system_prompt = (
                f"You are an expert agricultural assistant. "
                f"CRITICAL RULE: You must translate and output your entire response "
                f"completely and fluently in the {target_language} language only. "
                f"Do not use English words unless they are specific scientific names or numbers."
            )
            
            # Send prompt request downstream to your dynamic routing backend
            answer = call_ai_agent(user_prompt, system_instruction=system_prompt)
            st.markdown(answer)
            
    # Save response to history logs
    st.session_state.messages.append({"role": "assistant", "content": answer})
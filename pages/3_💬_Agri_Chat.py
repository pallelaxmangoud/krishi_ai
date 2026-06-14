import streamlit as st
from utils.ai_engine import call_ai_agent

st.set_page_config(page_title="Agri Chat", page_icon="💬", layout="wide")

st.title("💬 Krishi AI - Agri Chat")
st.write("Ask any agriculture-related questions below.")

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("How can I help you with your crops today?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate response from the engine
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Call your updated clean engine function
            response = call_ai_agent(
                prompt=prompt, 
                system_instruction="You are an expert agricultural assistant. Provide clear, practical farming advice. Respond in the user's language choice."
            )
            st.markdown(response)
            
    st.session_state.messages.append({"role": "assistant", "content": response})
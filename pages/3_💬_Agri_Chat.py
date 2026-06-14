import streamlit as st
from utils.ai_engine import call_ai_agent

st.set_page_config(page_title="Agri Chat", page_icon="💬", layout="wide")

st.title("💬 Krishi AI - Agri Chat")
st.write("Ask any agriculture-related questions below.")

# --- NEW: Language Selection Widget ---
st.sidebar.markdown("### 🌐 Language Settings")
selected_language = st.sidebar.radio(
    "Choose your language / భాషను ఎంచుకోండి:",
    ["English", "Telugu (తెలుగు)", "Hindi (हिंदी)"]
)

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

    # Customizing the instruction based on the user's dropdown choice
    system_instruction_with_lang = (
        f"You are an expert agricultural assistant. Provide clear, practical farming advice. "
        f"CRITICAL: The user has explicitly selected to receive the response in {selected_language}. "
        f"You MUST reply completely in the script of {selected_language}."
    )

    # Generate response from the engine
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = call_ai_agent(
                prompt=prompt, 
                system_instruction=system_instruction_with_lang
            )
            st.markdown(response)
            
    st.session_state.messages.append({"role": "assistant", "content": response})

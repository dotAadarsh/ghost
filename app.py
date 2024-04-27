import streamlit as st
from redact import redact_prompt
from gemini_ai import call_genai

st.set_page_config(
    page_title="Ghost | Your Privacy, Our Priority",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://twitter.com/dotAadarsh',
        'Report a bug': "https://github.com/dotAadarsh/ghost",
        'About': "A secure AI powered chatbot powered by Pangea"
    })

st.title("Ghost")
st.caption("Your Privacy, Our Priority")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    try:
        # Display user message in chat message container after redaction
        redacted_prompt = redact_prompt(prompt)
        st.chat_message("user").markdown(redacted_prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": redacted_prompt})

        # Add loading spinner
        with st.spinner("Waiting for response..."):
            # Call AI for response
            response = call_genai(redacted_prompt)
    except Exception as e:
        st.error(f"An error occurred: {e}")
        response = "Sorry, I encountered an error and couldn't process your request."

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

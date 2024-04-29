import streamlit as st
from pathlib import Path
import os
from functions.sanitize_file import sanitize_file
from functions.display import display_pdf
from functions.vectorize_pdf import ask
from functions.redact import redact_prompt
from functions.gemini_ai import call_genai


st.set_page_config(
    page_title="Ghost | Where Privacy Meets Intelligence!",
    page_icon="",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://twitter.com/dotAadarsh',
        'Report a bug': "https://github.com/dotAadarsh/ghost",
        'About': "A secure AI powered chatbot powered by Pangea"
    })

st.title("GHOST")
st.caption("Where Privacy Meets Intelligence!")


def main():

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    uploaded_file = st.sidebar.file_uploader("Upload your PDF", type="pdf")

    # Define a variable to store the sanitized file path
    sanitized_file = st.session_state.get("sanitized_file")

    if uploaded_file:
        save_path = os.path.join(uploaded_file.name)
        if not sanitized_file:  # Check if sanitized file exists
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            st.toast(f"PDF saved successfully to: {save_path}")

            with st.spinner("Sanitizing the uploaded file..."):
                sanitized_file = sanitize_file(uploaded_file, save_path)
                st.session_state["sanitized_file"] = sanitized_file  # Store path
            display_pdf(sanitized_file)

    # React to user input
    if prompt := st.chat_input("Wassup?"):
        try:
            redacted_prompt = redact_prompt(prompt)
            st.chat_message("user").markdown(redacted_prompt)
            st.session_state.messages.append({"role": "user", "content": redacted_prompt})

            with st.spinner("Waiting for response..."):
                vectorized_response = ask(sanitized_file, redacted_prompt)  # Use existing sanitized file
                response = call_genai(vectorized_response)

            st.chat_message("assistant").markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            st.error(f"An error occurred: {e}")
            response = "Sorry, I encountered an error and couldn't process your request."


if __name__ == "__main__":
    main()

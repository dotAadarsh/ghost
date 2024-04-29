import streamlit as st
from redact import redact_prompt
from gemini_ai import call_genai
from pathlib import Path
import os
from display import share_display_pdf
from sanitize_file import sanitize_file
from vector_pdf import ask

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

# Define a flag variable to track whether process_pdf has been executed
process_pdf_executed = False

def process_pdf(uploaded_file):
    global process_pdf_executed
    if process_pdf_executed:
        return  # If process_pdf has already been executed, return without doing anything

    if uploaded_file:
        save_path = os.path.join("files", uploaded_file.name)  # Define save path (modify "saved_pdfs")
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        st.toast(f"PDF saved successfully to: {save_path}")

        sanitized_file = sanitize_file(uploaded_file, save_path)
        share_display_pdf(sanitized_file)

        # Store sanitized file path in session state
        st.session_state["sanitized_file"] = sanitized_file
        process_pdf_executed = True  # Set the flag to True after process_pdf has been executed

    return st.session_state.get("sanitized_file")  # Return sanitized file from session state (if available)


def main():

    toggle_on = st.sidebar.toggle('Bring Your Own File (.pdf)')


    if toggle_on:
        st.toast('Feature activated!')
        uploaded_file = st.sidebar.file_uploader("Upload your PDF", type="pdf")
        sanitized_file = process_pdf(uploaded_file)

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
            redacted_prompt = redact_prompt(prompt)
            st.chat_message("user").markdown(redacted_prompt)
            st.session_state.messages.append({"role": "user", "content": redacted_prompt})


            if sanitized_file and toggle_on:
                # Use the stored sanitized_file for subsequent queries within this session
                redacted_prompt = ask(sanitized_file, redacted_prompt)

            # Add loading spinner
            with st.spinner("Waiting for response..."):
                print(redacted_prompt)
                response = call_genai(redacted_prompt)
                print(response)

            # Display assistant response
            st.chat_message("assistant").markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            st.error(f"An error occurred: {e}")
            response = "Sorry, I encountered an error and couldn't process your request."

if __name__ == "__main__":
    main()

import streamlit as st
from functions.gemini_ai import call_genai
from functions.redact import redact_prompt

st.set_page_config(
    page_title="Ghost | Where Privacy Meets Intelligence!",
    page_icon="./assets/ghost_logo.png",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://twitter.com/dotAadarsh',
        'Report a bug': "https://github.com/dotAadarsh/ghost",
        'About': "A secure AI powered chatbot powered by Pangea"
    })

st.title("Ghost")
st.caption("Where Privacy Meets Intelligence!")


with st.sidebar:
    st.caption("Powered by Pangea")

def main():

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # React to user input
    if prompt := st.chat_input("Wassup?"):
        try:
            redacted_prompt = redact_prompt(prompt)
            st.chat_message("user").markdown(redacted_prompt)
            st.session_state.messages.append({"role": "user", "content": redacted_prompt})

            # Add loading spinner
            with st.spinner("Waiting for response..."):
                response = call_genai(redacted_prompt)

            # Display assistant response
            st.chat_message("assistant").markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            st.error(f"An error occurred: {e}")
            response = "Sorry, I encountered an error and couldn't process your request."


if __name__ == "__main__":
    main()

import pangea.exceptions as pe
from pangea.config import PangeaConfig
from pangea.services import Redact
import streamlit as st

# Get Pangea token and domain from environment variables
token = st.secrets["PANGEA_TOKEN"]
assert token, "PANGEA_TOKEN is not set in the environment"

domain = st.secrets["PANGEA_DOMAIN"]
assert domain, "PANGEA_DOMAIN is not set in the environment"

# Initialize Pangea configuration and Redact service
config = PangeaConfig(domain=domain)
redact = Redact(token, config=config)

# Function to redact user input
def redact_prompt(user_prompt):
    """
    Redact sensitive information from user input using Pangea's Redact service.

    Args:
        user_prompt (str): The user input to be redacted.

    Returns:
        str: The redacted user input, or None if an error occurs.
    """
    print(f"Redacting user input: {user_prompt}")

    try:
        # Attempt to redact the user input
        redact_response = redact.redact(text=user_prompt)
        redacted_text = redact_response.result.redacted_text
        print(f"Redacted text: {redacted_text}")
        return redacted_text

    except pe.PangeaAPIException as e:
        # Handle Pangea API exceptions
        print(f"Pangea API Exception: {e.response.summary}")
        for err in e.errors:
            print(f"\t{err.detail}")
        # Return None in case of error
        return None

    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred: {e}")
        # Return None in case of error
        return None

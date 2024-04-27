import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the GenAI API with the provided API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def call_genai(prompt):
    """
    Call the GenAI API to generate a response based on the given prompt.

    Args:
        prompt (str): The prompt for generating the response.

    Returns:
        str: The generated response.
    """
    try:
        # Set up generation configuration
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 0,
            "max_output_tokens": 8192,
        }

        # Set up safety settings
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]

        # Initialize the GenerativeModel
        model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                      generation_config=generation_config,
                                      safety_settings=safety_settings)

        # Start a chat session
        convo = model.start_chat(history=[])

        # Send the prompt to the chat session
        convo.send_message(prompt)

        # Return the last text message from the chat session
        return convo.last.text

    except genai.exceptions.GenAIException as e:
        # Handle GenAI API exceptions
        print(f"GenAI API Exception: {e}")
        return "Sorry, an error occurred while processing your request."
    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred: {e}")
        return "Sorry, an unexpected error occurred."


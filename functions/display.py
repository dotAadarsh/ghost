import os
import base64
import requests
from io import BytesIO
import io
import streamlit as st 

def display_pdf(url):
  """Downloads and displays a PDF from a URL in a Streamlit app."""
  try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for unsuccessful downloads
  except requests.exceptions.RequestException as e:
    st.error(f"Failed to download PDF: {e}")
    return

  # Read PDF content as bytes
  pdf_bytes = io.BytesIO(response.content)

  # Encode bytes in base64
  base64_pdf = base64.b64encode(pdf_bytes.getvalue()).decode("utf-8")

  # Display PDF using embed tag (adjust width and height as needed)
  html = F"""
    <embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="400" type="application/pdf">
  """
  with st.expander("Sanitized File"):
    st.markdown(html, unsafe_allow_html=True)


import io
import base64
import requests
from streamlit import st

def display_pdf(url):
  """Downloads and displays a PDF from a URL in a Streamlit app.

  This function downloads the PDF from the given URL, displays an error message
  if download fails, and then displays the PDF using a server-side rendered approach.
  """
  try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for unsuccessful downloads
  except requests.exceptions.RequestException as e:
    st.error(f"Failed to download PDF: {e}")
    return

  # Render PDF bytes on server and display in iframe
  pdf_bytes = io.BytesIO(response.content)
  with st.caching.server.hold():  # Cache PDF rendering on server
    b64_pdf = base64.b64encode(pdf_bytes.getvalue()).decode("utf-8")
    html = F"""
      <iframe src="data:application/pdf;base64,{b64_pdf}" width="700" height="400"></iframe>
    """
  st.markdown(html, unsafe_allow_html=True)

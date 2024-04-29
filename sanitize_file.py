import pangea.exceptions as pe
from pangea.config import PangeaConfig
from pangea.response import TransferMethod
from pangea.services import Sanitize
from pangea.services.sanitize import SanitizeContent, SanitizeFile, SanitizeShareOutput
from pangea.services import Share
import os
from dotenv import load_dotenv
import streamlit as st
import requests
import json
import io

# Load environment variables from .env file
load_dotenv()

token = os.getenv("PANGEA_TOKEN")
assert token

domain = os.getenv("PANGEA_DOMAIN")
assert domain

config = PangeaConfig(domain)

# Create the Sanitize client with its token and config
client = Sanitize(token, config)

def sanitize_file(uploaded_file, save_path):

    try:
        # Create Sanitize file information, setting scan and CDR providers
        file_scan = SanitizeFile(scan_provider="crowdstrike", cdr_provider="apryse")

        # Create content sanitization config
        content = SanitizeContent(
            url_intel=True,
            url_intel_provider="crowdstrike",
            domain_intel=True,
            domain_intel_provider="crowdstrike",
            defang=True,
            defang_threshold=20,
            remove_interactive=True,
            remove_attachments=True,
            redact=True,
        )

        # Enable share output and its folder
        share_output = SanitizeShareOutput(enabled=True, output_folder="sdk_examples/sanitize/")

        with open(save_path, "rb") as f:
            # Make the request to sanitize service
            response = client.sanitize(
                file=f,
                # Set transfer method to post-url
                transfer_method=TransferMethod.POST_URL,
                file_scan=file_scan,
                content=content,
                share_output=share_output,
                uploaded_file_name=uploaded_file.name,
            )

            if response.result is None:
                st.write(response)
                print("Failed to get response")
                sys.exit(1)
                
            # st.sidebar.json(response)
            print("Sanitize request success")
            file_share_id = response.result.dest_share_id
            print(f"\tFile share id: {file_share_id}")
            print(f"\tRedact data: {response.result.data.redact}")
            print(f"\tDefang data: {response.result.data.defang}")
            print(f"\tCDR data: {response.result.data.cdr}")
            print(f"\tPresigned url: {response.result.dest_url}")

            share_url = "https://share.aws.us.pangea.cloud/v1beta/get"
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }

            data = {"transfer_method": "dest-url", "id": f"{file_share_id}"} 

            share_response = requests.post(share_url, headers=headers, data=json.dumps(data), verify=False)

            # Handle the response based on your needs
            if share_response.status_code == 200:
                res = share_response.json()
                print(res["result"]["dest_url"])
                sanitize_file_location = res["result"]["dest_url"]
            else:
                st.toast(f"Error: {share_response.text}")
            

            if response.result.data.malicious_file:
                st.toast("File IS malicious")
            else:
                st.toast("File is NOT malicious")

            return sanitize_file_location

    except pe.PangeaAPIException as e:
        print(e)

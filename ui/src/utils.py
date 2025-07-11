import streamlit as st
import requests

backend_url = "http://doclasiq_api:8001/api/classify"

def classify_doc(file):

    files = {"file": (file.name, file, file.type)}
    response = requests.post(backend_url, files=files)

    # Check the response status
    if response.status_code == 200:
        print("Request successful!")
        print(f"Response: {response.json()}")
        res = response.json()
        return res["classified_output"], res["extracted_data"]
    else:
        print(f"Request failed with status code {response.status_code}")
        print(f"Error: {response.text}")
        return response.text, response.text
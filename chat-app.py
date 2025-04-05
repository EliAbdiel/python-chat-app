import streamlit as st  # For creating web interface
import requests as req  # For making HTTP requests
import json  # For JSON data handling

from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables

API_URL = os.environ["SPRING_BOOT_ENDPOINT"] # Spring Boot API URL

# Create a container for chat messages with fixed height
messages = st.container(height=900)

# Get user input through chat interface
if prompt := st.chat_input("Say something"):
    # Display user message in chat
    messages.chat_message("user").write(prompt)
    
    try:
        # Prepare request payload
        payload = {"query": prompt}
        
        # Send POST request to API
        response = req.post(API_URL, json=payload)
        
        # Handle successful response
        if response.status_code == 200:
            # Parse JSON response
            result = response.json()
            
            # Extract text from nested response structure
            text = result["candidates"][0]["content"]["parts"][0]["text"]
            
            # Display assistant's response in chat
            messages.chat_message("assistant").write(text)
            
    except req.exceptions.RequestException as e:
        # Handle any request-related errors
        messages.chat_message("assistant").write("Sorry, I can't understand you.")
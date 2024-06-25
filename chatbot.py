import streamlit as st
import requests
import json

# Function to generate response from AI
def generate_response(prompt, history):
    url = "http://localhost:11434/api/generate"
    
    # Constructing context for the AI based on chat history
    context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history])
    full_prompt = f"{context}\nHuman: {prompt}\nAssistant:"
    
    # Data payload for API request
    data = {
        "model": "phi3",
        "prompt": full_prompt
    }
    
    try:
        # Making POST request to AI model endpoint
        response = requests.post(url, json=data)
        response.raise_for_status()  # Raise error if request fails
        
        full_response = ""
        for line in response.iter_lines():
            if line:
                json_response = json.loads(line)
                if 'response' in json_response:
                    full_response += json_response['response']
                if json_response.get('done', False):
                    break
        
        return full_response.strip()  # Return AI response
    except requests.RequestException as e:
        return f"Error: Unable to generate response - {str(e)}"

# System prompt for the AI's role and responsibilities
system_prompt = """
You are an AI movie recommendation assistant created by Aditi. Your role is to:

1. Provide personalized movie recommendations based on user preferences.
2. Suggest movies from various genres and eras, catering to different tastes.
3. Offer information about movies, actors, directors, and reviews.
4. Aim to enhance user's movie-watching experience with thoughtful suggestions.

Your goal is to assist users in discovering movies they'll enjoy, leveraging your knowledge and algorithms to make relevant recommendations.
"""

# Setting Streamlit page configuration
st.set_page_config(page_title="Movie Recommender by Aditi", page_icon="🎥", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Raleway:wght@300;600&display=swap');
    .stApp {
        background-color: #141414;
        color: #e5e5e5;
    }
    .stTextInput > div > div > input {
        background-color: #333;
        color: #e5e5e5;
        border: 1px solid #e5e5e5;
    }
    .stButton > button {
        background-color: #e50914;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        transition: background-color 0.3s, transform 0.3s;
    }
    .stButton > button:hover {
        background-color: #f40612;
        transform: scale(1.05);
    }
    .stButton > button:active {
        transform: scale(0.95);
    }
    .social-icons {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 10px;
    }
    .social-icons a {
        margin: 0 10px;
        transition: transform 0.3s, filter 0.3s;
    }
    .social-icons a:hover {
        transform: scale(1.2);
        filter: brightness(1.2);
    }
    .movie-title {
        color: #e50914;
        font-size: 48px;
        font-family: 'Raleway', sans-serif;
        font-weight: 600;
        text-align: center;
        margin-bottom: 20px;
    }
    .messages-container {
        background-color: #222;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        max-height: 300px;
        overflow-y: auto;
    }
    .messages-container p {
        margin: 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Layout structure using Streamlit columns
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.empty()

with col2:
    # Displaying AI assistant's title
    st.markdown('<div class="movie-title">Movie GPT</div>', unsafe_allow_html=True)
    
    # Initializing or retrieving chat history from session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Displaying chat history
    st.markdown('<div class="messages-container">', unsafe_allow_html=True)
    for message in st.session_state.messages:
        role = "User" if message['role'] == "Human" else "Bot"
        st.markdown(f"**{role}:** {message['content']}")
    st.markdown('</div>', unsafe_allow_html=True)

    # Input field for user prompt
    prompt = st.text_input("Ask me about movies:")

    # Button to send user prompt
    if st.button("Send"):
        if prompt:
            st.session_state.messages.append({"role": "Human", "content": prompt})
            response = generate_response(prompt, st.session_state.messages)
            st.session_state.messages.append({"role": "Bot", "content": response})
    
    # Button to clear chat history
    if st.button("Clear Chat"):
        st.session_state.messages = []

with col3:
    st.empty()

# Footer section with social links
st.markdown("""
    <div class="social-icons">
        <a href="https://github.com/yadavadit" target="_blank"><img src="https://img.icons8.com/material-outlined/48/e50914/github.png"/></a>
        <a href="https://www.linkedin.com/in/yaditi/" target="_blank"><img src="https://img.icons8.com/color/48/e50914/linkedin.png"/></a>
        <a href="mailto:yadavadit@northeastern.edu"><img src="https://img.icons8.com/color/48/e50914/gmail.png"/></a>
    </div>
    """, unsafe_allow_html=True)

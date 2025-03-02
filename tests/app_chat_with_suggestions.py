import streamlit as st
import random

# Set page config
st.set_page_config(page_title="Chat with Examples", layout="wide")

# Define your examples
examples = [
    "How are you?",
    "Is the sky blue?", 
    "Will it rain tomorrow?",
    "Is this a good question?",
    "Are you sure about that?"
]

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to handle sending a message and getting response
def send_message(message):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": message})
    
    # Generate bot response
    bot_response = random.choice(["Yes", "Definitely yes"])
    
    # Add bot response to chat history
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

# Display title
st.title("Chat with Example Suggestions")

# Display example chips before the chat input
st.write("Click on an example to send it:")
example_cols = st.columns(len(examples))
for i, col in enumerate(example_cols):
    if col.button(examples[i], key=f"example_{i}", use_container_width=True):
        send_message(examples[i])
        st.rerun()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Type your message here...")

# Handle user input from chat box
if user_input:
    send_message(user_input)
    st.rerun()  # Add rerun here to force refresh for chat input too
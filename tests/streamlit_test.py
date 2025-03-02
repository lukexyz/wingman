import streamlit as st
import random

# Set page config
st.set_page_config(page_title="Chat with Examples", layout="wide")

# Define your examples
examples = [
    "How are you?",
    "Is the sky blue?", 
    "Will it rain tomorrow?"
]

# Initialize session state for messages and markdown content
if "messages" not in st.session_state:
    st.session_state.messages = []

if "markdown_content" not in st.session_state:
    st.session_state.markdown_content = """
    # Welcome to the Chat Demo
    
    This is a demonstration of a Streamlit chat interface with examples.
    
    - Click on example buttons to send pre-defined messages
    - Type your own messages in the chat input
    - This area can display documentation, results, or any markdown content
    
    *The content in this area will update based on the conversation.*
    """

# Function to handle sending a message and getting response
def send_message(message):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": message})
    
    # Generate bot response
    bot_response = random.choice(["Yes", "Definitely yes"])
    
    # Add bot response to chat history
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    
    # Update markdown content based on the message
    # This is just a simple example - you can make this more sophisticated
    st.session_state.markdown_content = f"""
    
    You asked: **{message}**
    
    The response was: **{bot_response}**
    """

# Create two columns for the layout
left_col, right_col = st.columns([1, 1])

# Left column: Chat interface
with left_col:
    st.title("Chat")
    
    # Display example chips before the chat input
    example_cols = st.columns(len(examples))
    for i, col in enumerate(example_cols):
        if col.button(examples[i], key=f"example_{i}", use_container_width=True):
            send_message(examples[i])
            st.rerun()

    
    # Container for chat messages with fixed height
    with st.container():
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        # Display chat history in the container
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input at the bottom of the left column
    user_input = st.chat_input("Type your message here...")
    
    # Handle user input from chat box
    if user_input:
        send_message(user_input)
        st.rerun()

# Right column: Markdown display
with right_col:
    st.title("Evaluation")
    
    # Add a container with custom styling for the markdown content
    with st.container(border=True):
        # Display the markdown content
        st.markdown(st.session_state.markdown_content)
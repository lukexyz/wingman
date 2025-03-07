import claudette
import gradio as gr

def create_chat_interface(model, system_prompt="You are a helpful and concise assistant."):
    """Create and configure a chat interface using Gradio.
    
    Args:
        model: The Claude model to use for chat completion
        system_prompt (str): The system prompt to initialize the chat with
        
    Returns:
        gr.ChatInterface: Configured chat interface object
    """
    chat = claudette.Chat(model, sp=system_prompt)
    
    def respond(user_message, history):
        print("Messages received so far:", user_message)  # Print to see outside gradio
        c = chat(user_message)
        return c.content[0].text
    
    chatbot = gr.ChatInterface(
        fn=respond,
        examples=["Hello Neo.. let's begin."],
        theme="default"
    )
    
    return chatbot

if __name__ == "__main__":
    # Example usage
    model = claudette.models[3]  # Using claude-3-haiku-20240307
    chatbot = create_chat_interface(model)
    chatbot.launch(inline=True) 
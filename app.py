"""Wingman - An AI-powered interview practice and conversation assistant."""
import claudette
import gradio as gr
from pathlib import Path
import random
import time
from utils import custom_css
from wingman.chat import INTERVIEW_INSTRUCTIONS
from wingman.interview import DEFAULT_QUESTIONS

# Global variables for chat state
chat_instance = None
is_first_interaction = True

def read_file(file_obj):
    if file_obj is None:
        return ""
    content = file_obj.read().decode('utf-8')
    return content

def save_file(file_path, content):
    with open(file_path, 'wb') as file_obj:
        file_obj.write(content.encode('utf-8'))

def initialize_interview_chat():
    """Initialize the interview chat with context and return initial questions."""
    global chat_instance
    
    try:
        context_file = Path('nbs/docs/analytics.md')
        context_media = context_file.read_text(encoding='utf-8')
    except:
        context_media = ""  # Fallback if file not found
        
    system_prompt = """You are a helpful and concise assistant."""
    model = claudette.models[3]
    
    chat_instance = claudette.Chat(model, sp=system_prompt)
    
    # Get initial interview questions
    prompt = f"""Can you come up with 10 realistic questions a hiring manager might ask in an opening interview? The job title for this role is: SENIOR RESEARCH ANALYST.
            Do not add any additional commentary, just list 10 questions only. Start each question with a new line starting like:
                [Q1] ... 
                [Q2] ...
                My resume is in the project docs, the core competencies for a senior analyst are below:
                {context_media}"""
    
    questions = chat_instance(prompt)
    save_file(Path('templates/questions.txt'), questions.content[0].text)

    return chat_instance(prompt)

def respond(user_message, history):
    """Handle chat responses and initialize interview on first interaction."""
    global chat_instance, is_first_interaction
    
    print("Messages received so far:", user_message)  # Print to see outside gradio
    
    # Initialize chat on first interaction
    if is_first_interaction and user_message.strip().lower() == "hello. let's begin.":
        is_first_interaction = False
        initial_questions = initialize_interview_chat()
        #return f"Welcome and good luck. Here is you first interview question:\n{initial_questions.content[0].text}\n\n"
        response = chat_instance(f"""System message: {INTERVIEW_INSTRUCTIONS}, 
                                     User: {user_message}""")
        return f"Good luck, here is your first question.\n {response.content[0].text}"

    # Regular chat interaction
    if chat_instance is None:
        chat_instance = claudette.Chat(claudette.models[3], sp="You are a helpful and concise assistant.")
    
    response = chat_instance(f'System message: {INTERVIEW_INSTRUCTIONS}, User: {user_message}')
    return response.content[0].text



def update_system_prompt(file_obj, scenario):
    content = read_file(file_obj) if file_obj else ""
    if scenario == "Technical Interview":
        base_prompt = "You are a technical interviewer conducting an interview. "
    else:
        base_prompt = "You are having a friendly conversation. "
    
    return base_prompt + f"\nContext:\n{content}"

with gr.Blocks(
    title="Wingman", 
    theme="shivi/calm_seafoam",
    css=custom_css) as demo: 

    html = gr.HTML(value="""
        <div class="main-header" style="text-align: center; width: 100%;">
            <h1 style='font-size: 2em; margin: 0.0em 0;'> 
                <span style='
                    background-color: rgba(255, 255, 0, 0.3);
                    padding: 0px 8px;
                    border-radius: 8px;
                '>WINGMAN🎙️</span>
            </h1>
        </div>
    """)
    
    # Add accordion for the top section
    with gr.Accordion("📝 System Settings", open=False):
        with gr.Row():
            file = gr.File(label="Included in system prompt.", file_types=[".txt"])
            with gr.Column():
                radio = gr.Radio(["Technical Interview", "Friendly neighbour"], label='Scenario')
                system_prompt = gr.Textbox(label="System Prompt")

    # Connect the file upload and radio to update system prompt
    file.change(fn=update_system_prompt, 
                inputs=[file, radio], 
                outputs=system_prompt)
    radio.change(fn=update_system_prompt,
                inputs=[file, radio],
                outputs=system_prompt)
    
    with gr.Row():
        with gr.Column():
            markdown = gr.Markdown(value="# CHAT")
            button = gr.Button(variant="primary", value="🎙️ Record") # TODO - Incorporate with `fastrtc`

            chatbot = gr.ChatInterface(
                fn=respond,
                examples=["Hello. Let's begin."],
                theme="default"
            )

        with gr.Column():
            markdown_2 = gr.Markdown(value="# EVALUATION")
            with gr.Group():
                textbox_2 = gr.Textbox(value="Question: What skills to you bring to this role?", label=None, show_label=False)
                highlighted_eval = gr.HighlightedText(
                    value=[
                        "GOOD:",
                        ["Python", "positive"],
                        " strengths for data exploration and visualization.\n",
                        ["SQL", "positive"],
                        "'s importance as a foundational tool in analytics workflows.\n",
                        ["10 years", "highlight"],
                        " experience with SQL\n\n",
                        "BAD:\n",
                        ["generic", "negative"],
                        " response rather than tailored to the position\n",
                        ["Missing", "negative"],
                        " concrete examples of how these tools would be applied"
                    ],
                    show_legend=True,
                    color_map={
                        "positive": "green",
                        "negative": "red",
                        "highlight": "yellow"
                    }
                )
            with gr.Row():
                number = gr.Number(label="Linguistic Clarity", value=6.1, info="rating/10")
                number_2 = gr.Number(label="Confidence", value=7.0, info="rating/10")
                number_3 = gr.Number(label="Technical Expertise", value=6.8, info="rating/10")
                number_4 = gr.Number(label="Strategic Thinking", value=5.2, info="rating/10")

demo.launch()
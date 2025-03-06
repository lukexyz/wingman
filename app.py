import gradio as gr
import claudette
from pathlib import Path

def read_file(file_obj):
    if file_obj is None:
        return ""
    content = file_obj.read().decode('utf-8')
    return content

def update_system_prompt(file_obj, scenario):
    content = read_file(file_obj) if file_obj else ""
    if scenario == "Technical Interview":
        base_prompt = "You are a technical interviewer conducting an interview. "
    else:
        base_prompt = "You are having a friendly conversation. "
    
    return base_prompt + f"\nContext:\n{content}"

with gr.Blocks() as demo:
    html = gr.HTML(value="""
        <h1 style='font-size: 2em; margin: 0.0em 0;'>
            wingman 
            <span style='
                background-color: rgba(255, 255, 0, 0.3);
                padding: 0px 8px;
                border-radius: 8px;
            '>highlighter</span>
            🎙️
        </h1>
    """)
    
    # Add accordion for the top section
    with gr.Accordion("System Settings", open=True):
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
            button = gr.Button(variant="primary", value="🎙️ Record")
            chatbot = gr.Chatbot()
            multimodaltextbox = gr.MultimodalTextbox(lines=1.0, label=" ")

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

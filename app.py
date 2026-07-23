import gradio as gr
from src.research import research

def generate(query):
    result = research(query)

    if result is None:
        return "Something went wrong."

    return result["summary"]

with gr.Blocks() as demo:
    gr.Markdown("# 🔍 ResearchPilot AI")

    query = gr.Textbox(label="Research Question")

    output = gr.Markdown()

    button = gr.Button("Generate")

    button.click(
        fn=generate,
        inputs=query,
        outputs=output,
    )

demo.launch()
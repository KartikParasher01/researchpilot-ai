import gradio as gr
from src.research import research

def generate_report(query, progress=gr.Progress()):
    response = research(query,progress)

    if not response["success"]:
        return (
            response["message"],
            "",
            "",
            "",
            "",
        )

    # Get the LLM response
    result = response["data"]

    # Format confidence
    confidence = result["confidence"]

    if hasattr(confidence, "value"):
        confidence = confidence.value

    confidence = {
        "High": "🟢 High",
        "Medium": "🟡 Medium",
        "Low": "🔴 Low",
    }.get(confidence, confidence)

    # Format key points
    key_points_md = "\n".join(
        f"- {point}" for point in result["key_points"]
    )

    # Format sources
    sources_md = "\n".join(
        f"- [{source['title']}]({source['url']})"
        for source in result["sources"]
    )

    return (
        result["summary"],
        key_points_md,
        result["analysis"],
        confidence,          # <- Use formatted confidence
        sources_md,
    )


with gr.Blocks(title="ResearchPilot AI") as demo:

    gr.Markdown("""
    # 🔍 ResearchPilot AI

    ### Your personal AI Research Assistant
    """)

    query = gr.Textbox(
        label="Research Question",
        placeholder="Ask me anything.",
        lines=3,
    )

    button = gr.Button(
        "🚀 Generate Research Report",
        variant="primary"
    )

    with gr.Group():
        gr.Markdown("## 📄 Summary")
        summary = gr.Markdown()

    with gr.Group():
        gr.Markdown("## 📌 Key Points")
        key_points = gr.Markdown()

    with gr.Group():
        gr.Markdown("## 🧠 Analysis")
        analysis = gr.Markdown()

    with gr.Group():
        gr.Markdown("## 📊 Confidence")
        confidence = gr.Textbox(interactive=False)

    with gr.Group():
        gr.Markdown("## 🔗 Sources")
        sources = gr.Markdown()

    button.click(
        fn=generate_report,
        inputs=query,
        outputs=[
            summary,
            key_points,
            analysis,
            confidence,
            sources,
        ],
    )

# demo.launch()
demo.launch(debug=True)
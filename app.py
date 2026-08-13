import os
import gradio as gr

from src.research import research


def generate_report(query, progress=gr.Progress()):
    if not query or not query.strip():
        return (
            "Please enter a research question.",
            "",
            "",
            "",
            "",)

    response = research(query.strip(), progress)

    if not response["success"]:
        return (
            response["message"],
            "",
            "",
            "",
            "",
        )

    result = response["data"]

    # Format confidence
    confidence = result["confidence"]

    if hasattr(confidence, "value"):
        confidence = confidence.value

    confidence_labels = {
        "High": "🟢 High",
        "Medium": "🟡 Medium",
        "Low": "🔴 Low",
    }

    confidence = confidence_labels.get(confidence, confidence)

    # Format key points
    key_points_md = "\n".join(
        f"- {point}" for point in result["key_points"])

    # Format sources
    sources_md = "\n".join(
        f"- [{source['title']}]({source['url']})"
        for source in result["sources"])

    return (result["summary"],key_points_md,result["analysis"],confidence,sources_md,)


with gr.Blocks(title="ResearchPilot AI") as demo:

    gr.Markdown(
        """
        # 🔎 ResearchPilot AI

        ### Your personal AI Research Assistant
        """)

    query = gr.Textbox(
        label="Research Question",
        placeholder="Ask me anything.",
        lines=3,
    )

    button = gr.Button(
        "🚀 Generate Research Report",
        variant="primary",
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


if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=int(os.getenv("PORT", 7860)),
    )
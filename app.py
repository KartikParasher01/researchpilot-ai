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
            "",
        )

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

    confidence_display = {
        "High": "🟢 High",
        "Medium": "🟡 Medium",
        "Low": "🔴 Low",
    }.get(confidence, confidence)

    # Format key points
    key_points_md = "\n".join(
        f"• {point}" for point in result["key_points"]
    )

    # Format sources
    sources_md = "\n\n".join(
        f"**{source['title']}**  \n"
        f"[Read source ↗]({source['url']})"
        for source in result["sources"]
    )

    return (
        result["summary"],
        key_points_md,
        result["analysis"],
        confidence_display,
        sources_md,
    )


css = """
#app-container {
    max-width: 1100px;
    margin: auto;
}

#hero {
    text-align: center;
    padding: 30px 20px 10px 20px;
}

#hero h1 {
    font-size: 42px;
    margin-bottom: 8px;
}

#hero p {
    font-size: 18px;
    opacity: 0.75;
}

#question-box textarea {
    font-size: 17px !important;
}

#generate-btn {
    width: 100%;
    margin-top: 10px;
}

.section-card {
    border-radius: 12px;
    padding: 8px;
}

#confidence-box textarea {
    font-size: 18px !important;
    font-weight: 600;
}

.footer {
    text-align: center;
    opacity: 0.6;
    font-size: 13px;
    padding: 25px 0;
}
"""


with gr.Blocks(
    title="ResearchPilot AI",
) as demo:

    with gr.Column(elem_id="app-container"):

        # ---------------------------------------------------------
        # Header
        # ---------------------------------------------------------

        gr.Markdown(
            """
            <div id="hero">

            # 🔎 ResearchPilot AI

            ### Research the web. Understand the answer.

            Ask a question and ResearchPilot searches the web,
            analyzes relevant sources, and generates a structured report.

            </div>
            """
        )

        # ---------------------------------------------------------
        # Research Question
        # ---------------------------------------------------------

        with gr.Group():

            query = gr.Textbox(
                label="Research Question",
                placeholder=(
                    "Example: What are the major challenges "
                    "facing MSMEs in India?"
                ),
                lines=4,
                elem_id="question-box",
            )

            button = gr.Button(
                "🚀 Generate Research Report",
                variant="primary",
                size="lg",
                elem_id="generate-btn",
            )

        # ---------------------------------------------------------
        # Summary
        # ---------------------------------------------------------

        gr.Markdown("## 📄 Research Summary")

        summary = gr.Markdown(
            elem_classes=["section-card"]
        )

        # ---------------------------------------------------------
        # Key Findings + Confidence
        # ---------------------------------------------------------

        with gr.Row():

            with gr.Column(scale=2):

                gr.Markdown("## 📌 Key Findings")

                key_points = gr.Markdown(
                    elem_classes=["section-card"]
                )

            with gr.Column(scale=1):

                gr.Markdown("## 📊 Confidence")

                confidence = gr.Textbox(
                    interactive=False,
                    elem_id="confidence-box",
                )

        # ---------------------------------------------------------
        # Analysis
        # ---------------------------------------------------------

        gr.Markdown("## 🧠 Analysis")

        analysis = gr.Markdown(
            elem_classes=["section-card"]
        )

        # ---------------------------------------------------------
        # Sources
        # ---------------------------------------------------------

        gr.Markdown("## 🔗 Sources")

        sources = gr.Markdown(
            elem_classes=["section-card"]
        )

        # ---------------------------------------------------------
        # Footer
        # ---------------------------------------------------------

        gr.Markdown(
            """
            <div class="footer">

            ResearchPilot AI · Web Research Assistant

            <br>

            Always verify important information against the original sources.

            </div>
            """
        )

        # ---------------------------------------------------------
        # Generate Report
        # ---------------------------------------------------------

        button.click(
            fn=generate_report,
            inputs=query,
            outputs=[summary,key_points,analysis,confidence,sources,],)


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0",server_port=int(os.getenv("PORT", 7860)),
        css=css,theme=gr.themes.Soft(),)
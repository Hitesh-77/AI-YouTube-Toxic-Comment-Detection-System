import gradio as gr

with gr.Blocks(
    title = "AI YouTube Toxic Comment Detection System"
    ) as demo:

    with gr.Column():
        gr.Markdown(
            """
            # 🛡️ AI YouTube Toxic Comment Detection System

            Paste a YouTube video URL.

            The system will:
            
            ✅ Fetch comments

            ✅ Analyze every comment

            ✅ Show dashboard statistics

            ✅ Display all comments

            ✅ Click any comment to view detailed ML analysis
            """
        )

        youtube_url = gr.Textbox(
            label="YouTube Video URL",
            placeholder="Paste a YouTube video URL here..."
        )

        max_comments = gr.Slider(
            minimum=10,
            maximum=500,
            step=10,
            value=100,
            label="Maximum Comments",
            interactive=True
        )


if __name__ == "__main__":
    demo.launch(
        theme = gr.themes.Soft(
                primary_hue="blue",
                secondary_hue="slate"
            ),
        css_paths = "style.css"
        )
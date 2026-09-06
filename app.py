import gradio as gr
from youtube_comments import fetch_youtube_comments
from predict import analyze_all_comments

def fetch_and_analyze(youtube_url, max_comments):
    comments = fetch_youtube_comments(youtube_url, max_comments)
    results = analyze_all_comments(comments)

    total_comments = len(results)
    toxic_comments = sum(
        row[2] == "🔴 Toxic"
        for row in results
    )
    safe_comments = sum(
        row[2] == "🟢 Non Toxic"
        for row in results
    )
    toxicity_rate = (
        toxic_comments / total_comments * 100
        if total_comments > 0
        else 0
    )

    return (
        total_comments,
        safe_comments,
        toxic_comments,
        round(toxicity_rate, 2),
        results
    )  

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

        fetch_btn = gr.Button(
            "Fetch & Analyze Comments",
            variant="primary"
        )
        gr.Markdown("---")

        gr.Markdown("## 📊 Dashboard")
        with gr.Row():
            total_comments = gr.Number(
                label="Total Comments",
                value = 0,
                interactive = False
            )

            safe_comments = gr.Number(
                label="Safe Comments",
                value = 0,
                interactive = False
            )
    
            toxic_comments = gr.Number(
                label="Toxic Comments",
                value = 0,
                interactive = False
            )

            toxicity_rate = gr.Number(
                label="Toxicity Rate",
                value = 0,
                interactive = False
            )
        gr.Markdown("---")

        gr.Markdown("## 💬 YouTube Comments")

        comments_table = gr.Dataframe(
            headers = ["Username", "Comment", "Prediction", "Toxicity Score (%)"],
            label = "Fetched Comments",
            interactive = False
        )
        gr.Markdown("---")

        gr.Markdown("## 🔍 Selected Comment Analysis")

        with gr.Row():
            original_comment = gr.Textbox(
                label = "Original Comment",
                interactive = False,
                lines = 3
            )

            preprocessed_comment = gr.Textbox(
                label = "Preprocessed Comment",
                interactive = False,
                lines = 3
            )

        with gr.Row():
            prediction = gr.Textbox(
                label="Prediction",
                interactive=False
            )

            confidence = gr.Textbox(
                label="Confidence",
                interactive=False
            )
        gr.Markdown("---")

        prediction_details = gr.Dataframe(
            headers=["Category", "Probability (%)", "Prediction"],
            label="Prediction Details",
            interactive=False
        )
        gr.Markdown("---")

        probability_plot = gr.Plot(
            label="Probability Distribution"
        )

        fetch_btn.click(
            fn = fetch_and_analyze,
            inputs = [youtube_url, max_comments],
            outputs = [
                total_comments,
                safe_comments,
                toxic_comments,
                toxicity_rate,
                comments_table
            ]
        )


            


if __name__ == "__main__":
    demo.launch(
        theme = gr.themes.Soft(
                primary_hue="blue",
                secondary_hue="slate"
            ),
        css_paths = "style.css"
        )
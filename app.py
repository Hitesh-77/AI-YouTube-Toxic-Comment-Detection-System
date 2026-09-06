import gradio as gr
from youtube_comments import fetch_youtube_comments
from predict import analyze_all_comments, predict_comment, labels
import matplotlib.pyplot as plt
import numpy as np

def show_comment_details(evt: gr.SelectData, results):
    row_index = evt.index[0]
    selected_row = results[row_index]

    selected_comment = selected_row[1]
    cleaned_comment, probabilities, predictions = predict_comment(
        selected_comment
    )

    if np.sum(predictions) == 0:
        status = "🟢 Non Toxic"
    else:
        status = "🔴 Toxic"

    toxicity_score = np.max(probabilities) * 100

    prediction_details = []
    for label, probability, prediction_value in zip(labels, probabilities, predictions):
        prediction_details.append([
            label,
            round(probability * 100, 2),
            "Positive" if prediction_value == 1 else "Negative"
        ])

    probability_plot = plt.figure(figsize = (8, 4))

    plt.bar(
        labels,
        probabilities * 100
    )

    plt.title("Toxicity Probability Distribution")
    plt.xlabel("Category")
    plt.ylabel("Probability (%)")
    plt.ylim(0, 100)

    plt.xticks(rotation=30)
    plt.tight_layout()

    return (
        selected_comment,
        cleaned_comment,
        status,
        f"{toxicity_score:.2f}%",
        prediction_details,
        probability_plot
    )

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
        results,
        results
    )  

with gr.Blocks(
    title = "AI YouTube Toxic Comment Detection System"
    ) as demo:

    results_state = gr.State()
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
            interactive = False,
            datatype = ["str", "str", "str", "number"],
            wrap = True
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

            toxicity_score = gr.Textbox(
                label="Toxicity Score",
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
                comments_table,
                results_state
            ]
        )

        comments_table.select(
            fn = show_comment_details,
            inputs = [results_state],
            outputs=[
                original_comment,
                preprocessed_comment,
                prediction,
                toxicity_score,
                prediction_details,
                probability_plot
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
import joblib
import numpy as np
import pandas as pd
from preprocessing import clean_text

MODEL_PACKAGE = joblib.load("best_lr_toxic_comment_model.pkl")

model = MODEL_PACKAGE["model"]
thresholds = MODEL_PACKAGE["thresholds"]
labels = MODEL_PACKAGE["labels"]

def predict_comment(comment):
    cleaned_comment = clean_text(comment)

    new_data = pd.DataFrame({
        "clean_comment": [cleaned_comment],
        "comment_length": [len(comment)],
        "word_count": [len(comment.split())]
    })

    probs = model.predict_proba(new_data)

    predictions = np.zeros_like(probs, dtype=int)

    for i, threshold in enumerate(thresholds):
        predictions[:, i] = (
            probs[:, i] >= threshold
        ).astype(int)

    return cleaned_comment, probs[0], predictions[0]


def analyze_all_comments(comments):
    result = []
    for row in comments:
        username = row[0]
        comment = row[1]

        cleaned_comment, probabilities, predictions = predict_comment(comment)
        
        if np.sum(predictions) == 0:
            status = "🟢 Non Toxic"
        else:
            status = "🔴 Toxic"

        toxicity_score = np.max(probabilities) * 100

        result.append([
            username,
            comment,
            status,
            round(toxicity_score, 2)
        ])

    return result




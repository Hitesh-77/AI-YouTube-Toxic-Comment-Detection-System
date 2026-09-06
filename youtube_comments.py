import os 
import re 
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

def extract_video_id(youtube_url):
    patterns = [
        r"(?:v=)([^&]+)",
        r"(?:youtu\.be/)([^?]+)",
        r"(?:youtube\.com/shorts/)([^?]+)"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, youtube_url)
        if match:
            return match.group(1)

    return None

def fetch_youtube_comments(youtube_url, max_comments = 100):
    video_id = extract_video_id(youtube_url)
    if video_id is None:
        raise ValueError("Invalid Youtube URL")

    youtube = build(
        "youtube",
        "v3",
        developerKey=API_KEY
    )

    
    comments = []
    next_page_token = None

    while len(comments) < max_comments:
        request = youtube.commentThreads().list(
            part = "snippet",
            videoId = video_id,
            maxResults = min(100, max_comments - len(comments)),
            pageToken = next_page_token,
            textFormat = "plainText",
            order = "relevance"
        )

        response = request.execute()
        for item in response["items"]:

            comment_data = item["snippet"]["topLevelComment"]["snippet"]
            username = comment_data["authorDisplayName"]
            comment = comment_data["textDisplay"]

            comments.append(
                [username, comment]
            )

            if len(comments) >= max_comments:
                break

            
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break
            
    return comments        

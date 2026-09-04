import streamlit as st

st.set_page_config(
    page_title="AI Toxic Comment Detection System",
    page_icon="🛡️",
    layout="centered"
)

with open("style.css", "r", encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# header
st.markdown("""
    <div class = "main-title">
        🛡️ AI YouTube Toxic Comment Detection System
    </div>
""", unsafe_allow_html=True)

# intro
st.markdown("""
    <div class = "intro">
        Paste a YouTube video URL.
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="intro" style="margin-top: 8px;">
        The system will:
    </div>

    <div class="checklist">
        <div><span class="check">✅</span> Fetch comments</div>
        <div><span class="check">✅</span> Analyze every comment</div>
        <div><span class="check">✅</span> Show dashboard statistics</div>
        <div><span class="check">✅</span> Display all comments</div>
        <div><span class="check">✅</span> Click any comment to view detailed ML analysis</div>
    </div>
""", unsafe_allow_html=True)

st.markdown(
    """
    <div class="youtube-url-label">
        YouTube Video URL
    </div>
    """,
    unsafe_allow_html=True
)

video_url = st.text_input(
    label="YouTube Video URL",
    placeholder="https://www.youtube.com/watch?v=...",
    label_visibility="collapsed"
)

st.markdown("""
    <div class="comments-slider-label">
        Maximum Comments
    </div>
""", unsafe_allow_html=True)

max_comments = st.slider(
    label = "Maximum Comments",
    label_visibility = "collapsed",
    value = 100,
    min_value = 10,
    max_value = 500,
    step = 10
)

if st.button("Fetch & Analyze Comments",use_container_width=True):
    st.write("Button clicked")

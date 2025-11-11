# app.py
import streamlit as st
from transformers import pipeline
import pandas as pd
import plotly.express as px
from datetime import datetime
import random
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import BytesIO
from fpdf import FPDF
import base64

# -----------------------------
# APP CONFIG
# -----------------------------
st.set_page_config(page_title="AI Emotion Companion Dashboard", layout="wide", page_icon="💬")
st.title("💬 AI Emotion Companion — Sentiment & Emotion Dashboard")
st.caption("An emotion-aware conversational AI with analytics, exports, and empathy. Powered by Hugging Face.")

# -----------------------------
# LOAD MODELS (once)
# -----------------------------
@st.cache_resource
def load_models():
    with st.spinner("Loading models (only once)..."):
        sentiment_model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
        emotion_model = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion")
    return sentiment_model, emotion_model

sentiment_analyzer, emotion_analyzer = load_models()

# -----------------------------
# INITIAL STATE
# -----------------------------
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []
if "user_name" not in st.session_state:
    st.session_state.user_name = "User"

# -----------------------------
# EMOJI + REPLY HELPERS
# -----------------------------
def emotion_to_emoji(e):
    mapping = {
        "joy": "😄", "sadness": "😢", "anger": "😤",
        "fear": "😟", "love": "💕", "surprise": "😲", "neutral": "🙂"
    }
    return mapping.get(e.lower(), "🙂")

def generate_bot_reply(sentiment_label, emotion_label):
    sentiment_label = sentiment_label.upper()
    emo = emotion_label.lower()

    replies = {
        "POSITIVE": [
            "That’s great to hear! 😊 What made you feel that way?",
            "I love that energy! Tell me more!",
            "Keep that positivity flowing! 🌟"
        ],
        "NEGATIVE": [
            "I'm really sorry you're feeling this way. Want to talk about it?",
            "That sounds tough — but remember, emotions are temporary 💫",
            "I hear you. You're not alone ❤️"
        ],
        "NEUTRAL": [
            "Got it. Tell me more about that!",
            "I see. How do you feel about it?",
            "Interesting — would you like to elaborate?"
        ]
    }

    emotion_context = {
        "joy": "You sound genuinely happy — that's wonderful! 😄",
        "sadness": "I sense sadness. It’s okay to feel that way. Want me to share a comforting quote?",
        "anger": "Tell me more",
        "fear": "You sound worried — take it one step at a time.",
        "love": "That’s so heartwarming 💕",
        "surprise": "Wow, that must’ve been unexpected! 😲"
    }

    base = random.choice(replies.get(sentiment_label, replies["NEUTRAL"]))
    extra = emotion_context.get(emo, "")
    return f"{base} {extra}"

def make_wordcloud(texts):
    if not texts:
        return None
    wc = WordCloud(width=700, height=300, background_color="white").generate(" ".join(texts))
    fig, ax = plt.subplots(figsize=(8, 3.5))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    buf = BytesIO()
    plt.tight_layout()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return buf

def create_pdf_report(df, dominant, quote):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "AI Emotion Companion — Mood Summary", ln=True, align="C")
    pdf.ln(6)
    pdf.cell(0, 8, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.ln(6)
    pdf.cell(0, 8, f"Dominant mood: {dominant}", ln=True)
    pdf.ln(8)
    pdf.multi_cell(0, 8, f"Motivational quote / advice: {quote}")
    pdf.ln(8)
    pdf.cell(0, 8, "Recent messages (last 10):", ln=True)
    pdf.ln(4)
    for _, row in df.tail(10).iterrows():
        pdf.multi_cell(0, 7, f"{row['time']} | {row['user']}: {row['message']}")
    out = pdf.output(dest='S').encode('latin-1')
    return out

# -----------------------------
# SIDEBAR SETTINGS
# -----------------------------
with st.sidebar:
    st.header("👤 Settings")
    st.session_state.user_name = st.text_input("Your name:", value=st.session_state.user_name)
    if st.button("🧹 Clear Chat History"):
        st.session_state.chat_log = []
        st.success("Chat cleared!")

# -----------------------------
# MAIN CHAT AREA
# -----------------------------
st.markdown("## 💬 Talk to your AI Companion")

user_message = st.text_input("Type your message here and press Enter:")
if user_message:
    sent_result = sentiment_analyzer(user_message)[0]
    emo_result = emotion_analyzer(user_message)[0]

    sentiment = sent_result["label"]
    confidence = round(sent_result["score"] * 100, 2)
    emotion = emo_result["label"]

    bot_reply = generate_bot_reply(sentiment, emotion)

    entry = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "user": st.session_state.user_name,
        "message": user_message,
        "sentiment": sentiment,
        "confidence": confidence,
        "emotion": emotion,
        "bot_reply": bot_reply
    }
    st.session_state.chat_log.append(entry)

# -----------------------------
# DISPLAY CHAT (Black Text Styling)
# -----------------------------
if st.session_state.chat_log:
    for chat in reversed(st.session_state.chat_log):
        st.markdown(f"""
        <div style="margin-bottom:15px;">
            <div style="
                background-color:#EDEDED;
                color:black;
                padding:12px;
                border-radius:12px;
                margin-bottom:6px;
                box-shadow:0px 1px 2px rgba(0,0,0,0.1);
            ">
                <b>{chat['user']}</b> <small>({chat['time']})</small>: {chat['message']}<br>
                <small><i>Sentiment:</i> {chat['sentiment']} ({chat['confidence']}%) | 
                <i>Emotion:</i> {chat['emotion']} {emotion_to_emoji(chat['emotion'])}</small>
            </div>
            <div style="
                background-color:#F5F5F5;
                color:black;
                padding:12px;
                border-radius:12px;
                box-shadow:0px 1px 2px rgba(0,0,0,0.1);
            ">
                <b>🤖 AI:</b> {chat['bot_reply']}
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("Say hi to start the conversation!")

# -----------------------------
# ANALYTICS SECTION
# -----------------------------
st.markdown("---")
st.markdown("## 📊 Emotion Analytics")

if st.session_state.chat_log:
    df = pd.DataFrame(st.session_state.chat_log)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Sentiment Distribution")
        fig_pie = px.pie(df, names="sentiment", title="Sentiment Breakdown", hole=0.3)
        st.plotly_chart(fig_pie, use_container_width=True)

        st.subheader("Emotion Frequency")
        emotion_counts = df['emotion'].value_counts().reset_index()
        emotion_counts.columns = ['emotion', 'count']
        fig_bar = px.bar(emotion_counts, x='emotion', y='count', title='Emotion Frequency', text='count')
        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.subheader("Confidence Trend")
        df['time'] = pd.to_datetime(df['time'], format="%H:%M:%S", errors='coerce')
        fig_line = px.line(
        df, 
        x='time', 
        y='confidence', 
        color='sentiment', 
        markers=True, 
        title='Confidence over Time'
        )

        st.plotly_chart(fig_line, use_container_width=True)

        st.subheader("Word Cloud")
        wc_buf = make_wordcloud(df['message'].tolist())
        if wc_buf:
            st.image(wc_buf)

    st.subheader("Mood Summary")
    dominant = df['emotion'].mode()[0]
    quotes = {
        "joy": "“Happiness is not something ready made. It comes from your actions.” — Dalai Lama",
        "sadness": "“Stars can’t shine without darkness.” — D.H. Sidebottom",
        "anger": "“For every minute you remain angry, you give up sixty seconds of peace.” — Emerson",
        "fear": "“Do one thing every day that scares you.” — Roosevelt",
        "love": "“Love is composed of a single soul inhabiting two bodies.” — Aristotle",
        "surprise": "“The most beautiful thing is unexpected happiness.” — Unknown"
    }
    quote = quotes.get(dominant, "Keep going — small steps count. You're doing great! 💫")
    st.info(f"Dominant Emotion: **{dominant}** {emotion_to_emoji(dominant)}\n\n{quote}")

    csv_bytes = df.to_csv(index=False).encode('utf-8')
    st.download_button("📁 Download CSV", data=csv_bytes, file_name="chat_log.csv", mime="text/csv")

    if st.button("📄 Download PDF Report"):
        pdf_bytes = create_pdf_report(df, dominant, quote)
        b64 = base64.b64encode(pdf_bytes).decode()
        href = f"<a href='data:application/octet-stream;base64,{b64}' download='mood_summary.pdf'>Click here to download PDF</a>"
        st.markdown(href, unsafe_allow_html=True)
else:
    st.info("Start chatting to unlock analytics and reports!")

st.markdown("---")
st.caption("💡 Built with Streamlit and Hugging Face | Data stays in your session only.")


# 💬 AI Sentiment Analyzer & Emotion Chat Dashboard

A full-fledged **emotion-aware conversational AI dashboard** using Hugging Face Transformers and Streamlit.  
Chat with an AI, analyze your messages in real-time, and visualize mood trends.

## 🌐 Live Demo
You can try the app live on Hugging Face Spaces:  
[https://huggingface.co/spaces/Khushi545/Emotion-Companion](https://huggingface.co/spaces/Khushi545/Emotion-Companion)

## 🚀 Features
- Conversational AI chat with **sentiment** and **emotion detection**  
- Dynamic bot replies based on your emotional tone  
- Real-time **chat history** tracking  
- **Sentiment & confidence charts** over time  
- **Word cloud** of chat messages  
- **Mood summary** with motivational quotes  
- **Downloadable CSV and PDF reports**  
- Hosted on **Hugging Face Spaces** (free)

## 🧠 Models Used
- **Sentiment Analysis:** `distilbert-base-uncased-finetuned-sst-2-english`  
- **Emotion Classification:** `bhadresh-savani/distilbert-base-uncased-emotion`

## ⚙️ Run Locally
Clone the repo and install dependencies:

```bash
git clone <repo-link>
cd <repo-folder>
pip install -r requirements.txt
streamlit run app.py
````

> The app will open in your default browser at `http://localhost:8501`.

## 📂 Files in the Repo

* `app.py` — Main Streamlit application
* `requirements.txt` — Python dependencies
* `README.md` — Project documentation
* `Dockerfile` — For containerized deployment (optional)

## 💡 Notes

* The Hugging Face Space may **sleep after inactivity**, but it will restart when accessed.
* All data stays in your session; no user data is stored externally.

---


I can also make a **super compact version** suitable for Hugging Face Spaces that looks clean on their UI. Do you want me to do that?
```

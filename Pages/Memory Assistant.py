import os
import streamlit as st
import google.generativeai as genai
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import pytz
import base64

# Secure API Key Handling
genai.configure(api_key=st.secrets["genai"]["api_key"])

# Database Setup
def init_db():
    with sqlite3.connect("progress.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS progress (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            date TEXT NOT NULL,
                            success_rate INTEGER NOT NULL,
                            failure_rate INTEGER NOT NULL,
                            tasks_completed INTEGER NOT NULL
                         )''')
        conn.commit()

# Add Progress to Database
def add_progress(success, failure, tasks):
    date = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect("progress.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO progress (date, success_rate, failure_rate, tasks_completed) VALUES (?, ?, ?, ?)", 
                       (date, success, failure, tasks))
        conn.commit()

# Fetch Progress Data
def get_progress():
    with sqlite3.connect("progress.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM progress")
        return cursor.fetchall()
    
def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()
    
def set_bg(image_path):
    img_base64 = get_base64(image_path)
    bg_css = f"""
    <style>
        .stApp {{
            background-image: url("data:image/png;base64,{img_base64}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
    </style>
    """
    st.markdown(bg_css, unsafe_allow_html=True)

set_bg("bg.jpg")

# AI Model Configuration
generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    safety_settings=safety_settings,
    generation_config=generation_config,
    system_instruction="You are helping an Alzheimer's patient with memory exercises."
)

# Initialize Database
init_db()

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []
if "last_input" not in st.session_state:
    st.session_state.last_input = ""
if "success_count" not in st.session_state:
    st.session_state.success_count = 0
if "failure_count" not in st.session_state:
    st.session_state.failure_count = 0
if "task_count" not in st.session_state:
    st.session_state.task_count = 0

# 🌟 Streamlit UI
st.title("🧠 Alzheimer's Memory Assistant")
st.write("Chat with AI to improve memory through exercises!")

# Display Chat History
for message in st.session_state.history:
    role = "👤 You" if message["role"] == "user" else "🤖 Bot"
    st.markdown(f"**{role}:** {message['parts'][0]}")

# User input
user_input = st.text_input("Type your message and press Enter:", key="user_input")

if user_input and user_input != st.session_state.last_input:
    st.session_state.last_input = user_input  

    # Start chat session
    chat_session = model.start_chat(history=st.session_state.history)
    response = chat_session.send_message(user_input)
    model_response = response.text

    # Simple evaluation logic (this can be improved)
    if "correct" in model_response.lower() or "good job" in model_response.lower():
        st.session_state.success_count += 1
    else:
        st.session_state.failure_count += 1
    st.session_state.task_count += 1

    # Store progress
    add_progress(st.session_state.success_count, st.session_state.failure_count, st.session_state.task_count)

    # Update chat history
    st.session_state.history.append({"role": "user", "parts": [user_input]})
    st.session_state.history.append({"role": "model", "parts": [model_response]})

    # Refresh page
    st.rerun()

# 📊 Progress Tracking Section
st.title("📊 Progress Report")
st.write("Track improvements in memory exercises and task completion.")

# Fetch and display progress data
data = get_progress()
if data:
    df = pd.DataFrame(data, columns=["ID", "Date", "Success Rate", "Failure Rate", "Tasks Completed"])
    df.drop(columns=["ID"], inplace=True)
    df["Date"] = pd.to_datetime(df["Date"])  # Convert date for plotting
    st.write(df)

    # 📈 Plot Progress
    fig, ax = plt.subplots()
    ax.plot(df["Date"], df["Success Rate"], label="✅ Success Rate", marker='o', linestyle='-', color='green')
    ax.plot(df["Date"], df["Failure Rate"], label="❌ Failure Rate", marker='o', linestyle='-', color='red')
    ax.set_xlabel("Date")
    ax.set_ylabel("Attempts")
    ax.set_title("Memory Exercise Performance")
    ax.legend()
    st.pyplot(fig)
else:
    st.write("No progress recorded yet. Start answering to track progress!")

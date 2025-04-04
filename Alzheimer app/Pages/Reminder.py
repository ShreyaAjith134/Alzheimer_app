import streamlit as st
import time
import threading
from gtts import gTTS
import os
import sqlite3

# Database Setup
conn = sqlite3.connect("tasks.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS reminders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT NOT NULL,
                    time TEXT NOT NULL,
                    repeat TEXT NOT NULL,
                    days TEXT NOT NULL
                 )''')
conn.commit()

# Function to Add Task to Database
def add_task(task, time, repeat, days):
    days_str = ",".join(days)  
    cursor.execute("INSERT INTO reminders (task, time, repeat, days) VALUES (?, ?, ?, ?)", 
                   (task, time, repeat, days_str))
    conn.commit()

# Function to Get Tasks from Database
def get_tasks():
    cursor.execute("SELECT * FROM reminders")
    return cursor.fetchall()

# Function to Delete Completed Tasks
def complete_task(task_id):
    cursor.execute("DELETE FROM reminders WHERE id = ?", (task_id,))
    conn.commit()

# Function to play voice notification
def speak(text):
    tts = gTTS(text=text, lang='en')
    filename = "reminder.mp3"
    tts.save(filename)
    os.system(f"start {filename}")  # Windows, use 'afplay' for Mac, 'mpg321' for Linux

# Function to Check and Announce Tasks
def check_tasks():
    while True:
        current_time = time.strftime("%I:%M %p")  
        tasks = get_tasks()  
        for task in tasks:
            task_id, task_name, task_time, repeat, days = task
            today = time.strftime("%A")
            days_list = days.split(",")  

            if task_time == current_time and today in days_list:
                speak(f"Time for {task_name}")
                
                if repeat == "None":
                    complete_task(task_id)  

        time.sleep(30)  

threading.Thread(target=check_tasks, daemon=True).start()

# Streamlit UI
st.title("🧠 Alzheimer's Task Scheduler")

# Task Entry
task = st.text_input("Enter Task:")

# Time Selection
col1, col2, col3 = st.columns(3)
with col1:
    selected_hour = st.selectbox("Hour", [f"{hour:02}" for hour in range(1, 13)])
with col2:
    selected_minute = st.selectbox("Min", [f"{minute:02}" for minute in range(0, 60)])
with col3:
    selected_am_pm = st.selectbox("AM/PM", ["AM", "PM"])

# Recurrence Selection
repeat = st.selectbox("Repeat", ["None", "Daily", "Weekly"])

# Days Selection
selected_days = st.multiselect("Select Days (for Weekly Recurrence)", 
                               ["Monday", "Tuesday", "Wednesday", "Thursday", 
                                "Friday", "Saturday", "Sunday"], 
                               default=[time.strftime("%A")])

# Combine Time
time_selected = f"{selected_hour}:{selected_minute} {selected_am_pm}"

# Add Task Button
if st.button("Add Task"):
    if task and time_selected:
        add_task(task, time_selected, repeat, selected_days)
        st.success(f"Task '{task}' set for {time_selected} ({repeat}) on {', '.join(selected_days) if repeat == 'Weekly' else 'Everyday'}")

# Display Scheduled Tasks
st.subheader("📋 Scheduled Tasks")
tasks = get_tasks()
if tasks:
    for task in tasks:
        task_id, task_name, task_time, task_repeat, task_days = task
        st.write(f"⏰ {task_time} - {task_name} ({task_repeat}) on {task_days}")
else:
    st.write("No tasks scheduled.")

# Task Tracker for Completed Tasks
st.subheader("✅ Task Tracker")
for task in tasks:
    task_id, task_name, _, _, _ = task
    if st.checkbox(f"Mark '{task_name}' as completed", key=f"task_{task_id}"):
        complete_task(task_id)
        st.success(f"Task '{task_name}' marked as completed!")
        st.rerun()  # Refresh the app after task completion

# Close database connection at the end
conn.close()

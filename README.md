---

## 🧠 Alzheimer’s Support Web App

This project is a **multi-page Streamlit app** to support Alzheimer’s patients and caregivers with **memory exercises**, **progress tracking**, and a **task scheduler with voice reminders** — all in one place.

---

## 📂 Project Structure

```
ALZHEIMER_APP/
│
├── .streamlit/
│   └── secrets.toml      # Your Gemini API key
│
├── Pages/
│   ├── bg.jpg            # Background image for Pages
│   ├── Memory Assistant.py   # AI memory exercises
│   ├── Reminder.py       # Task scheduler with TTS
│   ├── progress.db       # DB for memory tracking
│   └── tasks.db          # DB for reminders
│
├── bg.jpg                # Main background image (optional)
├── Home.py               # Landing page
├── progress.db           # Root-level DB (optional)
├── tasks.db              # Root-level DB (optional)
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## 🚀 How It Works

### 🏠 **Home Page (`Home.py`)**

* Overview of the app
* Navigation instructions to use Memory Assistant & Task Scheduler

### 🧩 **Memory Assistant (`Memory Assistant.py`)**

* Chat with Gemini AI to do memory exercises
* Stores your success/failure rates in `progress.db`
* Visual progress report using Matplotlib

### ⏰ **Task Scheduler (`Reminder.py`)**

* Add daily or weekly tasks
* Voice reminders play at scheduled time with `gTTS`
* Tasks saved in `tasks.db` and can be marked as completed

### 🎨 **Custom Background**

* Uses `bg.jpg` for a calming visual background

---

## ⚙️ Tech Stack

* **Python**
* **Streamlit**
* **Google Generative AI (Gemini)** (API key stored in `.streamlit/secrets.toml`)
* **SQLite3** for local data storage
* **Matplotlib**, **Pandas**
* **gTTS** for voice reminders
* **Threading** for real-time task checking

---

## ✅ How to Run the App

1. **Clone the repo**

   ```bash
   git clone https://github.com/yourusername/ALZHEIMER_APP.git
   cd ALZHEIMER_APP
   ```

2. **Create virtual environment (recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Add your API key to `.streamlit/secrets.toml`**

   ```toml
   [genai]
   api_key = "YOUR_GEMINI_API_KEY"
   ```

5. **Run the app**

   ```bash
   streamlit run Home.py
   ```

   Use the sidebar navigation to switch between **Memory Assistant** and **Task Scheduler** pages.

---

## 📌 Tips for Voice Alerts

* Uses `os.system("start reminder.mp3")` for **Windows**.
  If you’re on Mac, replace with `afplay`, or use `mpg321` on Linux.

* Keep your system volume on!

---

Home Page:  
![Memory Assistant](./Pages/screenshot1.png)

Memory Assistant Page:  
![Memory Assistant](./Pages/screenshot2.png)

Reminder Page:  
![Task Scheduler](./Pages/screenshot3.png)

---

## 📄 License

Open source under the [MIT License](LICENSE).

---


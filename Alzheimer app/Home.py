import streamlit as st
import base64

# Page title
st.title("🧠 Alzheimer's Awareness & Support")

def get_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

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

# Introduction
st.write(
    "Alzheimer's disease is a progressive neurological disorder that affects memory, thinking, and behavior. "
    "Our AI-powered memory assistant helps patients engage in exercises that can improve cognitive function."
)


# About Alzheimer's
st.header("📌 What is Alzheimer's Disease?")
st.write(
    "Alzheimer's disease is the most common cause of dementia, affecting millions worldwide. "
    "It leads to a gradual decline in cognitive abilities, making daily tasks difficult."
)

# Symptoms
st.header("⚠️ Early Signs & Symptoms")
st.markdown(
    """
    - **Memory loss** affecting daily life.
    - **Difficulty in problem-solving** or planning.
    - **Confusion with time or place**.
    - **Trouble understanding visual images**.
    - **Difficulty in speaking or writing**.
    - **Misplacing things** and losing the ability to retrace steps.
    - **Changes in mood & personality**.
    """
)

# Prevention & Care
st.header("💡 Prevention & Support")
st.write(
    "While there is no cure, certain lifestyle changes can reduce the risk of Alzheimer's:"
)
st.markdown(
    """
    - 🏃 **Stay physically active** – Regular exercise helps maintain brain health.
    - 🥦 **Eat a brain-healthy diet** – Include fruits, vegetables, and omega-3 fatty acids.
    - 🧩 **Engage in mental exercises** – Reading, puzzles, and social interactions help.
    - 😃 **Manage stress & get enough sleep** – Helps in reducing cognitive decline.
    """
)
# Footer
st.write("---")
st.write("🔗 Learn more at [Alzheimer's Association](https://www.alz.org/)")


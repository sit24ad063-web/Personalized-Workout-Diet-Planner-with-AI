import os
import base64
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# -------------------- CONFIG --------------------
st.set_page_config(layout="wide")
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)

# -------------------- IMAGE LOADER --------------------
def load_local_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

hero_image_base64 = load_local_image("pic.jpg")

# -------------------- SESSION --------------------
if "plan" not in st.session_state:
    st.session_state.plan = None

# -------------------- GLOBAL STYLE --------------------
st.markdown(f"""
<style>
.block-container {{padding:0rem;}}
body {{background-color:#0f0f0f; font-family:'Segoe UI', sans-serif; color:white;}}

.hero {{
    position: relative;
    height: 100vh;
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding: 0 8%;
    background: radial-gradient(circle at 20% 50%, #1f1f1f 0%, #0f0f0f 60%);
    overflow:hidden;
}}

.bubble {{
    position:absolute;
    border-radius:50%;
    background:rgba(255,255,255,0.05);
    animation: float 12s infinite ease-in-out;
}}
@keyframes float {{
    0% {{transform: translateY(0px);}}
    50% {{transform: translateY(-50px);}}
    100% {{transform: translateY(0px);}}
}}

.hero-text h1 {{
    font-size:80px;
    font-weight:900;
    line-height:1.1;
}}
.hero-text p {{
    font-size:20px;
    color:#bbbbbb;
    max-width:500px;
}}

.hero-img img {{
    max-height:90vh;
    filter: drop-shadow(0px 0px 50px rgba(255,0,0,0.4));
}}

.glass {{
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(15px);
    border-radius: 20px;
    padding: 40px;
    box-shadow: 0 0 40px rgba(255,0,0,0.15);
    margin: 80px 8%;
}}

.plan-box {{
    background:#1a1a1a;
    padding:30px;
    border-radius:20px;
    border:1px solid rgba(255,0,0,0.3);
    box-shadow: 0 0 40px rgba(255,0,0,0.2);
}}

.stButton>button {{
    background: linear-gradient(90deg,#ff3c3c,#ff0000);
    color:white;
    border:none;
    border-radius:50px;
    padding:10px 30px;
    font-weight:bold;
}}
</style>

<div class="hero">
<div class="bubble" style="width:200px;height:200px;top:20%;left:10%;"></div>
<div class="bubble" style="width:150px;height:150px;top:60%;left:30%;animation-duration:15s;"></div>
<div class="bubble" style="width:250px;height:250px;top:40%;left:70%;animation-duration:18s;"></div>

<div class="hero-text">
    <h1>YOU.<br>ARE.<br>ENGINEERED.</h1>
    <p>AI-crafted workouts and culturally aware meal plans designed for serious students.</p>
</div>

<div class="hero-img">
    <img src="data:image/jpg;base64,{hero_image_base64}">
</div>
</div>
""", unsafe_allow_html=True)

# -------------------- AI FUNCTION --------------------
def generate_workout_plan(age, weight, height, goal, diet, budget, location):

    prompt = f"""
Create a structured and clean weekly workout and nutrition plan.

User:
- Age: {age}
- Weight: {weight}kg
- Height: {height}cm
- Goal: {goal}
- Diet: {diet}
- Budget: {budget}
- Training Location: {location}

STRICT RULES:
- Use markdown headings (##, ###)
- Use bullet points
- No long paragraphs
- Separate workout and nutrition clearly
"""

    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {"role": "system", "content": "You are an elite fitness coach and formatting specialist."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.6,
        max_tokens=900
    )

    return response.choices[0].message.content

# -------------------- CALORIE SECTION --------------------
st.markdown('<div class="glass">', unsafe_allow_html=True)
st.markdown("## 🔥 Interactive Calorie Estimator")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", 15, 60, 21)
    weight = st.number_input("Weight (kg)", 40, 150, 70)
    height = st.number_input("Height (cm)", 140, 210, 175)
    goal = st.selectbox("Your Goal", ["Weight Loss", "Muscle Gain", "Shredded Aesthetic"])

with col2:
    diet = st.selectbox("Diet Type", ["Vegetarian", "Non-Vegetarian", "Vegan"])
    budget = st.selectbox("Food Budget", ["Low", "Medium", "High"])
    location = st.selectbox("Train Where?", ["Home", "Gym"])

bmr = 10 * weight + 6.25 * height - 5 * age + 5
calories = round(bmr * 1.4)

st.markdown("---")

row_left, row_mid, row_right = st.columns([6,1,2])

with row_left:
    st.markdown(
        f"""
        <div style="display:flex; align-items:center; gap:15px;">
            <h3 style="margin:0;">🔥 Estimated Maintenance Calories:</h3>
            <h3 style="margin:0; color:#ff3c3c;">{calories} kcal/day</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

with row_right:
    generate_clicked = st.button("🚀 Generate Plan")

if generate_clicked:
    with st.spinner("Engineering your elite transformation..."):
        st.session_state.plan = generate_workout_plan(
            age, weight, height, goal, diet, budget, location
        )

if st.session_state.plan:
    st.markdown("<br><br>", unsafe_allow_html=True)
    left, center, right = st.columns([1,4,1])
    with center:
        st.markdown("<div class='plan-box'>", unsafe_allow_html=True)
        st.markdown("## 🤖 Your Personalized Plan")
        st.markdown(st.session_state.plan)
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
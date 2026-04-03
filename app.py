import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

# 1. Setup Streamlit page config (Set layout to 'wide' for a better look)
st.set_page_config(page_title="NutriVision AI", page_icon="🥗", layout="wide")

# 2. Custom CSS for a sleek UI
st.markdown("""
<style>
    /* Center the main title */
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        background: -webkit-linear-gradient(#FF4B4B, #FF904B);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .sub-title {
        text-align: center;
        color: #888;
        font-size: 1.2rem;
        margin-bottom: 30px;
    }
    /* Style the analyze button */
    .stButton>button {
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 24px;
        width: 100%;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #FF6B6B;
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# 3. Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# 4. Gemini response function
def get_gemini_response(prompt, img):
    model = genai.GenerativeModel('gemini-2.5-flash') # Updated to current model
    if img:
        response = model.generate_content([prompt, img])
    else:
        response = model.generate_content(prompt)
    return response.text

# ---------------- UI ---------------- #

# Header
st.markdown("<h1 class='main-title'>🥗 NutriVision AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Snap a pic. Know your macros. Hit your goals.</p>", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/8145/8145413.png", width=100) # Optional cute icon
    st.header("⚙️ Your Settings")
    goal = st.selectbox(
        "🎯 Select your fitness goal:",
        ["Maintain Weight", "Weight Loss", "Weight Gain", "Muscle Building"]
    )
    st.markdown("---")
    st.info("💡 **Tip:** Upload clear, well-lit photos of your food for the most accurate calorie estimation.")

# --- Main Content Area ---
# Prompt definition with improved formatting instructions
input_prompt = f"""
You are an expert nutritionist. Analyze the food image and provide the response in this exact format:

### 🍽️ Food Identification
* **Items Found:** (Name the food items)
* **Total Estimated Calories:** (Number) kcal
* **Health Rating:** (Healthy / Moderate / Unhealthy)

### 📊 Macro Breakdown
Create a simple markdown table with columns: 'Nutrient' and 'Estimated Amount (g)'. Include Protein, Carbs, and Fats.

### 💡 Nutritionist Advice
Provide 2-3 short, actionable suggestions based on the user's goal: **{goal}**.
"""

# Image upload
uploaded_file = st.file_uploader("📸 Upload your meal (JPG, PNG)", type=["jpg", "jpeg", "png"])

# Create two columns for a side-by-side layout
col1, col2 = st.columns([1, 1.2])

image = None

with col1:
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        # Display image nicely in the first column
        st.image(image, caption="Your Meal", use_container_width=True)
    else:
        st.info("Upload an image to see the preview here.")

with col2:
    # Button to trigger analysis (placed in the second column)
    if st.button(" Analyze Meal"):
        if uploaded_file is None:
            st.warning("⚠️ Please upload an image first!")
        else:
            with st.status("👨‍⚕️ AI Nutritionist is analyzing your food...", expanded=True) as status:
                st.write("Detecting ingredients...")
                st.write("Calculating macros...")
                try:
                    # Get response from Gemini
                    response = get_gemini_response(input_prompt, image)
                    status.update(label="Analysis Complete! ✅", state="complete", expanded=False)
                    
                    # Display the beautiful markdown result
                    st.success("Here is your breakdown:")
                    st.markdown(response)
                    
                except Exception as e:
                    status.update(label="Error occurred", state="error")
                    st.error(f"An error occurred: {e}")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: grey;'> Built By Shukla Pranjal </p>", unsafe_allow_html=True)

import streamlit as st
import joblib
import numpy as np
import datetime

# 1. Model aur Features Load karna
model = joblib.load('model.pkl')

# Page Configuration
st.set_page_config(page_title="India AQI Predictor", page_icon="🌬️")

# Custom CSS for better UI
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    .prediction-box { padding: 20px; border-radius: 10px; text-align: center; color: white; font-size: 24px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌬️ Air Quality Index Predictor")
st.write("Based on the **India Air Quality Dataset**, this tool predicts AQI using the **Random Forest** model.")

# 2. User Input Section (Limited to top 4 as requested)
st.subheader("📊 Enter Pollutant Concentrations (µg/m³)")
col1, col2 = st.columns(2)

with col1:
    pm25 = st.number_input("PM2.5 (Fine Particles)", min_value=0.0, value=45.0, help="Main culprit for respiratory issues")
    no2 = st.number_input("NO2 (Nitrogen Dioxide)", min_value=0.0, value=25.0)

with col2:
    pm10 = st.number_input("PM10 (Coarse Particles)", min_value=0.0, value=90.0)
    co = st.number_input("CO (Carbon Monoxide)", min_value=0.0, value=0.8)




# 3. Prediction Logic
if st.button("Predict Air Quality"):
    # Model 10 features expect kar raha hai (Pehle wala training logic)
    # Order: PM2.5, PM10, NO, NO2, CO, SO2, O3, Benzene, Toluene, Xylene
    
    input_data = [
        pm25,    # PM2.5
        pm10,    # PM10
        0.0,     # NO (Placeholder)
        no2,     # NO2
        0.0,     # CO (Placeholder - Agar slider nahi hai toh 0.0)
        0.0,     # SO2 (Placeholder)
        0.0,     # O3 (Placeholder)
        0.0,     # Benzene (Placeholder)
        0.0,     # Toluene (Placeholder)
        0.0      # Xylene (Placeholder)
    ]
    
    # Input ko model ke format mein convert karein (1, 10)
    features = np.array([input_data])
    
    # Prediction run karein
    prediction = model.predict(features)[0]
    aqi = round(prediction, 2)

    # 4. Color-Coded Results & Health Advice [Source 10, 165]
    st.divider()
    if aqi <= 50:
        bg_color, category, advice = "#28a745", "Good ✅", "Air quality is satisfactory. Enjoy outdoor activities!"
    elif aqi <= 100:
        bg_color, category, advice = "#ffc107", "Satisfactory 😊", "Minor discomfort for sensitive people."
    elif aqi <= 200:
        bg_color, category, advice = "#fd7e14", "Moderate ⚠️", "Breathing discomfort to people with lungs/heart disease."
    elif aqi <= 300:
        bg_color, category, advice = "#dc3545", "Poor 😷", "Avoid prolonged outdoor exertion."
    else:
        bg_color, category, advice = "#343a40", "Severe 🚨", "HEALTH WARNING: Everyone should stay indoors!"

    # Display Result
    st.markdown(f"""
        <div class="prediction-box" style="background-color: {bg_color};">
            Predicted AQI: {aqi} <br>
            Category: {category}
        </div>
        """, unsafe_allow_html=True)
    
    st.info(f"**Health Recommendation:** {advice}")

st.sidebar.markdown("### Model Info")
st.sidebar.write("**Algorithm:** Random Forest Regressor")
st.sidebar.write("**Accuracy (R²):** 90.92%")
st.sidebar.write("**Dataset:** CPCB India (2015-2020)")

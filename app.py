import streamlit as st
import joblib
import numpy as np
import pandas as pd

@st.cache_resource
def load_model():
    model    = joblib.load('model.pkl')
    features = joblib.load('feature_names.pkl')
    return model, features

model, feature_names = load_model()

st.set_page_config(page_title='AQI Predictor', page_icon='🌫️', layout='centered')

st.markdown("""
<style>
.stApp { background-color: #0d1117; color: #e6edf3; }
.stNumberInput label { color: #7d8590 !important; font-size: 12px !important; }
.stNumberInput input { background: #0d1117 !important; color: #e6edf3 !important; border: 0.5px solid #30363d !important; border-radius: 8px !important; }
.stButton button { background: #238636 !important; color: #fff !important; border: none !important; border-radius: 10px !important; font-size: 15px !important; font-weight: 500 !important; width: 100% !important; padding: 12px !important; }
.stButton button:hover { background: #2ea043 !important; }
div[data-testid="metric-container"] { background: #161b22; border: 0.5px solid #30363d; border-radius: 10px; padding: 14px; text-align: center; }
div[data-testid="metric-container"] label { color: #7d8590 !important; font-size: 11px !important; }
div[data-testid="metric-container"] div { color: #e6edf3 !important; font-size: 26px !important; font-weight: 500 !important; }
.stMarkdown h1 { color: #e6edf3 !important; }
.stMarkdown p { color: #7d8590 !important; }
div[data-testid="stHorizontalBlock"] { gap: 8px; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;font-size:24px;color:#e6edf3;margin-bottom:4px'>🌫️ AQI Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#7d8590;font-size:13px;margin-bottom:24px'>India Air Quality Data trained ML Model</p>", unsafe_allow_html=True)

st.markdown("<p style='color:#7d8590;font-size:11px;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px'>Enter Pollutant Values</p>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    pm25    = st.number_input('PM2.5 (µg/m³)',  min_value=0.0, value=50.0,  step=0.1)
    pm10    = st.number_input('PM10 (µg/m³)',   min_value=0.0, value=100.0, step=0.1)
    no      = st.number_input('NO (µg/m³)',     min_value=0.0, value=10.0,  step=0.1)
    no2     = st.number_input('NO2 (µg/m³)',    min_value=0.0, value=40.0,  step=0.1)
with col2:
    nox     = st.number_input('NOx (µg/m³)',    min_value=0.0, value=50.0,  step=0.1)
    nh3     = st.number_input('NH3 (µg/m³)',    min_value=0.0, value=15.0,  step=0.1)
    co      = st.number_input('CO (mg/m³)',     min_value=0.0, value=1.0,   step=0.01)
    so2     = st.number_input('SO2 (µg/m³)',    min_value=0.0, value=20.0,  step=0.1)
with col3:
    o3      = st.number_input('O3 (µg/m³)',     min_value=0.0, value=30.0,  step=0.1)
    benzene = st.number_input('Benzene (µg/m³)',min_value=0.0, value=1.5,   step=0.01)
    toluene = st.number_input('Toluene (µg/m³)',min_value=0.0, value=5.0,   step=0.1)
    xylene  = st.number_input('Xylene (µg/m³)', min_value=0.0, value=2.0,   step=0.1)

st.markdown("<br>", unsafe_allow_html=True)

if st.button('🔍 Predict AQI'):

    input_dict = {col: 0.0 for col in feature_names}
    user_map = {
        'pm2.5': pm25, 'pm10': pm10, 'no': no, 'no2': no2,
        'nox': nox, 'nh3': nh3, 'co': co, 'so2': so2,
        'o3': o3, 'benzene': benzene, 'toluene': toluene, 'xylene': xylene
    }
    for feat in feature_names:
        feat_lower = feat.lower().replace('.', '').replace(' ', '')
        for key, val in user_map.items():
            key_clean = key.replace('.', '').replace(' ', '')
            if key_clean in feat_lower:
                input_dict[feat] = val
                break

    input_df = pd.DataFrame([input_dict])
    prediction = round(float(model.predict(input_df)[0]), 1)

    if prediction <= 50:
        category, emoji, color, msg = 'Good',         '🟢', '#238636', 'Air quality is excellent. Safe for everyone.'
    elif prediction <= 100:
        category, emoji, color, msg = 'Satisfactory', '🟡', '#d29922', 'Air quality is acceptable.'
    elif prediction <= 200:
        category, emoji, color, msg = 'Moderate',     '🟠', '#e3791a', 'Sensitive groups should take precautions.'
    elif prediction <= 300:
        category, emoji, color, msg = 'Poor',         '🔴', '#da3633', 'Avoid outdoor activities!'
    elif prediction <= 400:
        category, emoji, color, msg = 'Very Poor',    '🟣', '#8957e5', 'Stay indoors. Very unhealthy air.'
    else:
        category, emoji, color, msg = 'Severe',       '⚫', '#484f58', 'Emergency conditions. Seek medical advice!'

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#7d8590;font-size:11px;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px'>Result</p>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.metric('Predicted AQI', prediction)
    with c2:
        st.metric('Category', f'{emoji} {category}')

    st.markdown(f"""
    <div style='background:#161b22;border:0.5px solid {color}44;border-left:2px solid {color};border-radius:8px;padding:12px 14px;margin:12px 0;font-size:13px;color:{color}'>
        {msg}
    </div>""", unsafe_allow_html=True)

    # AQI Gauge
    gauge_pct = min(prediction / 500 * 100, 100)
    st.markdown(f"""
    <div style='margin:16px 0 8px'>
        <p style='color:#7d8590;font-size:11px;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px'>AQI Gauge</p>
        <div style='height:8px;border-radius:4px;background:linear-gradient(90deg,#238636 0%,#d29922 30%,#e3791a 55%,#da3633 70%,#8957e5 85%,#484f58 100%);position:relative'>
            <div style='position:absolute;top:-4px;left:{gauge_pct}%;width:16px;height:16px;background:#e6edf3;border-radius:50%;transform:translateX(-50%);border:2px solid #0d1117;box-shadow:0 0 0 2px {color}'></div>
        </div>
        <div style='display:flex;justify-content:space-between;font-size:9px;color:#484f58;margin-top:5px'>
            <span>0</span><span>100</span><span>200</span><span>300</span><span>400</span><span>500</span>
        </div>
    </div>""", unsafe_allow_html=True)

    # AQI Scale Table
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#7d8590;font-size:11px;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:8px'>AQI Reference Scale</p>", unsafe_allow_html=True)
    st.markdown("""
| AQI Range | Category | Health Impact |
|-----------|----------|---------------|
| 0 – 50 | 🟢 Good | Minimal impact |
| 51 – 100 | 🟡 Satisfactory | Minor breathing issues |
| 101 – 200 | 🟠 Moderate | Sensitive groups affected |
| 201 – 300 | 🔴 Poor | Breathing discomfort |
| 301 – 400 | 🟣 Very Poor | Serious health effects |
| 400+ | ⚫ Severe | Emergency conditions |
    """)

print('✅ app.py ready!')

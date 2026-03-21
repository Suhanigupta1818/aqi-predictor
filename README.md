# 🌫️ AQI Predictor

A Machine Learning web app that predicts Air Quality Index (AQI) based on pollutant values.

## Live Demo
🚀 [Click here to open the app](https://share.streamlit.io)

## About
This app uses a **Random Forest** model trained on India Air Quality Dataset from Kaggle.
It takes pollutant values as input and predicts the AQI along with health recommendations.

## Model Performance
- Algorithm: Random Forest Regressor
- R² Score: 0.91
- Dataset: India Air Quality Data (Kaggle)

## Input Features
| Pollutant | Unit |
|-----------|------|
| PM2.5 | µg/m³ |
| PM10 | µg/m³ |
| NO | µg/m³ |
| NO2 | µg/m³ |
| NOx | µg/m³ |
| NH3 | µg/m³ |
| CO | mg/m³ |
| SO2 | µg/m³ |
| O3 | µg/m³ |
| Benzene | µg/m³ |
| Toluene | µg/m³ |
| Xylene | µg/m³ |

## AQI Scale
| AQI Range | Category | Health Impact |
|-----------|----------|---------------|
| 0 - 50 | 🟢 Good | Minimal impact |
| 51 - 100 | 🟡 Satisfactory | Minor breathing issues |
| 101 - 200 | 🟠 Moderate | Sensitive groups affected |
| 201 - 300 | 🔴 Poor | Breathing discomfort |
| 301 - 400 | 🟣 Very Poor | Serious health effects |
| 400+ | ⚫ Severe | Emergency conditions |

## Tech Stack
- Python
- Scikit-learn
- Streamlit
- Pandas, NumPy
- XGBoost, LightGBM

## Installation
```bash

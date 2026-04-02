# 🫀 PulseIQ — Heart Disease Analytics & Risk Predictor

> An interactive health analytics dashboard built with Streamlit, featuring real-time EDA and an ML-powered cardiovascular risk prediction engine.

---

## 📌 Overview

**PulseIQ** is a two-page Streamlit application built on the UCI Heart Disease Dataset (Cleveland, n=297). It combines exploratory data analysis with a machine learning risk predictor to help visualize and understand cardiovascular disease patterns.

---

### 1. Analytics Dashboard (`app.py`)

- 5 KPI cards — Total Patients, Disease Cases, Avg Age, Avg Cholesterol, Avg Max HR
- Interactive filters — Gender multiselect + Age Range slider
- Distribution charts — Disease by Age Group, Gender Breakdown, Disease Split (donut)
- Risk Factor Analysis — Cholesterol vs Max HR scatter, Correlation Matrix
- Age & Blood Pressure distribution histograms

### 2. CardioSense — Risk Predictor (`pages/3_Risk_Predictor.py`)

- Input 13 clinical features across Demographics, Cardiac Metrics, and Clinical Values
- Logistic Regression model trained on UCI dataset
- Outputs disease probability % with Low / Medium / High risk classification
- Personalized health recommendations based on risk level
- Model accuracy: ~83–85%

---

## 🛠️ Tech Stack

| Tool                      | Usage                          |
| ------------------------- | ------------------------------ |
| Python                    | Core language                  |
| Streamlit                 | Web app framework              |
| Pandas                    | Data processing                |
| Plotly Express            | Interactive charts             |
| Scikit-learn              | ML model (Logistic Regression) |
| UCI Heart Disease Dataset | Cleveland, 297 patients        |

---

---

## ⚠️ Disclaimer

> This app is for **educational purposes only** and is not a substitute for professional medical advice. Always consult a qualified healthcare provider for medical decisions.

---

## 👤 Author

**Aarya** — Data Analyst | Power BI | Python | Streamlit  
📍 Mumbai, India  
🔗 [LinkedIn](https://www.linkedin.com/in/sachin-mishra431/) | [GitHub](https://github.com/sach431)

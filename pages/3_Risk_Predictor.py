import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

st.set_page_config(
    page_title=" Predictor — PulseIQ",
    layout="wide",
    page_icon="🔬",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600&display=swap');

:root {
    --bg:      #f4f6fb;
    --surface: #ffffff;
    --border:  #e8ecf4;
    --text:    #0f1623;
    --muted:   #7a869a;
    --coral:   #ff5c5c;
    --teal:    #00b4a6;
    --blue:    #4477ff;
    --shadow:  0 2px 16px rgba(0,0,0,0.06);
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text);
}
.main, .block-container { background-color: var(--bg) !important; padding: 1.8rem 2.5rem; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] * { color: #3a4560 !important; }
.sidebar-brand {
    font-family: 'Syne', sans-serif;
    font-size: 1.15rem;
    font-weight: 800;
    color: var(--coral) !important;
    padding-bottom: 1.2rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.4rem;
}

/* Header */
.page-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.1rem;
    font-weight: 800;
    color: var(--text);
    line-height: 1.15;
    margin-bottom: 0.3rem;
}
.page-title span { color: var(--coral); }
.page-sub {
    font-size: 0.82rem;
    color: var(--muted);
    margin-bottom: 1.6rem;
}

/* Section label */
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: var(--text);
    margin: 1.4rem 0 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-label::after { content:''; flex:1; height:1px; background:var(--border); }

/* Input card */
.input-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.2rem 1.4rem 1rem;
    box-shadow: var(--shadow);
}
.input-card-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    padding: 0.25rem 0.7rem;
    border-radius: 20px;
    display: inline-block;
    margin-bottom: 1rem;
}
.tag-demo  { background:#fff0ee; color:var(--coral);  }
.tag-card  { background:#e8f8f7; color:var(--teal);   }
.tag-clin  { background:#eef2ff; color:var(--blue);   }

/* Predict button */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #ff5c5c, #ff8c69) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    padding: 0.75rem 2rem !important;
    width: 100% !important;
    letter-spacing: 0.04em !important;
    box-shadow: 0 4px 15px rgba(255,92,92,0.3) !important;
    transition: all 0.2s !important;
}
div[data-testid="stButton"] > button:hover { opacity: 0.88 !important; transform: translateY(-1px) !important; }

/* Result panels */
.result-panel {
    border-radius: 16px;
    padding: 2rem 2rem 1.6rem;
    text-align: center;
    box-shadow: var(--shadow);
}
.result-high { background: linear-gradient(135deg, #fff5f5, #ffe8e8); border: 1.5px solid #ffb3b3; }
.result-low  { background: linear-gradient(135deg, #f0fdf9, #e0faf5); border: 1.5px solid #99e6da; }
.result-icon  { font-size: 2.5rem; margin-bottom: 0.5rem; }
.result-tag   {
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; margin-bottom: 0.4rem;
}
.result-pct {
    font-family: 'Syne', sans-serif;
    font-size: 3.8rem;
    font-weight: 800;
    line-height: 1;
}
.result-high .result-pct { color: var(--coral); }
.result-low  .result-pct { color: var(--teal);  }
.result-high .result-tag { color: #cc2a2a; }
.result-low  .result-tag { color: #007a6e; }
.result-desc { font-size: 0.8rem; color: var(--muted); margin-top: 0.5rem; }

/* Progress bar */
.prog-wrap { background: #e8ecf4; border-radius: 50px; height: 8px; margin: 1rem 0 0; overflow: hidden; }
.prog-high { height: 100%; border-radius: 50px; background: linear-gradient(90deg, #ff5c5c, #ff8c69); }
.prog-low  { height: 100%; border-radius: 50px; background: linear-gradient(90deg, #00b4a6, #4ade80); }

/* Mini metrics */
.mini-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.7rem; margin-bottom: 0.8rem; }
.mini-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 0.75rem 1rem;
    text-align: center;
    box-shadow: var(--shadow);
}
.mini-label { font-size: 0.65rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; color: var(--muted); margin-bottom: 0.2rem; }
.mini-val   { font-family: 'Syne', sans-serif; font-size: 1.3rem; font-weight: 700; color: var(--text); }

/* Advice */
.advice-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    font-size: 0.83rem;
    color: #3a4560;
    line-height: 1.65;
    box-shadow: var(--shadow);
}
.advice-box strong { color: var(--text); }

/* Widget overrides */
div[data-testid="stSlider"] label,
div[data-testid="stSelectbox"] label { color: #3a4560 !important; font-size: 0.8rem !important; }
div[data-baseweb="select"] > div {
    background: #f4f6fb !important;
    border-color: var(--border) !important;
    border-radius: 10px !important;
}
hr { border-color: var(--border) !important; }
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)

# ── Train model ───────────────────────────────────────────────────────────────
@st.cache_resource
def train_model():
    df = pd.read_csv('data/heart.csv')
    X = df[['age','sex','cp','trestbps','chol','fbs',
            'restecg','thalach','exang','oldpeak','slope','ca','thal']]
    y = df['target']
    sc = StandardScaler()
    Xs = sc.fit_transform(X)
    m  = LogisticRegression(max_iter=1000)
    m.fit(Xs, y)
    return m, sc

model, scaler = train_model()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-brand">🫀 CardioSense</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.78rem;color:#7a869a;line-height:1.7;">
    Uses <strong style="color:#ff5c5c">Logistic Regression</strong> trained on UCI Heart Disease dataset (Cleveland, n=297).<br><br>
    <span style="color:#b0b8cc;font-size:0.7rem;">⚠ For educational use only. Not a substitute for medical advice.</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<p style="font-size:0.65rem;color:#b0b8cc;">MODEL: LOGISTIC REGRESSION<br/>ACCURACY: ~83–85%<br/>FEATURES: 13</p>', unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="page-title">PulseIQ Risk <span>Engine</span></div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Enter patient vitals — ML model assesses cardiovascular disease risk</div>', unsafe_allow_html=True)

# ── Input Form ────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">🧬 Patient Information</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown('<div class="input-card"><span class="input-card-title tag-demo">Demographics</span>', unsafe_allow_html=True)
    age  = st.slider("Age", 20, 80, 45)
    sex  = st.selectbox("Gender", ["Male", "Female"])
    fbs  = st.selectbox("Fasting Blood Sugar > 120 mg/dL", ["No (0)", "Yes (1)"])
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="input-card"><span class="input-card-title tag-card">Cardiac Metrics</span>', unsafe_allow_html=True)
    cp      = st.selectbox("Chest Pain Type", ["Typical Angina (1)", "Atypical Angina (2)", "Non-Anginal (3)", "Asymptomatic (4)"])
    thalach = st.slider("Max Heart Rate (bpm)", 70, 210, 150)
    exang   = st.selectbox("Exercise Induced Angina", ["No (0)", "Yes (1)"])
    restecg = st.selectbox("Resting ECG", ["Normal (0)", "ST-T Abnormality (1)", "LV Hypertrophy (2)"])
    st.markdown('</div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="input-card"><span class="input-card-title tag-clin">Clinical Values</span>', unsafe_allow_html=True)
    trestbps = st.slider("Resting Blood Pressure (mmHg)", 90, 200, 120)
    chol     = st.slider("Cholesterol (mg/dL)", 100, 600, 245)
    oldpeak  = st.slider("ST Depression", 0.0, 6.0, 1.0, step=0.1)
    slope    = st.selectbox("Slope of ST Segment", ["Upsloping (1)", "Flat (2)", "Downsloping (3)"])
    ca       = st.selectbox("Major Vessels (0–3)", [0, 1, 2, 3])
    thal     = st.selectbox("Thalassemia", ["Normal (3)", "Fixed Defect (6)", "Reversible Defect (7)"])
    st.markdown('</div>', unsafe_allow_html=True)

# ── Predict ───────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">⚡ Result</div>', unsafe_allow_html=True)
clicked = st.button("Analyse Risk Profile", use_container_width=True)

if clicked:
    sex_v  = 1 if sex == "Male" else 0
    cp_v   = int(cp.split("(")[1].replace(")",""))
    fbs_v  = int(fbs.split("(")[1].replace(")",""))
    ecg_v  = int(restecg.split("(")[1].replace(")",""))
    ex_v   = int(exang.split("(")[1].replace(")",""))
    sl_v   = int(slope.split("(")[1].replace(")",""))
    th_v   = int(thal.split("(")[1].replace(")",""))

    X = np.array([[age, sex_v, cp_v, trestbps, chol, fbs_v,
                   ecg_v, thalach, ex_v, oldpeak, sl_v, ca, th_v]])
    prob = model.predict_proba(scaler.transform(X))[0][1] * 100
    pred = model.predict(scaler.transform(X))[0]

    r1, r2 = st.columns([1.1, 1])

    with r1:
        if pred == 1:
            st.markdown(f"""
            <div class="result-panel result-high">
                <div class="result-icon">⚠️</div>
                <div class="result-tag">High Risk Detected</div>
                <div class="result-pct">{prob:.1f}%</div>
                <div class="result-desc">Disease probability based on 13 clinical features</div>
                <div class="prog-wrap"><div class="prog-high" style="width:{min(prob,100):.0f}%"></div></div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-panel result-low">
                <div class="result-icon">✅</div>
                <div class="result-tag">Low Risk</div>
                <div class="result-pct">{prob:.1f}%</div>
                <div class="result-desc">Disease probability based on 13 clinical features</div>
                <div class="prog-wrap"><div class="prog-low" style="width:{min(prob,100):.0f}%"></div></div>
            </div>
            """, unsafe_allow_html=True)

    with r2:
        st.markdown(f"""
        <div class="mini-grid">
            <div class="mini-card"><div class="mini-label">Age</div><div class="mini-val">{age}</div></div>
            <div class="mini-card"><div class="mini-label">Max HR</div><div class="mini-val">{thalach}</div></div>
            <div class="mini-card"><div class="mini-label">Cholesterol</div><div class="mini-val">{chol}</div></div>
            <div class="mini-card"><div class="mini-label">Blood Pressure</div><div class="mini-val">{trestbps}</div></div>
        </div>
        """, unsafe_allow_html=True)

        if prob > 70:
            advice = "<strong>High priority:</strong> Immediate cardiology consultation recommended. Review lipid panel and ECG findings thoroughly."
        elif prob > 40:
            advice = "<strong>Moderate risk:</strong> Lifestyle modifications advised — balanced diet, regular exercise, BP monitoring. Follow-up in 3 months."
        else:
            advice = "<strong>Low risk:</strong> Maintain current healthy lifestyle. Annual checkup sufficient. Keep cholesterol and BP in optimal range."

        st.markdown(f'<div class="advice-box">💡 {advice}</div>', unsafe_allow_html=True)
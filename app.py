import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="PulseIQ — Analytics",
    layout="wide",
    page_icon="🫀",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600&display=swap');

:root {
    --bg:      #0E0E0E;
    --surface: #151515;
    --border:  #2A1A1A;
    --text:    #FFFFFF;
    --muted:   #888888;
    --coral:   #E0292A;
    --teal:    #A0A0A0;
    --blue:    #C0C0C0;
    --yellow:  #BBBBBB;
    --shadow:  0 2px 16px rgba(0,0,0,0.4);
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text);
}
.main, .block-container {
    background-color: var(--bg) !important;
    padding: 1.8rem 2.5rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0A0A0A !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] * { color: #AAAAAA !important; }
.sidebar-brand {
    font-family: 'Syne', sans-serif;
    font-size: 1.15rem;
    font-weight: 800;
    color: var(--coral) !important;
    padding-bottom: 1.2rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.4rem;
}
.sidebar-section {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted) !important;
    margin-bottom: 0.6rem;
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
.page-tag {
    display: inline-block;
    background: #2A0A0A;
    color: var(--coral);
    border: 1px solid #5A1A1A;
    border-radius: 20px;
    padding: 0.25rem 0.75rem;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    margin-bottom: 1.6rem;
}

/* KPI Cards */
.kpi-row { display: flex; gap: 1rem; margin-bottom: 1.6rem; }
.kpi {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    flex: 1;
    box-shadow: var(--shadow);
    position: relative;
    overflow: hidden;
    border-top: 2px solid var(--coral);
}
.kpi-icon {
    width: 36px; height: 36px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
    margin-bottom: 0.9rem;
}
.kpi-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    color: var(--coral);
    text-transform: uppercase;
    margin-bottom: 0.2rem;
}
.kpi-value {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--text);
    line-height: 1;
}
.kpi-sub { font-size: 0.72rem; font-weight: 500; margin-top: 0.3rem; }
.kpi-dot {
    position: absolute;
    width: 90px; height: 90px;
    border-radius: 50%;
    opacity: 0.05;
    top: -25px; right: -25px;
}

/* Section label */
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: var(--text);
    margin: 1.6rem 0 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* Chart Cards */
.chart-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.2rem 1.4rem 0.4rem;
    box-shadow: var(--shadow);
}
.chart-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.85rem;
    font-weight: 700;
    color: var(--text);
}
.chart-sub {
    font-size: 0.7rem;
    color: var(--muted);
    margin-bottom: 0.5rem;
}

/* Streamlit widget overrides */
div[data-testid="stSlider"] label,
div[data-testid="stMultiSelect"] label { color: #AAAAAA !important; font-size: 0.8rem !important; }
div[data-baseweb="select"] > div {
    background: #1A1A1A !important;
    border-color: var(--border) !important;
    border-radius: 10px !important;
    color: #FFFFFF !important;
}
hr { border-color: var(--border) !important; }
#MainMenu, footer { visibility: hidden; }
header { visibility: visible !important; background: #0E0E0E !important; }
.stDeployButton { display: block !important; }
[data-testid="collapsedControl"] { display: flex !important; visibility: visible !important; color: #E0292A !important; }
</style>
""", unsafe_allow_html=True)

# ── Plotly theme ─────────────────────────────────────────────────────────────
BG     = "#151515"
GRID   = "#2A1A1A"
FC     = "#888888"
CORAL  = "#E0292A"
TEAL   = "#666666"
BLUE   = "#999999"
YELLOW = "#BBBBBB"
CMAP   = {"Disease": CORAL, "No Disease": "#3D1010"}

def style(fig, h=280):
    fig.update_layout(
        plot_bgcolor=BG, paper_bgcolor=BG, height=h,
        margin=dict(l=8, r=8, t=8, b=8),
        font=dict(family="Plus Jakarta Sans", color=FC, size=11),
        legend=dict(bgcolor="rgba(0,0,0,0)", borderwidth=0, font=dict(color="#AAAAAA")),
        xaxis=dict(gridcolor=GRID, linecolor=GRID, color="#AAAAAA"),
        yaxis=dict(gridcolor=GRID, linecolor=GRID, color="#AAAAAA"),
    )
    return fig

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load():
    df = pd.read_csv('data/heart.csv')
    df['target_label'] = df['target'].map({1: 'Disease', 0: 'No Disease'})
    df['sex_label']    = df['sex'].map({1: 'Male', 0: 'Female'})
    df['age_group']    = pd.cut(df['age'], bins=[20,35,45,55,65,80],
                                labels=['20–35','35–45','45–55','55–65','65+'])
    return df

df = load()

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-brand">🫀 PulseIQ</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section">Filters</div>', unsafe_allow_html=True)
    gender    = st.multiselect("Gender", options=list(df['sex_label'].unique()), default=list(df['sex_label'].unique()))
    age_range = st.slider("Age Range", int(df['age'].min()), int(df['age'].max()), (30, 65))
    st.markdown("---")

filtered = df[df['sex_label'].isin(gender) & df['age'].between(*age_range)]
d_pct = round(filtered['target'].mean()*100, 1) if len(filtered) else 0

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="page-title">PulseIQ <span>Analytics</span></div>
<span class="page-tag">● {len(filtered)} patients loaded</span>
""", unsafe_allow_html=True)

# ── KPI Row ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="kpi-row">
  <div class="kpi">
    <div class="kpi-icon" style="background:#2A0A0A;">🧑‍⚕️</div>
    <div class="kpi-dot" style="background:{CORAL}"></div>
    <div class="kpi-label">Total Patients</div>
    <div class="kpi-value">{len(filtered)}</div>
    <div class="kpi-sub" style="color:#888888">Filtered records</div>
  </div>
  <div class="kpi">
    <div class="kpi-icon" style="background:#2A0A0A;">❤️</div>
    <div class="kpi-dot" style="background:{CORAL}"></div>
    <div class="kpi-label">Disease Cases</div>
    <div class="kpi-value">{int(filtered['target'].sum())}</div>
    <div class="kpi-sub" style="color:{CORAL}">{d_pct}% prevalence</div>
  </div>
  <div class="kpi">
    <div class="kpi-icon" style="background:#2A0A0A;">📅</div>
    <div class="kpi-dot" style="background:{CORAL}"></div>
    <div class="kpi-label">Average Age</div>
    <div class="kpi-value">{round(filtered['age'].mean(),1)}</div>
    <div class="kpi-sub" style="color:#888888">years</div>
  </div>
  <div class="kpi">
    <div class="kpi-icon" style="background:#2A0A0A;">🧪</div>
    <div class="kpi-dot" style="background:{CORAL}"></div>
    <div class="kpi-label">Avg Cholesterol</div>
    <div class="kpi-value">{round(filtered['chol'].mean(),1)}</div>
    <div class="kpi-sub" style="color:#888888">mg/dL</div>
  </div>
  <div class="kpi">
    <div class="kpi-icon" style="background:#2A0A0A;">💓</div>
    <div class="kpi-dot" style="background:{CORAL}"></div>
    <div class="kpi-label">Avg Max HR</div>
    <div class="kpi-value">{round(filtered['thalach'].mean(),1)}</div>
    <div class="kpi-sub" style="color:#888888">bpm</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Row 1 ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">📊 Distribution Overview</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns([1.3, 1.3, 0.9])

with c1:
    st.markdown('<div class="chart-card"><div class="chart-label">Disease by Age Group</div><div class="chart-sub">Grouped by presence of heart disease</div>', unsafe_allow_html=True)
    d = filtered.groupby(['age_group','target_label'], observed=True).size().reset_index(name='n')
    fig = px.bar(d, x='age_group', y='n', color='target_label', barmode='group',
                 color_discrete_map=CMAP, labels={'n':'Patients','age_group':'Age Group'})
    fig.update_traces(marker_line_width=0, marker_cornerradius=4)
    style(fig)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar':False})
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="chart-card"><div class="chart-label">Gender Breakdown</div><div class="chart-sub">Male vs Female disease comparison</div>', unsafe_allow_html=True)
    d2 = filtered.groupby(['sex_label','target_label']).size().reset_index(name='n')
    fig2 = px.bar(d2, x='sex_label', y='n', color='target_label', barmode='group',
                  color_discrete_map=CMAP, labels={'n':'Patients','sex_label':'Gender'})
    fig2.update_traces(marker_line_width=0, marker_cornerradius=4)
    style(fig2)
    st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar':False})
    st.markdown('</div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="chart-card"><div class="chart-label">Disease Split</div><div class="chart-sub">Overall proportion</div>', unsafe_allow_html=True)
    d3 = filtered['target_label'].value_counts().reset_index()
    d3.columns = ['label','count']
    fig3 = px.pie(d3, names='label', values='count', color='label',
                  color_discrete_map=CMAP, hole=0.62)
    fig3.update_traces(textfont_size=11, marker=dict(line=dict(color='#0E0E0E', width=3)))
    fig3.update_layout(plot_bgcolor=BG, paper_bgcolor=BG, height=280,
                       margin=dict(l=0,r=0,t=0,b=0),
                       legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#AAAAAA", size=11)),
                       font=dict(family="Plus Jakarta Sans"))
    st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar':False})
    st.markdown('</div>', unsafe_allow_html=True)

# ── Row 2 ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">🔬 Risk Factor Analysis</div>', unsafe_allow_html=True)
c4, c5 = st.columns(2)

with c4:
    st.markdown('<div class="chart-card"><div class="chart-label">Cholesterol vs Max Heart Rate</div><div class="chart-sub">Scatter by disease status</div>', unsafe_allow_html=True)
    fig4 = px.scatter(filtered, x='chol', y='thalach', color='target_label',
                      opacity=0.75, color_discrete_map=CMAP,
                      labels={'chol':'Cholesterol (mg/dL)','thalach':'Max HR (bpm)'})
    fig4.update_traces(marker=dict(size=7, line=dict(width=1, color='#0E0E0E')))
    style(fig4, 300)
    st.plotly_chart(fig4, use_container_width=True, config={'displayModeBar':False})
    st.markdown('</div>', unsafe_allow_html=True)

with c5:
    st.markdown('<div class="chart-card"><div class="chart-label">Correlation Matrix</div><div class="chart-sub">Feature relationships</div>', unsafe_allow_html=True)
    corr = filtered[['age','trestbps','chol','thalach','oldpeak','target']].corr().round(2)
    fig5 = px.imshow(corr, text_auto=True,
                     color_continuous_scale=[[0,'#3D1010'],[0.5,'#2A2A2A'],[1,'#E0292A']],
                     zmin=-1, zmax=1)
    fig5.update_traces(textfont_size=11)
    fig5.update_layout(plot_bgcolor=BG, paper_bgcolor=BG, height=300,
                       margin=dict(l=0,r=0,t=0,b=0), coloraxis_showscale=False,
                       font=dict(family="Plus Jakarta Sans", color="#AAAAAA", size=11))
    st.plotly_chart(fig5, use_container_width=True, config={'displayModeBar':False})
    st.markdown('</div>', unsafe_allow_html=True)

# ── Row 3 ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">📈 Distributions</div>', unsafe_allow_html=True)
c6, c7 = st.columns(2)

with c6:
    st.markdown('<div class="chart-card"><div class="chart-label">Age Distribution</div><div class="chart-sub">Overlay by disease status</div>', unsafe_allow_html=True)
    fig6 = px.histogram(filtered, x='age', color='target_label', nbins=25,
                        barmode='overlay', opacity=0.75, color_discrete_map=CMAP,
                        labels={'age':'Age (years)'})
    fig6.update_traces(marker_line_width=0)
    style(fig6, 260)
    st.plotly_chart(fig6, use_container_width=True, config={'displayModeBar':False})
    st.markdown('</div>', unsafe_allow_html=True)

with c7:
    st.markdown('<div class="chart-card"><div class="chart-label">Resting Blood Pressure</div><div class="chart-sub">Distribution by disease status</div>', unsafe_allow_html=True)
    fig7 = px.histogram(filtered, x='trestbps', color='target_label', nbins=30,
                        barmode='overlay', opacity=0.75, color_discrete_map=CMAP,
                        labels={'trestbps':'BP (mmHg)'})
    fig7.update_traces(marker_line_width=0)
    style(fig7, 260)
    st.plotly_chart(fig7, use_container_width=True, config={'displayModeBar':False})
    st.markdown('</div>', unsafe_allow_html=True)
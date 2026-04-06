from pathlib import Path
import sys

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from backend import get_about_charts, get_project_paths, get_runtime

st.set_page_config(page_title="About | AgriPredict", page_icon="📘", layout="wide")

PALETTE = {
    "bg": "#F0F7F0",
    "card": "#FFFFFF",
    "soft": "#E8F5E4",
    "green": "#2D7D46",
    "green_2": "#52A46A",
    "green_3": "#A8D5B5",
    "gold": "#E8A020",
    "blue": "#4A90C4",
    "teal": "#3AAFA9",
    "text": "#1A2E1F",
    "muted": "#5A7060",
    "line": "#C8E0CE",
}

CSS = f"""
<style>
.stApp {{background: linear-gradient(160deg, #EBF5EB 0%, #F5FBF5 40%, #FAFFF9 100%); color:{PALETTE['text']};}}
[data-testid="stSidebar"] {{display:none;}}
[data-testid="collapsedControl"] {{display:none;}}
.block-container {{padding-top:1rem; padding-bottom:3rem; max-width:1200px;}}
.nav-shell {{
    background:rgba(255,255,255,.97); border:1px solid {PALETTE['line']}; border-radius:20px;
    padding:.65rem 1.1rem; box-shadow:0 4px 24px rgba(45,125,70,.08); margin-bottom:1.4rem;
}}
.brand {{display:flex; align-items:center; gap:.7rem; font-weight:800; font-size:1.75rem; color:{PALETTE['green']}; letter-spacing:-.5px;}}
.brand-badge {{
    width:40px; height:40px; border-radius:14px;
    background:linear-gradient(135deg,{PALETTE['green']},{PALETTE['green_2']});
    color:white; display:flex; align-items:center; justify-content:center; font-size:1.1rem;
    box-shadow:0 6px 16px rgba(45,125,70,.30);
}}
.hero-card {{
    padding:2.2rem 2rem;
    background: linear-gradient(135deg, #FFFFFF 0%, #F0FBF4 50%, #E5F7EC 100%);
    border:1px solid {PALETTE['line']}; border-radius:28px;
    box-shadow:0 8px 40px rgba(45,125,70,.08);
    position:relative; overflow:hidden;
    margin-bottom:1.6rem;
}}
.hero-card::before {{
    content:''; position:absolute; top:-80px; right:-80px;
    width:260px; height:260px;
    background:radial-gradient(circle,rgba(82,164,106,.12) 0%,transparent 70%);
    pointer-events:none;
}}
.kicker {{
    display:inline-flex; align-items:center; gap:.4rem;
    padding:.4rem .9rem; border-radius:999px; font-size:.8rem; font-weight:700;
    color:{PALETTE['teal']}; border:1px solid rgba(58,175,169,.35); background:rgba(58,175,169,.08);
    letter-spacing:.04em; text-transform:uppercase;
}}
.kicker-gold {{
    display:inline-flex; align-items:center; gap:.4rem;
    padding:.4rem .9rem; border-radius:999px; font-size:.8rem; font-weight:700;
    color:{PALETTE['gold']}; border:1px solid rgba(232,160,32,.38); background:rgba(232,160,32,.08);
    letter-spacing:.04em; text-transform:uppercase;
}}
.hero-title {{
    font-size:3rem; line-height:1.13; font-weight:900; margin:.9rem 0 .75rem;
    color:{PALETTE['text']}; text-align:center; letter-spacing:-1.2px;
}}
.hero-title span {{color:{PALETTE['green']};}}
.hero-copy {{
    font-size:1.05rem; color:{PALETTE['muted']}; line-height:1.9;
    max-width:760px; margin:0 auto; text-align:center;
}}
.soft-card, .metric-card, .feature-card, .workflow-card, .data-card {{
    background:rgba(255,255,255,.97); border:1px solid {PALETTE['line']};
    border-radius:22px; box-shadow:0 4px 20px rgba(45,125,70,.06);
}}
.soft-card {{padding:1.4rem 1.45rem; height:100%;}}
.data-card {{padding:1.4rem 1.45rem; height:100%;}}
.metric-card {{padding:1.1rem 1.1rem;}}
.metric-value {{font-size:2rem; font-weight:900; letter-spacing:-.5px;}}
.metric-label {{font-size:.88rem; color:{PALETTE['muted']}; margin-top:.15rem;}}
.metric-icon {{font-size:1.5rem; margin-bottom:.3rem;}}
.feature-card {{
    padding:1rem 1.05rem; margin-bottom:.75rem;
    border-left:3px solid {PALETTE['green_3']};
}}
.small-note {{font-size:.9rem; color:{PALETTE['muted']};}}
.workflow-card {{
    padding:1.1rem 1.05rem; min-height:170px;
    border-top:3px solid {PALETTE['teal']};
}}
.section-kicker {{
    display:inline-flex; align-items:center; gap:.4rem;
    font-size:.8rem; font-weight:700; color:{PALETTE['teal']};
    border:1px solid rgba(58,175,169,.35); border-radius:999px;
    padding:.38rem .85rem; background:rgba(58,175,169,.08);
    letter-spacing:.04em; text-transform:uppercase;
}}
.data-row {{
    display:flex; justify-content:space-between; align-items:center;
    padding:.7rem 0; border-bottom:1px solid {PALETTE['line']};
}}
.data-row:last-child {{border-bottom:none;}}
div[data-testid="stPageLink"] a {{
    padding:.55rem 1.05rem; border-radius:14px; text-decoration:none;
    font-weight:700; color:{PALETTE['muted']}; border:1px solid transparent;
}}
div[data-testid="stPageLink"] a:hover {{
    color:{PALETTE['green']}; background:#EFF7EF; border-color:{PALETTE['line']};
}}
div[data-testid="stPageLink"] a[aria-current="page"] {{
    background:linear-gradient(135deg,{PALETTE['green']},{PALETTE['green_2']});
    color:white !important; border-color:{PALETTE['green']};
    box-shadow:0 6px 18px rgba(45,125,70,.28);
}}
.chart-wrap {{
    background:rgba(255,255,255,.97); border:1px solid {PALETTE['line']};
    border-radius:22px; box-shadow:0 4px 20px rgba(45,125,70,.06);
    padding:.8rem;
}}
.section-title {{
    font-size:2rem; line-height:1.2; font-weight:900;
    color:{PALETTE['text']}; margin:.8rem 0 .5rem; letter-spacing:-.6px;
}}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


def render_top_nav() -> None:
    left, mid, right = st.columns([1.2, 0.8, 1.4], vertical_alignment="center")
    with left:
        st.markdown('<div class="brand"><div class="brand-badge">🌾</div><div>AgriPredict</div></div>', unsafe_allow_html=True)
    with mid:
        st.page_link("app.py", label="🏠 Home")
    with right:
        a, b = st.columns(2)
        with a:
            st.page_link("pages/1_About.py", label="📘 About")
        with b:
            st.page_link("pages/2_Predict.py", label="🔮 Predict Yield")


@st.cache_resource(show_spinner=False)
def load_runtime():
    return get_runtime()


@st.cache_data(show_spinner=False)
def load_charts():
    return get_about_charts()


runtime = load_runtime()
charts = load_charts()
paths = get_project_paths()


def style_fig(fig, height=330):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=PALETTE["text"], size=12),
        title=dict(font=dict(size=17, color=PALETTE["text"]), x=0.02),
        margin=dict(l=18, r=18, t=52, b=18),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(showgrid=True, gridcolor="rgba(200,224,206,.4)", zeroline=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(200,224,206,.4)", zeroline=False),
    )
    return fig


comparison_fig = style_fig(charts["comparison"], height=320)
comparison_fig.update_traces(marker_line_width=0)
actual_pred_fig = style_fig(charts["actual_vs_predicted"], height=320)
actual_pred_fig.update_traces(marker=dict(size=8, color=PALETTE["green_2"], opacity=0.68))
relationship_fig = style_fig(charts["feature_relationship"], height=310)
relationship_fig.update_traces(marker_color=PALETTE["teal"])

# ─── NAV ───
st.markdown('<div class="nav-shell">', unsafe_allow_html=True)
render_top_nav()
st.markdown('</div>', unsafe_allow_html=True)

# ─── HERO ───
st.markdown('<div class="hero-card">', unsafe_allow_html=True)
st.markdown('<div style="text-align:center;"><span class="kicker">📘 About This Project</span></div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="hero-title">Crop Yield Prediction<br><span>Using Machine Learning</span></div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="hero-copy">This page presents the project architecture, dataset details, and model evaluation results. '
    'The app reads the real dataset, uses the same saved model artifact, and serves live predictions through the existing backend pipeline.</div>',
    unsafe_allow_html=True,
)
st.markdown('</div>', unsafe_allow_html=True)

# ─── DATASET + FEATURES ───
left, right = st.columns([1.08, 0.92], gap="large")
with left:
    st.markdown('<div class="data-card">', unsafe_allow_html=True)
    st.markdown("<span class='kicker-gold'>🗂️ Dataset Details</span>", unsafe_allow_html=True)
    st.markdown("<div class='section-title' style='text-align:left;'>The Crop Yield Dataset</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='small-note' style='line-height:1.95; margin-bottom:1.2rem;'>The dataset contains <strong>{runtime.metrics['rows_raw']:,}</strong> rows of agricultural records. "
        f"The cleaned training data retains <strong>{runtime.metrics['rows_processed']:,}</strong> rows after preprocessing and outlier handling. "
        f"The target variable is crop yield, predicted from fertilizer, temperature, and soil nutrient values.</div>",
        unsafe_allow_html=True,
    )
    overview_rows = [
        ("📦 Total Samples", f"{runtime.metrics['rows_raw']:,}"),
        ("✅ Processed Rows", f"{runtime.metrics['rows_processed']:,}"),
        ("🎯 Target Variable", "yield (tons per hectare)"),
        ("🔧 Missing Values", "Imputed using column medians"),
        ("🔢 Negative Values", "Corrected using abs()"),
        ("📊 Train / Test Split", "80% / 20%"),
    ]
    for label, value in overview_rows:
        st.markdown(
            f"<div class='data-row'><span class='small-note'>{label}</span>"
            f"<span style='font-weight:700; color:{PALETTE['text']}; font-size:.95rem;'>{value}</span></div>",
            unsafe_allow_html=True,
        )
    
   # st.code(
      #  f"Dataset path  : {paths['data']}\nModel artifact: {paths['model']}\nMetadata file : {paths['metadata']}\nNotebook ref  : {paths['notebook']}",
       # language="text",
   # )
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    features = [
        ("🌿", "Fertilizer", "Total fertilizer applied to the field (kg per hectare)."),
        ("🌡️", "Temperature", "Average field temperature during the growing season (°C)."),
        ("🧬", "Nitrogen (N)", "Soil nitrogen content — important for leaf and shoot growth."),
        ("🧂", "Phosphorus (P)", "Soil phosphorus that supports root development and energy transfer."),
        ("🪴", "Potassium (K)", "Soil potassium linked to water balance and crop resilience."),
        ("🌾", "Yield", "The final crop output in tons/ha that the model estimates."),
    ]
    for emoji, title, desc in features:
        st.markdown(
            f"<div class='feature-card'>"
            f"<div style='font-weight:700; color:{PALETTE['text']}; margin-bottom:.3rem; font-size:1rem;'>{emoji} {title}</div>"
            f"<div class='small-note' style='line-height:1.7;'>{desc}</div></div>",
            unsafe_allow_html=True,
        )

# ─── METRICS ───
st.write("")
st.markdown("<span class='section-kicker'>📊 Model Evaluation</span>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>Performance Metrics</div>", unsafe_allow_html=True)
st.markdown(
    f"<div class='small-note' style='margin-bottom:1.2rem;'>These values are read from the existing backend-generated metadata, so the UI remains synced with the real pipeline outputs.</div>",
    unsafe_allow_html=True,
)

m1, m2, m3, m4 = st.columns(4, gap="large")
for col, (emoji, label, value, color, bg) in zip(
    [m1, m2, m3, m4],
    [
        ("🎯", "R² Score", f"{runtime.metrics['r2']*100:.1f}%", PALETTE["green"], "linear-gradient(135deg,#F0FBF4,#E4F5EA)"),
        ("📉", "MAE", f"{runtime.metrics['mae']:.3f}", PALETTE["gold"], "linear-gradient(135deg,#FFFBF0,#FFF3D5)"),
        ("📏", "RMSE", f"{runtime.metrics['rmse']:.3f}", PALETTE["blue"], "linear-gradient(135deg,#EFF6FD,#E2EFFA)"),
        ("🏋️", "Train R²", f"{runtime.metrics['train_r2']*100:.1f}%", PALETTE["teal"], "linear-gradient(135deg,#EFF9F8,#E0F5F3)"),
    ],
):
    with col:
        st.markdown(
            f"<div class='metric-card' style='background:{bg};'>"
            f"<div class='metric-icon'>{emoji}</div>"
            f"<div class='metric-value' style='color:{color};'>{value}</div>"
            f"<div class='metric-label'>{label}</div></div>",
            unsafe_allow_html=True,
        )

# ─── CHARTS (only 2 most useful: model comparison + actual vs predicted) ───
st.write("")
c1, c2 = st.columns(2, gap="large")
with c1:
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.plotly_chart(comparison_fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.plotly_chart(actual_pred_fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ─── FEATURE RELATIONSHIP CHART ───
#st.markdown('<div class="chart-wrap" style="margin-top:1rem;">', unsafe_allow_html=True)
#t.plotly_chart(relationship_fig, use_container_width=True, config={"displayModeBar": False})
#st.markdown('</div>', unsafe_allow_html=True)

# ─── ML PIPELINE WORKFLOW ───
st.write("")
st.markdown("<span class='section-kicker'>🧩 ML Pipeline</span>", unsafe_allow_html=True)
st.markdown("<div class='section-title'>End-to-End Workflow</div>", unsafe_allow_html=True)
workflow = [
    ("📥", "Data Load", "The CSV file is loaded from its existing path without changing your original file setup."),
    ("🧹", "Preprocessing", "The backend normalizes columns, handles missing values, and prepares model-ready features."),
    ("📊", "EDA Visuals", "Frontend charts present backend-derived summaries in a cleaner, more user-friendly style."),
    ("🤖", "Model Training", "The trained Random Forest pipeline remains the same and continues to power prediction."),
    ("✅", "Evaluation", "MAE, RMSE, and R² are shown directly from the real backend metrics."),
]
flow_cols = st.columns(5, gap="large")
for col, (emoji, title, desc) in zip(flow_cols, workflow):
    with col:
        st.markdown(
            f"<div class='workflow-card'>"
            f"<div style='font-size:1.4rem; margin-bottom:.65rem;'>{emoji}</div>"
            f"<div style='font-weight:800; color:{PALETTE['text']}; margin-bottom:.45rem; font-size:.98rem;'>{title}</div>"
            f"<div class='small-note' style='line-height:1.7;'>{desc}</div></div>",
            unsafe_allow_html=True,
        )

# ─── CTA ───
st.write("")
cta1, cta2, cta3 = st.columns([1, 1, 1])
with cta2:
    st.page_link("pages/2_Predict.py", label="🔮 Try the Prediction Tool →", use_container_width=True)

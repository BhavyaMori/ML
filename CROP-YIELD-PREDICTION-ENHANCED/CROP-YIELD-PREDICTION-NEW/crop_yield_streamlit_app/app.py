from pathlib import Path
import sys
import base64
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent
sys.path.append(str(ROOT_DIR))

from backend import get_about_charts, get_runtime, refresh_runtime

st.set_page_config(page_title="Home | AgriPredict", page_icon="🌾", layout="wide")

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
    "accent": "#F0FBF4",
}

CSS = f"""
<style>
.stApp {{
    background: linear-gradient(160deg, #EBF5EB 0%, #F5FBF5 40%, #FAFFF9 100%);
    color: {PALETTE['text']};
}}
[data-testid="stSidebar"] {{display:none;}}
[data-testid="collapsedControl"] {{display:none;}}
.block-container {{padding-top: 1rem; padding-bottom: 3rem; max-width: 1200px;}}
.nav-shell {{
    background: rgba(255,255,255,0.97);
    border: 1px solid {PALETTE['line']};
    border-radius: 20px;
    padding: .65rem 1.1rem;
    box-shadow: 0 4px 24px rgba(45,125,70,.08);
    margin-bottom: 1.4rem;
}}
.brand {{display:flex; align-items:center; gap:.7rem; font-weight:800; font-size:1.75rem; color:{PALETTE['green']}; letter-spacing:-0.5px;}}
.brand-badge {{
    width:40px; height:40px; border-radius:14px;
    background: linear-gradient(135deg, {PALETTE['green']} 0%, {PALETTE['green_2']} 100%);
    color:white; display:flex; align-items:center; justify-content:center; font-size:1.1rem;
    box-shadow: 0 6px 16px rgba(45,125,70,.30);
}}
.hero-wrap {{
    background: linear-gradient(135deg, #FFFFFF 0%, #F0FBF4 50%, #E8F5E4 100%);
    border: 1px solid {PALETTE['line']};
    border-radius: 28px;
    padding: 2rem 1.8rem;
    box-shadow: 0 8px 40px rgba(45,125,70,.08);
    position: relative; overflow: hidden;
}}
.badge {{
    display:inline-flex; align-items:center; gap:.4rem;
    padding:.45rem 1rem; border-radius:999px; font-size:.85rem; font-weight:700;
    background: linear-gradient(135deg, #FFF3D6, #FDEBC0);
    color:{PALETTE['gold']}; border:1px solid rgba(232,160,32,.35);
}}
.hero-title {{
    font-size:3.4rem; line-height:1.1; color:{PALETTE['text']};
    font-weight:900; margin:.9rem 0 .85rem 0; letter-spacing:-1.5px;
}}
.hero-title span {{
    color: {PALETTE['green']};
}}
.hero-copy {{font-size:1.08rem; color:{PALETTE['muted']}; line-height:1.85; max-width:92%;}}
.hero-chip {{
    display:inline-flex; align-items:center; gap:.35rem;
    padding:.38rem .85rem; border-radius:999px;
    background: rgba(45,125,70,.09); border:1px solid rgba(45,125,70,.22);
    color:{PALETTE['green']}; font-weight:600; font-size:.82rem;
}}
.panel-card, .info-card, .step-card, .section-card {{
    background: rgba(255,255,255,0.97);
    border: 1px solid {PALETTE['line']};
    border-radius: 22px;
    box-shadow: 0 4px 20px rgba(45,125,70,.06);
}}
.panel-card {{padding:1.4rem;}}
.info-card {{padding:.9rem 1rem;}}
.step-card {{
    padding:1.5rem 1.3rem; min-height:240px;
    position: relative; overflow: hidden;
    border-top: 3px solid {PALETTE['green_2']};
}}
.section-card {{padding:1.3rem 1.4rem; height:100%;}}
.metric-band {{
    background: linear-gradient(135deg, {PALETTE['green']} 0%, #1E5C30 100%);
    color: white; padding: 1.5rem 1.5rem;
    margin: 1.4rem 0 1.6rem 0; border-radius: 24px;
    box-shadow: 0 8px 32px rgba(45,125,70,.25);
    position: relative; overflow: hidden;
}}
.metric-item {{text-align:center; padding:.5rem .3rem; position: relative; z-index: 1;}}
.metric-value {{font-size:2.3rem; font-weight:900; margin:.2rem 0; letter-spacing:-1px;}}
.metric-label {{font-size:.88rem; color: rgba(255,255,255,.75); font-weight:500;}}
.metric-icon {{font-size:1.4rem; margin-bottom:.3rem;}}
.section-kicker {{
    display:inline-flex; align-items:center; gap:.4rem;
    font-size:.8rem; font-weight:700; color:{PALETTE['teal']};
    border:1px solid rgba(58,175,169,.35); border-radius:999px;
    padding:.38rem .85rem; background: rgba(58,175,169,.08);
    letter-spacing:.04em; text-transform:uppercase;
}}
.section-title {{
    font-size:2.4rem; line-height:1.18; font-weight:900;
    color:{PALETTE['text']}; margin:.85rem 0 .65rem; text-align:center;
    letter-spacing:-1px;
}}
.section-copy {{
    font-size:1.05rem; color:{PALETTE['muted']}; line-height:1.85;
    max-width:760px; margin:0 auto 1.3rem auto; text-align:center;
}}
.feature-row {{margin:.9rem 0 1rem 0;}}
.feature-head {{
    display:flex; justify-content:space-between; align-items:center;
    font-size:.95rem; margin-bottom:.4rem; color:{PALETTE['text']};
}}
.feature-track {{height:9px; background:rgba(200,224,206,.4); border-radius:999px; overflow:hidden;}}
.feature-fill {{
    height:9px; border-radius:999px;
    background: linear-gradient(90deg, {PALETTE['green_3']} 0%, {PALETTE['green_2']} 60%, {PALETTE['green']} 100%);
}}
.feature-foot {{display:flex; justify-content:space-between; font-size:.77rem; color:#8FA890; margin-top:.25rem;}}
.step-index {{font-size:.9rem; color:{PALETTE['green_3']}; font-weight:800; margin-bottom:1rem; letter-spacing:.08em;}}
.step-emoji {{font-size:2rem; margin-bottom:.85rem; display:block;}}
.step-title {{font-size:1.45rem; font-weight:800; color:{PALETTE['text']}; margin-bottom:.6rem; letter-spacing:-.3px;}}
.step-copy {{font-size:.96rem; line-height:1.8; color:{PALETTE['muted']};}}
div[data-testid="stPageLink"] a {{
    padding:.55rem 1.05rem; border-radius:14px; text-decoration:none;
    font-weight:700; color:{PALETTE['muted']}; border:1px solid transparent;
}}
div[data-testid="stPageLink"] a:hover {{
    color:{PALETTE['green']}; background:#EFF7EF; border-color:{PALETTE['line']};
}}
div[data-testid="stPageLink"] a[aria-current="page"] {{
    background: linear-gradient(135deg, {PALETTE['green']}, {PALETTE['green_2']});
    color:white !important; border-color:{PALETTE['green']};
    box-shadow: 0 6px 18px rgba(45,125,70,.28);
}}
.small-note {{font-size:.9rem; color:{PALETTE['muted']};}}
.footer-band {{
    background: linear-gradient(135deg, #F0FBF4 0%, #E8F5E4 100%);
    border: 1px solid {PALETTE['line']}; border-radius: 22px;
    padding: 1.5rem 1.8rem; margin-top: 2rem; text-align: center;
}}
.hero-gif-card {{
    background: linear-gradient(135deg, #FFFFFF 0%, #F7FCF8 60%, #EEF8F0 100%);
    border: 1px solid {PALETTE['line']};
    border-radius: 24px;
    padding: .7rem;
    box-shadow: 0 8px 28px rgba(45,125,70,.08);
    min-height: 295px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
}}
.hero-gif-note {{
    text-align: center;
    margin-top: .45rem;
    font-size: .82rem;
    color: {PALETTE['muted']};
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
        nav1, nav2 = st.columns(2)
        with nav1:
            st.page_link("pages/1_About.py", label="📘 About")
        with nav2:
            st.page_link("pages/2_Predict.py", label="🔮 Predict Yield")


@st.cache_resource(show_spinner=False)
def load_runtime():
    return get_runtime()


@st.cache_data(show_spinner=False)
def load_about_charts():
    return get_about_charts()


runtime = load_runtime()
charts = load_about_charts()
model = runtime.pipeline.named_steps["model"]
feature_count = 5


def style_plotly(fig, height=330):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=PALETTE["text"], size=12),
        title=dict(font=dict(size=18, color=PALETTE["text"]), x=0.02),
        margin=dict(l=18, r=18, t=52, b=18),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(showgrid=True, gridcolor="rgba(200,224,206,.45)", zeroline=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(200,224,206,.45)", zeroline=False),
    )
    return fig


comparison_fig = style_plotly(charts["comparison"], height=295)
comparison_fig.update_traces(marker_line_width=0)

# ─── NAV ───
st.markdown('<div class="nav-shell">', unsafe_allow_html=True)
render_top_nav()
st.markdown('</div>', unsafe_allow_html=True)

# ─── HERO ───
hero_left, hero_right = st.columns([1.05, 0.95], gap="large", vertical_alignment="center")
with hero_left:
    st.markdown('<div class="hero-wrap">', unsafe_allow_html=True)
    st.markdown('<span class="badge">🌾 ML-Powered Agriculture &nbsp;•&nbsp; Random Forest Regressor</span>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="hero-title">Predict Crop Yield<br><span>with Precision.</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="hero-copy">Enter soil nutrients, fertilizer dosage, and temperature to instantly estimate crop yield — powered by a backend pipeline achieving <strong style="color:{PALETTE["green"]};">{runtime.metrics["r2"] * 100:.1f}% R² accuracy</strong> on real agricultural data.</div>',
        unsafe_allow_html=True,
    )
    st.write("")
    cta1, cta2, cta3 = st.columns([1.3, 1.1, 0.85])
    with cta1:
        st.page_link("pages/2_Predict.py", label="🔮 Try Prediction", use_container_width=True)
    with cta2:
        st.page_link("pages/1_About.py", label="Learn More →", use_container_width=True)
    with cta3:
        if st.button("↺ Refresh", use_container_width=True):
            refresh_runtime()
            load_runtime.clear()
            load_about_charts.clear()
            st.rerun()
    st.write("")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"<div class='hero-chip'>🎯 {runtime.metrics['r2']*100:.1f}% R²</div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='hero-chip'>📦 {runtime.metrics['rows_raw']:,} records</div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='hero-chip'>🌲 100 trees</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with hero_right:
    top_a, top_b = st.columns([1, 1])
    with top_a:
        st.markdown("<span class='small-note'><strong>🌱 CROP GROWTH VISUAL</strong></span>", unsafe_allow_html=True)
    with top_b:
        st.markdown("<div style='text-align:right;'><span class='hero-chip'>Live Animation</span></div>", unsafe_allow_html=True)
    
    gif_path = ROOT_DIR / "crop_growth_step_by_step.gif"
    with open(gif_path, "rb") as f:
        gif_base64 = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <div class="hero-gif-card">
            <img src="data:image/gif;base64,{gif_base64}"
                 style="width:100%; height:295px; object-fit:cover; border-radius:18px; display:block;" />
        </div>
        <div class='hero-gif-note'>Step-by-step crop growth from seed to mature plant</div>
        """,
        unsafe_allow_html=True,
    )

    k1, k2, k3 = st.columns(3)
    for col, (val, lbl, color) in zip(
        [k1, k2, k3],
        [
            (f"{runtime.metrics['r2']*100:.1f}%", "R² Score", PALETTE["green"]),
            (f"{runtime.metrics['rows_raw']:,}", "Training Rows", PALETTE["teal"]),
            (str(feature_count), "Features Used", PALETTE["blue"]),
        ],
    ):
        col.markdown(
            f"<div class='info-card' style='text-align:center;'>"
            f"<div style='font-size:1.7rem; font-weight:900; color:{color};'>{val}</div>"
            f"<div class='small-note'>{lbl}</div></div>",
            unsafe_allow_html=True,
        )

# ─── METRICS BAND ───
metrics_html = f"""
<div class="metric-band">
  <div style="display:grid; grid-template-columns: repeat(5, 1fr); gap:.5rem;">
    <div class="metric-item"><div class="metric-icon">📦</div><div class="metric-value">{runtime.metrics['rows_raw']:,}</div><div class="metric-label">Training Samples</div></div>
    <div class="metric-item"><div class="metric-icon">🎯</div><div class="metric-value">{runtime.metrics['r2']*100:.1f}%</div><div class="metric-label">R² Accuracy</div></div>
    <div class="metric-item"><div class="metric-icon">📉</div><div class="metric-value">{runtime.metrics['mae']:.3f}</div><div class="metric-label">Mean Abs. Error</div></div>
    <div class="metric-item"><div class="metric-icon">🧬</div><div class="metric-value">{feature_count}</div><div class="metric-label">Input Features</div></div>
   <div class="metric-item"><div class="metric-icon">🌲</div><div class="metric-value">100</div><div class="metric-label">Forest Trees</div></div>
  </div>
</div>
"""
st.markdown(metrics_html, unsafe_allow_html=True)

# ─── DATA OVERVIEW ───
st.markdown('<div style="text-align:center; margin-top:.5rem;"><span class="section-kicker">📁 Dataset Overview</span></div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Understanding the Data</div>', unsafe_allow_html=True)
st.markdown(
    f'<div class="section-copy">The dataset contains <strong>{runtime.metrics["rows_raw"]:,}</strong> agricultural records '
    f'spanning soil nutrients, temperature, and fertilizer dosage — processed with outlier removal and median imputation.</div>',
    unsafe_allow_html=True,
)


def render_feature_distribution_card(df: pd.DataFrame) -> str:
    rows_cfg = [
        ("🌿 Fertilizer", "fertilizer", "kg/ha"),
        ("🌡️ Temperature", "temp", "°C"),
        ("🧬 Nitrogen (N)", "n", "kg/ha"),
        ("🧂 Phosphorus (P)", "p", "kg/ha"),
        ("🪴 Potassium (K)", "k", "kg/ha"),
        ("🌾 Yield", "yield", "t/ha"),
    ]
    html = [
        f"<div class='section-card'>"
        f"<h3 style='margin:.1rem 0 1.3rem 0; color:{PALETTE['text']}; font-size:1.5rem; font-weight:800;'>📊 Feature Distributions</h3>"
    ]
    for label, col, unit in rows_cfg:
        mean_val = float(df[col].mean())
        max_val = float(df[col].max()) if float(df[col].max()) != 0 else 1.0
        percent = max(min((mean_val / max_val) * 100, 100), 0)
        html.append(
            f"<div class='feature-row'>"
            f"<div class='feature-head'><span style='font-weight:600;'>{label}</span>"
            f"<span style='font-size:.83rem; background:rgba(45,125,70,.09); padding:.2rem .6rem; border-radius:8px; font-weight:700; color:{PALETTE['green']};'>Avg {mean_val:.1f} {unit}</span></div>"
            f"<div class='feature-track'><div class='feature-fill' style='width:{percent:.1f}%'></div></div>"
            f"<div class='feature-foot'><span>0</span><span>Max {max_val:.0f} {unit}</span></div>"
            f"</div>"
        )
    html.append("</div>")
    return "".join(html)


def donut_figure(title: str, value: float, color: str) -> go.Figure:
    fig = go.Figure(
        go.Pie(
            values=[value, max(1 - value, 0)],
            hole=0.72,
            sort=False,
            marker=dict(colors=[color, "#E0EDE4"], line=dict(width=0)),
            textinfo="none",
        )
    )
    fig.update_layout(
        height=230,
        margin=dict(l=0, r=0, t=22, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        annotations=[dict(
            text=f"<b>{value*100:.1f}%</b><br>R²",
            showarrow=False,
            font=dict(size=16, color=PALETTE["text"]),
        )],
        title=dict(text=title, x=0.5, xanchor="center", font=dict(size=15, color=PALETTE["text"])),
        showlegend=False,
    )
    return fig


left_card, right_card = st.columns(2, gap="large")
with left_card:
    st.markdown(render_feature_distribution_card(runtime.processed_df), unsafe_allow_html=True)

with right_card:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(
        f"<h3 style='margin:.1rem 0 .3rem 0; color:{PALETTE['text']}; font-size:1.5rem; font-weight:800;'>🎯 Model Accuracy Comparison</h3>"
        f"<div class='small-note' style='margin-bottom:1rem;'>R² score on test data — comparing final model vs baseline.</div>",
        unsafe_allow_html=True,
    )
    d1, d2 = st.columns(2)
    final_r2 = runtime.model_comparison["Final Model"]["R2"]
    base_r2 = runtime.model_comparison["Baseline"]["R2"]
    with d1:
        st.plotly_chart(donut_figure("Final Model", final_r2, PALETTE["green_2"]), use_container_width=True, config={"displayModeBar": False})
        st.markdown(
            f"<div class='info-card' style='margin-top:.3rem; background: linear-gradient(135deg, #F0FBF4, #E8F5E4);'>"
            f"<div class='small-note'>Train R²</div>"
            f"<div style='font-weight:800; color:{PALETTE['green']}; font-size:1.1rem;'>{runtime.metrics['train_r2']:.3f}</div>"
            f"<div class='small-note'>MAE: {runtime.metrics['mae']:.3f} &nbsp;•&nbsp; RMSE: {runtime.metrics['rmse']:.3f}</div></div>",
            unsafe_allow_html=True,
        )
    with d2:
        st.plotly_chart(donut_figure("Baseline", base_r2, PALETTE["blue"]), use_container_width=True, config={"displayModeBar": False})
        st.markdown(
            f"<div class='info-card' style='margin-top:.3rem; background: linear-gradient(135deg, #EFF6FD, #E4EFFA);'>"
            f"<div class='small-note'>Test R²</div>"
            f"<div style='font-weight:800; color:{PALETTE['blue']}; font-size:1.1rem;'>{base_r2:.3f}</div>"
            f"<div class='small-note'>MAE: {runtime.model_comparison['Baseline']['MAE']:.3f} &nbsp;•&nbsp; RMSE: {runtime.model_comparison['Baseline']['RMSE']:.3f}</div></div>",
            unsafe_allow_html=True,
        )
    delta = (final_r2 - base_r2) * 100
    st.markdown(
        f"<div class='info-card' style='margin-top:.9rem; background:linear-gradient(135deg,#F0FBF4,#E8F5E4); border-color:{PALETTE['line']};'>"
        f"<strong style='color:{PALETTE['green']};'>🏆 +{delta:.1f}% improvement</strong>"
        f" <span class='small-note'>— Final model outperforms baseline on test R².</span></div>",
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ─── HOW IT WORKS ───
st.write("")
st.markdown('<div style="text-align:center; margin-top:1.5rem;"><span class="section-kicker">⚙️ Workflow</span></div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">How It Works</div>', unsafe_allow_html=True)
steps = [
    ("01", "🌱", "Enter Field Data", "Provide soil nutrient values (N, P, K), temperature, and fertilizer dosage from the sliders on the Predict page."),
    ("02", "⚙️", "Model Inference", "The existing backend pipeline processes the inputs and runs the trained Random Forest model with 100 estimators."),
    ("03", "📈", "Get Yield Estimate", "View the predicted crop yield in tons/hectare with a gauge chart, status label, and confidence metrics."),
]
step_cols = st.columns(3, gap="large")
for col, (idx, emoji, title, copy) in zip(step_cols, steps):
    with col:
        st.markdown(
            f'<div class="step-card"><div class="step-index">STEP {idx}</div>'
            f'<span class="step-emoji">{emoji}</span>'
            f'<div class="step-title">{title}</div>'
            f'<div class="step-copy">{copy}</div></div>',
            unsafe_allow_html=True,
        )

# ─── FOOTER ───
st.markdown('<div class="footer-band">', unsafe_allow_html=True)
f1, f2, f3 = st.columns([1, 1.5, 1])
with f2:
    st.markdown(
        f"<div style='font-size:1.3rem; font-weight:800; color:{PALETTE['text']}; margin-bottom:.5rem;'>Ready to predict your harvest? 🌾</div>"
        f"<div class='small-note' style='margin-bottom:1rem;'>Use the live prediction tool powered by the same backend pipeline.</div>",
        unsafe_allow_html=True,
    )
    st.page_link("pages/2_Predict.py", label="🔮 Start Predicting Now →", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
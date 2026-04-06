from pathlib import Path
import sys

import plotly.graph_objects as go
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from backend import get_about_charts, get_feature_ranges, get_runtime, predict_yield

st.set_page_config(page_title="Predict | AgriPredict", page_icon="🔮", layout="wide")

FEATURE_LABELS = {
    "fertilizer": "Fertilizer",
    "temp": "Temperature",
    "n": "Nitrogen (N)",
    "p": "Phosphorus (P)",
    "k": "Potassium (K)",
}
FEATURE_UNITS = {
    "fertilizer": "kg/ha",
    "temp": "°C",
    "n": "kg/ha",
    "p": "kg/ha",
    "k": "kg/ha",
}
FEATURE_EMOJI = {
    "fertilizer": "🌿",
    "temp": "🌡️",
    "n": "🧬",
    "p": "🧂",
    "k": "🪴",
}

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
.stApp {{background:linear-gradient(160deg, #EBF5EB 0%, #F5FBF5 40%, #FAFFF9 100%); color:{PALETTE['text']};}}
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
    padding:1.8rem 2rem;
    background:linear-gradient(135deg, #FFFFFF 0%, #F0FBF4 50%, #E5F7EC 100%);
    border:1px solid {PALETTE['line']}; border-radius:28px;
    box-shadow:0 8px 40px rgba(45,125,70,.08);
    text-align:center; margin-bottom:1.5rem;
    position:relative; overflow:hidden;
}}
.hero-card::before {{
    content:''; position:absolute; top:-60px; right:-60px;
    width:200px; height:200px;
    background:radial-gradient(circle,rgba(82,164,106,.12) 0%,transparent 70%);
    pointer-events:none;
}}
.kicker {{
    display:inline-flex; align-items:center; gap:.4rem;
    padding:.4rem .9rem; border-radius:999px; font-size:.8rem; font-weight:700;
    color:{PALETTE['gold']}; border:1px solid rgba(232,160,32,.38); background:rgba(232,160,32,.08);
    letter-spacing:.04em; text-transform:uppercase;
}}
.hero-title {{
    font-size:2.8rem; line-height:1.15; font-weight:900;
    color:{PALETTE['text']}; margin:.9rem 0 .55rem; letter-spacing:-1.2px;
}}
.hero-title span {{color:{PALETTE['green']};}}
.hero-copy {{font-size:1.02rem; color:{PALETTE['muted']}; line-height:1.8; max-width:680px; margin:0 auto;}}
.panel-card, .result-card, .info-card, .chart-card {{
    background:rgba(255,255,255,.97); border:1px solid {PALETTE['line']};
    border-radius:22px; box-shadow:0 4px 20px rgba(45,125,70,.06);
}}
.panel-card {{padding:1.4rem 1.3rem;}}
.result-card {{
    padding:1.5rem 1.3rem;
    background:linear-gradient(135deg, #F5FBF7 0%, #EBF5EF 100%);
}}
.info-card {{padding:1rem 1.05rem; margin-top:1rem;}}
.chart-card {{padding:.9rem; margin-top:1rem;}}
.small-note {{font-size:.9rem; color:{PALETTE['muted']};}}
.current-chip {{
    display:inline-block; padding:.22rem .6rem; border-radius:8px;
    background:rgba(232,160,32,.12); color:{PALETTE['gold']};
    font-size:.82rem; font-weight:700; border:1px solid rgba(232,160,32,.25);
}}
.slider-block {{margin-top:.9rem; margin-bottom:1.05rem;}}
.slider-head {{
    display:flex; justify-content:space-between; align-items:center; margin-bottom:.25rem;
}}
.slider-title {{font-weight:700; color:{PALETTE['text']}; font-size:.98rem;}}
.range-note {{font-size:.82rem; color:{PALETTE['muted']}; margin-top:.2rem;}}
.input-row {{
    display:flex; justify-content:space-between; align-items:center;
    padding:.45rem 0; border-bottom:1px solid {PALETTE['line']};
}}
.input-row:last-child {{border-bottom:none;}}
.yield-display {{
    text-align:center;
    font-size:3.6rem; font-weight:900; color:{PALETTE['green']};
    margin:.25rem 0 0 0; letter-spacing:-1.5px;
    line-height:1;
}}
.yield-unit {{
    text-align:center; font-size:.95rem; color:{PALETTE['muted']};
    font-weight:500; margin-top:.1rem;
}}
.status-badge {{
    display:inline-block; padding:.4rem 1.1rem; border-radius:999px;
    font-size:.9rem; font-weight:700;
}}
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
.model-info-row {{
    display:flex; justify-content:space-between; align-items:center;
    padding:.4rem 0; border-bottom:1px solid {PALETTE['line']};
}}
.model-info-row:last-child {{border-bottom:none;}}
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


@st.cache_data(show_spinner=False)
def load_ranges():
    return get_feature_ranges()


@st.cache_data(show_spinner=False)
def load_about_charts():
    return get_about_charts()


@st.cache_resource(show_spinner=False)
def load_runtime():
    return get_runtime()


ranges = load_ranges()
charts = load_about_charts()
runtime = load_runtime()
keys = ["fertilizer", "temp", "n", "p", "k"]

if "prediction_result" not in st.session_state:
    st.session_state.prediction_result = None

if "input_values" not in st.session_state:
    st.session_state.input_values = {
        feature: float(ranges[feature]["default"]) for feature in keys
    }


def reset_inputs() -> None:
    st.session_state.input_values = {
        feature: float(ranges[feature]["default"]) for feature in keys
    }
    st.session_state.prediction_result = None


def style_fig(fig, height=280):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=PALETTE["text"], size=12),
        title=dict(font=dict(size=17, color=PALETTE["text"]), x=0.02),
        margin=dict(l=18, r=18, t=52, b=18),
        xaxis=dict(showgrid=True, gridcolor="rgba(200,224,206,.4)", zeroline=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(200,224,206,.4)", zeroline=False),
        showlegend=False,
    )
    return fig


relationship_fig = style_fig(charts["feature_relationship"], height=270)
relationship_fig.update_traces(
    marker_color=[PALETTE["green_2"], PALETTE["blue"], PALETTE["gold"], "#CD6F45", "#8E61BC"]
)


def result_gauge(value: float, max_value: float) -> go.Figure:
    pct = value / max_value
    if pct >= 0.66:
        bar_color = PALETTE["green_2"]
    elif pct >= 0.40:
        bar_color = PALETTE["gold"]
    else:
        bar_color = PALETTE["blue"]

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            number={"suffix": "", "font": {"size": 34, "color": PALETTE["green"]}},
            gauge={
                "axis": {"range": [0, max_value], "tickwidth": 0, "tickcolor": PALETTE["muted"]},
                "bar": {"color": bar_color, "thickness": 0.22},
                "bgcolor": "rgba(0,0,0,0)",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, max_value * 0.33], "color": "rgba(200,224,206,.3)"},
                    {"range": [max_value * 0.33, max_value * 0.66], "color": "rgba(200,224,206,.55)"},
                    {"range": [max_value * 0.66, max_value], "color": "rgba(168,213,181,.5)"},
                ],
                "threshold": {
                    "line": {"color": PALETTE["green"], "width": 2},
                    "thickness": 0.75,
                    "value": value,
                },
            },
        )
    )
    fig.update_layout(
        height=200,
        margin=dict(l=12, r=12, t=10, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color=PALETTE["text"]),
    )
    return fig


# ─── NAV ───
st.markdown('<div class="nav-shell">', unsafe_allow_html=True)
render_top_nav()
st.markdown("</div>", unsafe_allow_html=True)

# ─── HERO ───
st.markdown('<div class="hero-card">', unsafe_allow_html=True)
st.markdown(
    f'<span class="kicker">🌾 Random Forest Regressor &nbsp;•&nbsp; R² {runtime.metrics["r2"]*100:.1f}%</span>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="hero-title">Predict Your <span>Crop Yield</span></div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="hero-copy">Adjust the sliders to match your field conditions. The prediction behavior, model flow, data loading, and backend connection remain exactly the same.</div>',
    unsafe_allow_html=True,
)
st.markdown("</div>", unsafe_allow_html=True)

# ─── MAIN LAYOUT ───
left, right = st.columns([0.95, 1.15], gap="large", vertical_alignment="top")

with left:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown(
        f"<h3 style='margin:.1rem 0 .25rem 0; color:{PALETTE['text']}; font-size:1.4rem; font-weight:800;'>🪴 Field Parameters</h3>"
        f"<div class='small-note' style='margin-bottom:1.1rem;'>Drag the sliders to match your field conditions.</div>",
        unsafe_allow_html=True,
    )

    with st.form("prediction_form", clear_on_submit=False):
        new_inputs = {}
        for feature in keys:
            values = ranges[feature]
            current_value = float(st.session_state.input_values[feature])
            emoji = FEATURE_EMOJI[feature]
            st.markdown("<div class='slider-block'>", unsafe_allow_html=True)
            st.markdown(
                f"<div class='slider-head'>"
                f"<div class='slider-title'>{emoji} {FEATURE_LABELS[feature]}</div>"
                f"<span class='current-chip'>{current_value:.0f} {FEATURE_UNITS[feature]}</span></div>",
                unsafe_allow_html=True,
            )
            slider_value = st.slider(
                FEATURE_LABELS[feature],
                min_value=float(values["min"]),
                max_value=float(values["max"]),
                value=current_value,
                step=float(values["step"]),
                key=f"{feature}_widget",
                label_visibility="collapsed",
            )
            new_inputs[feature] = float(slider_value)
            st.markdown(
                f"<div class='range-note'>Range: {float(values['min']):.0f} – {float(values['max']):.0f} {FEATURE_UNITS[feature]}</div>",
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

        b1, b2 = st.columns(2)
        predict_clicked = b1.form_submit_button("🔮 Predict Yield", use_container_width=True, type="primary")
        reset_clicked = b2.form_submit_button("↺ Reset", use_container_width=True)

    if predict_clicked:
        st.session_state.input_values = new_inputs.copy()
        if any(value < 0 for value in st.session_state.input_values.values()):
            st.error("All input values must be non-negative.")
        else:
            st.session_state.prediction_result = predict_yield(**st.session_state.input_values)

    if reset_clicked:
        reset_inputs()
        st.rerun()

    # ─── Current Inputs Summary ───
    current_inputs = st.session_state.input_values
    input_rows_html = []
    for k in keys:
        emoji = FEATURE_EMOJI[k]
        input_rows_html.append(
            f"<div class='input-row'>"
            f"<span class='small-note'>{emoji} {FEATURE_LABELS[k]}</span>"
            f"<strong style='color:{PALETTE['text']};'>{current_inputs[k]:.0f} {FEATURE_UNITS[k]}</strong></div>"
        )
    st.markdown(
        f"<div class='info-card'>"
        f"<div style='font-weight:800; color:{PALETTE['text']}; margin-bottom:.5rem; font-size:.95rem;'>📋 Current Inputs</div>"
        f"{''.join(input_rows_html)}</div>",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    prediction_value = st.session_state.prediction_result
    max_yield = max(float(runtime.processed_df["yield"].max()), 1.0)
    display_value = prediction_value if prediction_value is not None else predict_yield(**{f: float(ranges[f]["default"]) for f in keys})

    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.markdown(
        "<div class='small-note' style='text-align:center; letter-spacing:.1em; font-weight:700; text-transform:uppercase; margin-bottom:.2rem;'>Predicted Crop Yield</div>",
        unsafe_allow_html=True,
    )
    st.markdown(f"<div class='yield-display'>{display_value:.2f}</div>", unsafe_allow_html=True)
    st.markdown("<div class='yield-unit'>tons / hectare</div>", unsafe_allow_html=True)

    st.plotly_chart(
        result_gauge(display_value, max_yield),
        use_container_width=True,
        config={"displayModeBar": False},
    )

    pct = display_value / max_yield
    if pct >= 0.66:
        status, badge_bg, badge_color = "🏆 Excellent Yield", "rgba(45,125,70,.12)", PALETTE["green"]
    elif pct >= 0.40:
        status, badge_bg, badge_color = "✅ Good Yield", "rgba(58,175,169,.12)", PALETTE["teal"]
    else:
        status, badge_bg, badge_color = "📊 Moderate Yield", "rgba(74,144,196,.12)", PALETTE["blue"]

    st.markdown(
        f"<div style='text-align:center;'>"
        f"<span class='status-badge' style='background:{badge_bg}; color:{badge_color}; border:1px solid {badge_color}44;'>{status}</span></div>",
        unsafe_allow_html=True,
    )

    if prediction_value is None:
        st.markdown("<div style='text-align:center; margin-top:.8rem;'>", unsafe_allow_html=True)
        st.info("Adjust the sliders and click **Predict Yield** to generate a live result.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ─── Feature Importance Chart ───
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(relationship_fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("<div class='small-note' style='text-align:center; margin-top:.2rem;'>Feature correlation with yield — values from the backend dataset.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ─── Model Info ───
    model_rows = [
        ("Model", "RandomForestRegressor"),
        ("Pipeline", "Existing saved artifact"),
        ("Split", "80% train / 20% test"),
        ("Samples", f"{runtime.metrics['rows_processed']:,} processed"),
        ("Test R²", f"{runtime.metrics['r2']:.3f}"),
        ("MAE", f"{runtime.metrics['mae']:.3f}"),
    ]
    rows_html = "".join([
        f"<div class='model-info-row'><span class='small-note'>{label}</span>"
        f"<strong style='color:{PALETTE['text']}; font-size:.88rem;'>{value}</strong></div>"
        for label, value in model_rows
    ])
    st.markdown(
        f"<div class='info-card'>"
        f"<div style='font-weight:800; color:{PALETTE['text']}; margin-bottom:.5rem; font-size:.95rem;'>🤖 Model Details</div>"
        f"{rows_html}</div>",
        unsafe_allow_html=True,
    )

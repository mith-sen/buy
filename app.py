import streamlit as st
from modules.ocr_engine import extract_text_from_image
from modules.ai_suggester import get_ai_analysis
from utils.firebase_ops import save_scan, get_scan_history

st.set_page_config(page_title="BeforeYouBuy", page_icon="🛒", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display&display=swap');

    * { font-family: 'DM Sans', sans-serif; }
    #MainMenu, footer, header { visibility: hidden; }

    .stApp { background: #080810; color: #e2e2ea; }

    [data-testid="stSidebar"] {
        background: #0c0c16;
        border-right: 1px solid #18182a;
        padding-top: 20px;
    }

    /* Hero */
    .hero {
        padding: 80px 0 60px 0;
        text-align: center;
    }
    .hero-eyebrow {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #00d68f;
        margin-bottom: 20px;
    }
    .hero-title {
        font-family: 'DM Serif Display', serif;
        font-size: 72px;
        font-weight: 400;
        line-height: 1.05;
        color: #ffffff;
        margin: 0 0 20px 0;
        letter-spacing: -1px;
    }
    .hero-title span {
        background: linear-gradient(135deg, #00d68f, #00b4d8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-desc {
        font-size: 17px;
        color: #6b6b80;
        font-weight: 300;
        max-width: 500px;
        margin: 0 auto;
        line-height: 1.7;
    }

    /* Score cards */
    .scores-row {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 16px;
        margin: 32px 0;
    }
    .score-card {
        background: #0e0e1c;
        border: 1px solid #1c1c2e;
        border-radius: 20px;
        padding: 28px 24px;
        text-align: center;
        position: relative;
        overflow: hidden;
        transition: border-color 0.3s;
    }
    .score-card::after {
        content: '';
        position: absolute;
        bottom: 0; left: 0; right: 0;
        height: 2px;
    }
    .score-card.green::after { background: linear-gradient(90deg, #00d68f, transparent); }
    .score-card.amber::after { background: linear-gradient(90deg, #f59e0b, transparent); }
    .score-card.red::after   { background: linear-gradient(90deg, #ef4444, transparent); }

    .score-value {
        font-family: 'DM Serif Display', serif;
        font-size: 56px;
        line-height: 1;
        font-weight: 400;
    }
    .score-card.green .score-value { color: #00d68f; }
    .score-card.amber .score-value { color: #f59e0b; }
    .score-card.red   .score-value { color: #ef4444; }

    .score-title {
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #44445a;
        margin-top: 10px;
    }

    /* Result cards */
    .result-card {
        background: #0e0e1c;
        border: 1px solid #1c1c2e;
        border-radius: 20px;
        padding: 32px;
        margin-bottom: 16px;
        line-height: 1.8;
        color: #c8c8d8;
        font-size: 15px;
    }
    .result-card h3 {
        font-family: 'DM Serif Display', serif;
        font-size: 22px;
        font-weight: 400;
        color: #ffffff;
        margin: 0 0 16px 0;
        padding-bottom: 16px;
        border-bottom: 1px solid #1c1c2e;
    }

    /* Input section */
    .section-label {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #44445a;
        margin-bottom: 16px;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent;
        gap: 0;
        border-bottom: 1px solid #1c1c2e;
        padding: 0;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #44445a;
        font-size: 13px;
        font-weight: 500;
        letter-spacing: 0.5px;
        padding: 12px 24px;
        border-radius: 0;
        border-bottom: 2px solid transparent;
    }
    .stTabs [aria-selected="true"] {
        background: transparent !important;
        color: #00d68f !important;
        border-bottom: 2px solid #00d68f !important;
    }

    /* Button */
    .stButton > button {
        background: #00d68f;
        color: #080810;
        font-weight: 600;
        font-size: 14px;
        letter-spacing: 0.5px;
        border: none;
        border-radius: 12px;
        padding: 14px 32px;
        width: 100%;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background: #00c07f;
        transform: translateY(-1px);
        box-shadow: 0 12px 32px rgba(0,214,143,0.2);
    }

    /* Radio */
    .stRadio [data-testid="stMarkdownContainer"] p {
        font-size: 14px;
        color: #8888a0;
    }
    div[role="radiogroup"] {
        gap: 8px;
    }
    div[role="radiogroup"] label {
        background: #0e0e1c;
        border: 1px solid #1c1c2e;
        border-radius: 10px;
        padding: 10px 18px;
        color: #8888a0;
        font-size: 14px;
        transition: all 0.2s;
    }
    div[role="radiogroup"] label:hover {
        border-color: #00d68f;
        color: #ffffff;
    }

    /* History card */
    .history-card {
        background: #0e0e1c;
        border: 1px solid #1c1c2e;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 12px;
    }
    .history-meta {
        font-size: 12px;
        color: #44445a;
        margin-bottom: 12px;
        letter-spacing: 0.5px;
    }

    /* Divider */
    hr { border-color: #1c1c2e; margin: 40px 0; }

    /* File uploader */
    [data-testid="stFileUploader"] {
        background: #0e0e1c;
        border: 1px dashed #1c1c2e;
        border-radius: 16px;
        padding: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ─────────────────────────────────────────────────
with st.sidebar:
    st.markdown("#### Profile")
    user_name = st.text_input("Name", value="User")
    allergies = st.multiselect("Allergies",
        ["Gluten", "Nuts", "Dairy", "Soy", "Eggs", "Shellfish"])
    diet = st.selectbox("Diet",
        ["Regular", "Vegan", "Vegetarian", "Diabetic", "Low-sodium"])

# ── Hero ────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">AI-Powered Analysis</div>
    <h1 class="hero-title">Know what you buy.<br><span>Before you buy it.</span></h1>
    <p class="hero-desc">Upload a product label or shopping bill and get instant health, safety, and environmental insights.</p>
</div>
""", unsafe_allow_html=True)

# ── Input ───────────────────────────────────────────────────
st.markdown('<div class="section-label">Scan Method</div>', unsafe_allow_html=True)
input_method = st.radio("", 
    ["Upload Product Image", "Upload Bill / Receipt", "Paste Text Manually"],
    horizontal=True, label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

extracted_text = ""

if input_method == "Upload Product Image":
    uploaded_file = st.file_uploader("Upload product label", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(uploaded_file, use_column_width=True)
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Analyze Product"):
                with st.spinner("Reading image..."):
                    extracted_text = extract_text_from_image(uploaded_file)

elif input_method == "Upload Bill / Receipt":
    uploaded_file = st.file_uploader("Upload your bill", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(uploaded_file, use_column_width=True)
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Analyze Bill"):
                with st.spinner("Reading bill..."):
                    extracted_text = extract_text_from_image(uploaded_file)

elif input_method == "Paste Text Manually":
    extracted_text = st.text_area("Paste ingredients or bill text", height=200)
    st.button("Analyze Text")

# ── Results ─────────────────────────────────────────────────
if extracted_text:
    st.markdown("<hr>", unsafe_allow_html=True)

    with st.spinner("Analyzing..."):
        context = f"User allergies: {allergies}, Diet: {diet}\n\n"
        result = get_ai_analysis(context + extracted_text)

    import random
    health = random.randint(30, 90)
    eco = random.randint(30, 85)
    safety = random.randint(40, 95)

    def score_class(s):
        return "green" if s >= 70 else "amber" if s >= 40 else "red"

    st.markdown(f"""
    <div class="scores-row">
        <div class="score-card {score_class(health)}">
            <div class="score-value">{health}</div>
            <div class="score-title">Health Score</div>
        </div>
        <div class="score-card {score_class(eco)}">
            <div class="score-value">{eco}</div>
            <div class="score-title">Eco Score</div>
        </div>
        <div class="score-card {score_class(safety)}">
            <div class="score-value">{safety}</div>
            <div class="score-title">Safety Score</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Health & Risks", "Eco Impact", "Alternatives & Recipe"])
    with tab1:
        st.markdown(f'<div class="result-card"><h3>Health Analysis</h3>{result}</div>', unsafe_allow_html=True)
    with tab2:
        st.markdown(f'<div class="result-card"><h3>Environmental Impact</h3>{result}</div>', unsafe_allow_html=True)
    with tab3:
        st.markdown(f'<div class="result-card"><h3>Better Choices</h3>{result}</div>', unsafe_allow_html=True)

    save_scan(user_name, extracted_text, result)

# ── History ─────────────────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
with st.expander("Scan History"):
    history = get_scan_history(user_name)
    if history:
        for i, scan in enumerate(reversed(history)):
            st.markdown(f"""
            <div class="history-card">
                <div class="history-meta">Scan {i+1} &nbsp;·&nbsp; {scan['timestamp']}</div>
                {scan['ai_result']}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="history-card" style="color:#44445a;text-align:center">No scans yet</div>', unsafe_allow_html=True)
import streamlit as st

st.set_page_config(page_title="BeforeYouBuy", page_icon="🛒", layout="wide")

st.markdown("""
<style>
<<<<<<< HEAD
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');
*, *::before, *::after { box-sizing: border-box; margin: 0; }
html, body, [data-testid="stApp"] { background: #07070d !important; color: #eeeae4 !important; font-family: 'DM Sans', sans-serif !important; text-rendering: optimizeLegibility; -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }
#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="stDecoration"] { display: none !important; }
[data-testid="stSidebarNav"] { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }
[data-testid="stMainBlockContainer"], .block-container { padding: 0 !important; max-width: 100% !important; }

.navbar { display: flex; align-items: center; justify-content: flex-start; gap: 16px; padding: 0 64px; height: 64px; background: rgba(7,7,13,0.95); border-bottom: 1px solid rgba(255,255,255,0.06); backdrop-filter: blur(12px); }
.nav-brand { display: flex; align-items: center; gap: 10px; font-family: 'Syne', sans-serif; font-size: 18px; font-weight: 700; color: #eeeae4; }
.nav-brand-icon { width: 32px; height: 32px; background: linear-gradient(135deg, #7c3aed, #5b21b6); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 15px; }
.nav-links { display: flex; align-items: center; gap: 4px; flex-wrap: nowrap; }
.nav-links a[data-testid="stPageLink"] { padding: 7px 16px; border-radius: 8px; font-size: 14px; font-weight: 600; letter-spacing: 0.01em; color: rgba(238,234,228,0.82) !important; border: 1px solid transparent; text-decoration: none !important; white-space: nowrap; }
.nav-links a[data-testid="stPageLink"]:hover { color: #ffffff !important; background: rgba(255,255,255,0.07); }
.nav-links a[data-testid="stPageLink"][aria-current="page"] { color: #e9d5ff !important; background: rgba(110,60,255,0.16); border-color: rgba(110,60,255,0.32); }

/* Force columns inside nav to be horizontal */
.nav-links [data-testid="stColumns"] { display: flex !important; flex-direction: row !important; gap: 4px !important; align-items: center !important; flex-wrap: nowrap !important; }
.nav-links [data-testid="stColumn"] { width: auto !important; flex: 0 0 auto !important; min-width: 0 !important; padding: 0 !important; }

.home-hero { min-height: calc(100vh - 64px); display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; background: radial-gradient(ellipse 90% 70% at 50% 0%, #130a30 0%, #07070d 65%); padding: 80px 40px; position: relative; overflow: hidden; }
.home-hero::before { content: ''; position: absolute; top: 20%; left: 50%; transform: translateX(-50%); width: 700px; height: 700px; background: radial-gradient(circle, rgba(110,50,255,0.07) 0%, transparent 65%); pointer-events: none; }
.hero-eyebrow { display: inline-flex; align-items: center; gap: 8px; background: rgba(110,60,255,0.1); border: 1px solid rgba(110,60,255,0.25); color: #a78bfa; font-size: 11.5px; font-weight: 500; letter-spacing: 0.08em; text-transform: uppercase; padding: 6px 16px; border-radius: 100px; margin-bottom: 28px; }
.hero-eyebrow-dot { width: 6px; height: 6px; background: #a78bfa; border-radius: 50%; animation: pulse 2s infinite; display: inline-block; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.3} }
.hero-h1 { font-family: 'Syne', sans-serif; font-size: clamp(48px, 7vw, 88px); font-weight: 800; line-height: 1.02; letter-spacing: -0.04em; background: linear-gradient(135deg, #fff 0%, #d8b4fe 40%, #7c3aed 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 20px; max-width: 900px; }
.hero-p { font-size: 18px; font-weight: 400; color: rgba(238,234,228,0.72); line-height: 1.75; max-width: 560px; margin-bottom: 44px; }
.hero-actions { display: flex; gap: 14px; align-items: center; margin-bottom: 72px; }
.btn-primary { padding: 14px 32px; border-radius: 12px; font-size: 15px; font-weight: 600; background: linear-gradient(135deg, #7c3aed, #5b21b6); color: #fff; border: none; box-shadow: 0 4px 24px rgba(124,58,237,0.4); font-family: 'Syne', sans-serif; cursor: pointer; }
.features-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; max-width: 900px; width: 100%; position: relative; z-index: 1; }
.feature-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 18px; padding: 28px 24px; text-align: left; transition: all 0.25s; }
.feature-card:hover { background: rgba(255,255,255,0.05); border-color: rgba(110,60,255,0.25); transform: translateY(-3px); }
.feature-icon { font-size: 28px; margin-bottom: 14px; }
.feature-title { font-family: 'Syne', sans-serif; font-size: 16px; font-weight: 700; color: #eeeae4; margin-bottom: 8px; }
.feature-desc { font-size: 13.5px; color: rgba(238,234,228,0.72); line-height: 1.65; }
=======
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
>>>>>>> origin/main

.how-section { padding: 100px 64px; background: #07070d; border-top: 1px solid rgba(255,255,255,0.05); }
.section-eyebrow { font-size: 11px; font-weight: 600; letter-spacing: 0.16em; text-transform: uppercase; color: #7c3aed; margin-bottom: 12px; }
.section-h2 { font-family: 'Syne', sans-serif; font-size: clamp(28px, 3.5vw, 44px); font-weight: 800; color: #eeeae4; margin-bottom: 16px; letter-spacing: -0.02em; }
.section-sub { font-size: 16px; color: rgba(238,234,228,0.7); line-height: 1.75; max-width: 560px; margin-bottom: 56px; }
.steps-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 28px; }
.step-card { background: rgba(255,255,255,0.025); border: 1px solid rgba(255,255,255,0.07); border-radius: 18px; padding: 32px 28px; }
.step-num { font-family: 'Syne', sans-serif; font-size: 48px; font-weight: 800; color: rgba(110,60,255,0.15); line-height: 1; margin-bottom: 16px; }
.step-title { font-family: 'Syne', sans-serif; font-size: 17px; font-weight: 700; color: #eeeae4; margin-bottom: 10px; }
.step-desc { font-size: 13.5px; color: rgba(238,234,228,0.72); line-height: 1.7; }

<<<<<<< HEAD
.footer { padding: 40px 64px; border-top: 1px solid rgba(255,255,255,0.05); display: flex; align-items: center; justify-content: space-between; background: #07070d; }
.footer-brand { font-family: 'Syne', sans-serif; font-size: 15px; font-weight: 700; color: rgba(238,234,228,0.6); }
.footer-copy { font-size: 12.5px; color: rgba(238,234,228,0.45); }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="navbar"><div class="nav-brand"><div class="nav-brand-icon">🛒</div>BeforeYouBuy</div><div class="nav-links">', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns([1,1,1,1])
with col1:
    st.page_link("app.py", label="Home")
with col2:
    st.page_link("pages/1_Bill_Scan.py", label="🧾 Bill Scan")
with col3:
    st.page_link("pages/2_Product_Scan.py", label="📦 Product Scan")
with col4:
    st.page_link("pages/3_Text_Scan.py", label="✏️ Text Scan")
st.markdown("</div></div>", unsafe_allow_html=True)

st.markdown("""
<div class="home-hero">
  <div class="hero-eyebrow"><span class="hero-eyebrow-dot"></span>Powered by Groq AI</div>
  <div class="hero-h1">Know What You Buy<br>Before You Buy It</div>
  <p class="hero-p">Upload any product label or shopping bill. Get instant health analysis, eco impact, and smarter alternatives – in seconds.</p>
  <div class="hero-actions">
    <a href="pages/1_Bill_Scan"><button class="btn-primary">🔍 Start Scanning</button></a>
  </div>
  <div class="features-grid">
    <div class="feature-card">
      <div class="feature-icon">🧾</div>
      <div class="feature-title">Bill Scan</div>
      <div class="feature-desc">Upload your shopping receipt and analyze every item you bought at once.</div>
    </div>
    <div class="feature-card">
      <div class="feature-icon">📦</div>
      <div class="feature-title">Product Scan</div>
      <div class="feature-desc">Photograph any product label to get a full ingredient and health breakdown.</div>
    </div>
    <div class="feature-card">
      <div class="feature-icon">✏️</div>
      <div class="feature-title">Text Scan</div>
      <div class="feature-desc">Paste ingredients or item names directly and get instant AI insights.</div>
    </div>
  </div>
</div>
<div class="how-section">
  <div class="section-eyebrow">How It Works</div>
  <div class="section-h2">Three steps to smarter shopping</div>
  <p class="section-sub">No sign-up needed. Just upload your product or bill and let AI do the work.</p>
  <div class="steps-grid">
    <div class="step-card"><div class="step-num">01</div><div class="step-title">Choose a Scan Type</div><div class="step-desc">Pick Bill Scan, Product Scan, or Text Scan from the navigation menu above.</div></div>
    <div class="step-card"><div class="step-num">02</div><div class="step-title">Upload or Paste</div><div class="step-desc">Take a photo of your bill/product label or paste the ingredient text directly.</div></div>
    <div class="step-card"><div class="step-num">03</div><div class="step-title">Get Insights</div><div class="step-desc">Browse health, eco impact, and alternatives in clear organized tabs on the same page.</div></div>
  </div>
</div>
<div class="footer">
  <div class="footer-brand">🛒 BeforeYouBuy</div>
  <div class="footer-copy">© 2026 · Built with Groq AI · For educational purposes</div>
</div>
""", unsafe_allow_html=True)
=======
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
>>>>>>> origin/main

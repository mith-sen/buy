import streamlit as st
from modules.ocr_engine import extract_text_from_image
from modules.ai_suggester import get_ai_analysis
from utils.firebase_ops import save_scan, get_scan_history

# ─── Page Config ───────────────────────────────────────────
st.set_page_config(
    page_title="BeforeYouBuy",
    page_icon="🛒",
    layout="wide"
)

# ─── Custom CSS ────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Syne:wght@700;800&display=swap');

    * { font-family: 'Space Grotesk', sans-serif; }

    .stApp {
        background: #0a0a0f;
        color: #e8e8f0;
    }

    /* Hide Streamlit branding */
    #MainMenu, footer, header { visibility: hidden; }

    /* Hero Section */
    .hero {
        background: linear-gradient(135deg, #0d0d1a 0%, #0a1628 50%, #0d1a0d 100%);
        border: 1px solid #1a1a2e;
        border-radius: 24px;
        padding: 60px 40px;
        text-align: center;
        margin-bottom: 40px;
        position: relative;
        overflow: hidden;
    }
    .hero::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle at 30% 50%, rgba(0,200,83,0.05) 0%, transparent 50%),
                    radial-gradient(circle at 70% 50%, rgba(0,100,255,0.05) 0%, transparent 50%);
        animation: pulse 8s ease-in-out infinite;
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 1; }
    }
    .hero-title {
        font-family: 'Syne', sans-serif;
        font-size: 64px;
        font-weight: 800;
        background: linear-gradient(135deg, #00c853, #00e5ff, #00c853);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 3s linear infinite;
        margin: 0;
        line-height: 1.1;
    }
    @keyframes shine {
        0% { background-position: 0% center; }
        100% { background-position: 200% center; }
    }
    .hero-subtitle {
        font-size: 18px;
        color: #6b7280;
        margin-top: 16px;
        font-weight: 300;
        letter-spacing: 0.5px;
    }
    .hero-badge {
        display: inline-block;
        background: rgba(0,200,83,0.1);
        border: 1px solid rgba(0,200,83,0.3);
        color: #00c853;
        padding: 6px 16px;
        border-radius: 100px;
        font-size: 13px;
        font-weight: 500;
        margin-bottom: 20px;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    /* Cards */
    .card {
        background: #111118;
        border: 1px solid #1e1e2e;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 16px;
        transition: border-color 0.3s;
    }
    .card:hover { border-color: #00c853; }

    /* Health Score */
    .score-container {
        text-align: center;
        padding: 30px;
        border-radius: 16px;
        margin: 10px 0;
    }
    .score-high {
        background: linear-gradient(135deg, rgba(0,200,83,0.1), rgba(0,200,83,0.05));
        border: 1px solid rgba(0,200,83,0.3);
    }
    .score-medium {
        background: linear-gradient(135deg, rgba(255,165,0,0.1), rgba(255,165,0,0.05));
        border: 1px solid rgba(255,165,0,0.3);
    }
    .score-low {
        background: linear-gradient(135deg, rgba(255,50,50,0.1), rgba(255,50,50,0.05));
        border: 1px solid rgba(255,50,50,0.3);
    }
    .score-number {
        font-family: 'Syne', sans-serif;
        font-size: 72px;
        font-weight: 800;
        line-height: 1;
    }
    .score-high .score-number { color: #00c853; }
    .score-medium .score-number { color: #ffa500; }
    .score-low .score-number { color: #ff3232; }
    .score-label {
        font-size: 14px;
        color: #6b7280;
        margin-top: 8px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: #111118;
        border-radius: 12px;
        padding: 4px;
        gap: 4px;
        border: 1px solid #1e1e2e;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: #6b7280;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background: #00c853 !important;
        color: #000 !important;
    }

    /* Upload area */
    .stFileUploader {
        background: #111118;
        border: 2px dashed #1e1e2e;
        border-radius: 16px;
        padding: 20px;
    }
    .stFileUploader:hover {
        border-color: #00c853;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #00c853, #00a846);
        color: #000;
        font-weight: 600;
        border: none;
        border-radius: 12px;
        padding: 12px 32px;
        font-size: 15px;
        letter-spacing: 0.5px;
        transition: all 0.3s;
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,200,83,0.3);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #0d0d14;
        border-right: 1px solid #1e1e2e;
    }

    /* Radio buttons */
    .stRadio > div {
        background: #111118;
        border-radius: 12px;
        padding: 16px;
        border: 1px solid #1e1e2e;
        gap: 8px;
    }

    /* Loading animation */
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    /* Result section */
    .result-header {
        font-family: 'Syne', sans-serif;
        font-size: 28px;
        font-weight: 700;
        color: #e8e8f0;
        margin-bottom: 24px;
    }

    /* Divider */
    hr { border-color: #1e1e2e; }
</style>
""", unsafe_allow_html=True)

# ─── Hero Section ──────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">⚡ AI Powered</div>
    <h1 class="hero-title">BeforeYouBuy</h1>
    <p class="hero-subtitle">Scan any product or bill — get instant health risks, eco impact & smarter alternatives</p>
</div>
""", unsafe_allow_html=True)

# ─── Sidebar ───────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 👤 Your Profile")
    user_name = st.text_input("Name", value="User")
    allergies = st.multiselect("Known Allergies",
        ["Gluten", "Nuts", "Dairy", "Soy", "Eggs", "Shellfish"])
    diet = st.selectbox("Diet Type",
        ["Regular", "Vegan", "Vegetarian", "Diabetic", "Low-sodium"])
    st.divider()
    st.markdown("<small style='color:#6b7280'>Your preferences personalize the AI analysis</small>", unsafe_allow_html=True)

# ─── Input Method ──────────────────────────────────────────
st.markdown("#### 📤 Choose how to scan")
input_method = st.radio("", 
    ["📷 Upload Product Image", "🧾 Upload Bill / Receipt", "✍️ Paste Text Manually"],
    horizontal=True, label_visibility="collapsed")

st.divider()

extracted_text = ""

# ─── Image Upload ──────────────────────────────────────────
if input_method == "📷 Upload Product Image":
    uploaded_file = st.file_uploader("Drop your product label image here", 
        type=["jpg", "jpeg", "png"])
    if uploaded_file:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(uploaded_file, caption="Uploaded", use_column_width=True)
        with col2:
            st.markdown("<br><br>", unsafe_allow_html=True)
            if st.button("🔍 Analyze Product"):
                with st.spinner("🤖 Reading your product..."):
                    extracted_text = extract_text_from_image(uploaded_file)
                st.success("✅ Done!")

elif input_method == "🧾 Upload Bill / Receipt":
    uploaded_file = st.file_uploader("Drop your shopping bill here",
        type=["jpg", "jpeg", "png"])
    if uploaded_file:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(uploaded_file, caption="Bill", use_column_width=True)
        with col2:
            st.markdown("<br><br>", unsafe_allow_html=True)
            if st.button("🔍 Analyze Bill"):
                with st.spinner("🤖 Reading your bill..."):
                    extracted_text = extract_text_from_image(uploaded_file)
                st.success("✅ Done!")

elif input_method == "✍️ Paste Text Manually":
    extracted_text = st.text_area("Paste ingredients or bill text here", height=200)
    st.button("🔍 Analyze Text")

# ─── AI Analysis Results ───────────────────────────────────
if extracted_text:
    st.divider()
    st.markdown('<div class="result-header">📊 Analysis Results</div>', unsafe_allow_html=True)

    with st.spinner("🧠 AI is analyzing..."):
        context = f"User allergies: {allergies}, Diet: {diet}\n\n"
        result = get_ai_analysis(context + extracted_text)

    # Health Score (random for now, can be parsed from AI later)
    import random
    score = random.randint(30, 90)
    score_class = "score-high" if score >= 70 else "score-medium" if score >= 40 else "score-low"
    score_emoji = "✅" if score >= 70 else "⚠️" if score >= 40 else "❌"

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="score-container {score_class}">
            <div class="score-number">{score}</div>
            <div class="score-label">{score_emoji} Health Score</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        eco = random.randint(30, 85)
        eco_class = "score-high" if eco >= 70 else "score-medium" if eco >= 40 else "score-low"
        st.markdown(f"""
        <div class="score-container {eco_class}">
            <div class="score-number">{eco}</div>
            <div class="score-label">🌍 Eco Score</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        safety = random.randint(40, 95)
        safety_class = "score-high" if safety >= 70 else "score-medium" if safety >= 40 else "score-low"
        st.markdown(f"""
        <div class="score-container {safety_class}">
            <div class="score-number">{safety}</div>
            <div class="score-label">🛡️ Safety Score</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Results in tabs
    tab1, tab2, tab3 = st.tabs(["🥗 Health & Risks", "🌍 Eco Impact", "💡 Alternatives & Recipe"])
    with tab1:
        st.markdown(f'<div class="card">{result}</div>', unsafe_allow_html=True)
    with tab2:
        st.markdown(f'<div class="card">{result}</div>', unsafe_allow_html=True)
    with tab3:
        st.markdown(f'<div class="card">{result}</div>', unsafe_allow_html=True)

    # Save to Firebase
    save_scan(user_name, extracted_text, result)
    st.success("✅ Scan saved to your history!")

# ─── Scan History ──────────────────────────────────────────
with st.expander("📜 View My Scan History"):
    history = get_scan_history(user_name)
    if history:
        for i, scan in enumerate(reversed(history)):
            st.markdown(f'<div class="card"><b>Scan {i+1}</b> — {scan["timestamp"]}<br><br>{scan["ai_result"]}</div>', unsafe_allow_html=True)
    else:
        st.info("No scans yet. Upload a product to get started!")
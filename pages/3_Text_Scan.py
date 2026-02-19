import streamlit as st

from modules.ai_suggester import get_ai_analysis
from utils.firebase_ops import get_scan_history, save_scan


st.set_page_config(page_title="Text Scan · BeforeYouBuy", page_icon="✏️", layout="wide")

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');
*, *::before, *::after { box-sizing: border-box; margin: 0; }
html, body, [data-testid="stApp"] { background: #07070d !important; color: #eeeae4 !important; font-family: 'DM Sans', sans-serif !important; text-rendering: optimizeLegibility; -webkit-font-smoothing: antialiased; -moz-osx-font-smoothing: grayscale; }
#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="stDecoration"], [data-testid="stSidebarNav"] { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }
[data-testid="stMainBlockContainer"], .block-container { padding: 0 !important; max-width: 100% !important; }
::-webkit-scrollbar { width: 5px; } ::-webkit-scrollbar-track { background: #0e0e18; } ::-webkit-scrollbar-thumb { background: #3d2f7a; border-radius: 4px; }

.navbar { display: flex; align-items: center; justify-content: flex-start; gap: 16px; padding: 0 64px; height: 64px; background: rgba(7,7,13,0.95); border-bottom: 1px solid rgba(255,255,255,0.06); backdrop-filter: blur(12px); }
.nav-brand { display: flex; align-items: center; gap: 10px; font-family: 'Syne', sans-serif; font-size: 18px; font-weight: 700; color: #eeeae4; }
.nav-brand-icon { width: 32px; height: 32px; background: linear-gradient(135deg, #7c3aed, #5b21b6); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 15px; }
.nav-links { display: flex; align-items: center; gap: 4px; flex-wrap: nowrap; }
.nav-links [data-testid="stColumns"] { display: flex !important; flex-direction: row !important; gap: 4px !important; align-items: center !important; flex-wrap: nowrap !important; }
.nav-links [data-testid="stColumn"] { width: auto !important; flex: 0 0 auto !important; min-width: 0 !important; padding: 0 !important; }
.nav-links a[data-testid="stPageLink"] { padding: 7px 16px; border-radius: 8px; font-size: 14px; font-weight: 600; letter-spacing: 0.01em; color: rgba(238,234,228,0.82) !important; border: 1px solid transparent; text-decoration: none !important; white-space: nowrap; }
.nav-links a[data-testid="stPageLink"]:hover { color: #ffffff !important; background: rgba(255,255,255,0.07); }
.nav-links a[data-testid="stPageLink"][aria-current="page"] { color: #e9d5ff !important; background: rgba(110,60,255,0.16); border-color: rgba(110,60,255,0.32); }

.page-hero { background: linear-gradient(160deg, #0c0720 0%, #110d2a 50%, #07070d 100%); border-bottom: 1px solid rgba(110,70,255,0.1); padding: 48px 64px 40px; }
.page-eyebrow { font-size: 11px; font-weight: 600; letter-spacing: 0.16em; text-transform: uppercase; color: #7c3aed; margin-bottom: 10px; }
.page-title { font-family: 'Syne', sans-serif; font-size: clamp(32px, 4vw, 52px); font-weight: 800; letter-spacing: -0.03em; background: linear-gradient(130deg, #fff 0%, #c4b5fd 60%, #7c3aed 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 10px; }
.page-sub { font-size: 15px; font-weight: 400; color: rgba(238,234,228,0.72); line-height: 1.75; max-width: 640px; }

.content-area { padding: 32px 64px 64px; }
.step-label { font-size: 10.5px; font-weight: 600; letter-spacing: 0.16em; text-transform: uppercase; color: #7c3aed; margin-bottom: 6px; }
.step-title { font-family: 'Syne', sans-serif; font-size: 20px; font-weight: 700; color: #eeeae4; margin-bottom: 16px; }

[data-testid="stTextArea"] textarea { background: rgba(255,255,255,0.03) !important; border: 1px solid rgba(255,255,255,0.09) !important; border-radius: 14px !important; color: #eeeae4 !important; font-family: 'DM Sans', sans-serif !important; font-size: 14px !important; line-height: 1.7 !important; }
[data-testid="stTextArea"] textarea:focus { border-color: rgba(110,60,255,0.45) !important; box-shadow: 0 0 0 3px rgba(110,60,255,0.09) !important; }
[data-testid="stButton"] button { background: linear-gradient(135deg, #7c3aed 0%, #5b21b6 100%) !important; color: #fff !important; border: none !important; border-radius: 10px !important; font-family: 'Syne', sans-serif !important; font-weight: 600 !important; font-size: 14px !important; padding: 13px 28px !important; transition: all 0.22s !important; box-shadow: 0 3px 18px rgba(124,58,237,0.32) !important; width: 100% !important; margin-top: 12px !important; }
[data-testid="stButton"] button:hover { transform: translateY(-2px) !important; box-shadow: 0 6px 26px rgba(124,58,237,0.48) !important; }
[data-testid="stTabs"] [data-baseweb="tab-list"] { background: rgba(255,255,255,0.025) !important; border-radius: 12px !important; padding: 5px !important; border: 1px solid rgba(255,255,255,0.06) !important; gap: 3px !important; }
[data-testid="stTabs"] [data-baseweb="tab"] { background: transparent !important; border-radius: 8px !important; color: rgba(238,234,228,0.45) !important; font-family: 'DM Sans', sans-serif !important; font-weight: 500 !important; font-size: 13.5px !important; padding: 9px 18px !important; border: none !important; }
[data-testid="stTabs"] [aria-selected="true"] { background: rgba(110,58,237,0.22) !important; color: #c4b5fd !important; border: 1px solid rgba(110,58,237,0.28) !important; }
[data-testid="stTabs"] [data-baseweb="tab-highlight"] { display: none !important; }
hr { border: none !important; border-top: 1px solid rgba(255,255,255,0.06) !important; margin: 28px 0 !important; }
label { font-family: 'DM Sans', sans-serif !important; color: rgba(238,234,228,0.6) !important; font-size: 12.5px !important; font-weight: 500 !important; }
[data-testid="stAlert"] { border-radius: 10px !important; }
[data-testid="stTextInput"] input { background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(255,255,255,0.09) !important; border-radius: 9px !important; color: #eeeae4 !important; }
[data-testid="stSelectbox"] > div { background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(255,255,255,0.09) !important; border-radius: 9px !important; }
[data-testid="stMultiSelect"] > div { background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(255,255,255,0.09) !important; border-radius: 9px !important; }
</style>
""",
    unsafe_allow_html=True,
)

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

st.markdown(
    """
<div class="page-hero">
  <div class="page-eyebrow">✏️ Text Scan</div>
  <div class="page-title">Paste & Analyze Text</div>
  <p class="page-sub">Type or paste any ingredient list, product description, or item names and get a full AI-powered health and eco analysis instantly.</p>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="content-area">', unsafe_allow_html=True)

with st.expander("👤 Profile (optional)", expanded=False):
    user_name = st.text_input("Name", value="User", placeholder="Your name...")
    allergies = st.multiselect("Allergies", ["Gluten", "Nuts", "Dairy", "Soy", "Eggs", "Shellfish"])
    diet = st.selectbox("Diet", ["Regular", "Vegan", "Vegetarian", "Diabetic", "Low-sodium"])

st.markdown('<p class="step-label">Step 1 — Enter Text</p>', unsafe_allow_html=True)
st.markdown('<p class="step-title">Paste Ingredients or Item Names</p>', unsafe_allow_html=True)

text_input = st.text_area(
    "Paste text",
    height=200,
    placeholder="e.g. Sugar, Palm Oil, Modified Starch, Maltodextrin, Salt, Artificial Flavours, Permitted Preservatives (211)...",
    label_visibility="collapsed",
)

analyze = st.button("🔍 Analyze Text")

if text_input and analyze:
    st.divider()
    st.markdown('<p class="step-label">Step 2 — Results</p>', unsafe_allow_html=True)
    st.markdown('<p class="step-title">AI Analysis</p>', unsafe_allow_html=True)

    with st.spinner("🤖 Running AI analysis..."):
        context = f"User allergies: {allergies}, Diet: {diet}\n\n"
        result = get_ai_analysis(context + text_input)

    if isinstance(result, str):
        result = {"health": result, "eco": result, "alternatives": result}

    tab1, tab2, tab3 = st.tabs(["🥗 Health & Risks", "🌍 Eco Impact", "💡 Alternatives & Recipe"])
    with tab1:
        st.markdown(result["health"])
    with tab2:
        st.markdown(result["eco"])
    with tab3:
        st.markdown(result["alternatives"])

    save_scan(user_name, text_input, result["health"] + "\n\n" + result["eco"] + "\n\n" + result["alternatives"])
    st.success("✅ Scan saved to your history!")

st.divider()
with st.expander("📜 View My Scan History"):
    history = get_scan_history(user_name)
    if history:
        for i, scan in enumerate(reversed(history)):
            st.markdown(f"**Scan {i+1}** — {scan['timestamp']}")
            st.markdown(scan["ai_result"])
            st.divider()
    else:
        st.info("No scans yet. Paste some text to get started!")

st.markdown("</div>", unsafe_allow_html=True)
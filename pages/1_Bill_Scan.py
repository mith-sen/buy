import streamlit as st
import hashlib
import io

from modules.ai_suggester import get_ai_analysis
from modules.ocr_engine import extract_text_from_image
from utils.firebase_ops import get_scan_history, save_scan


st.set_page_config(page_title="Bill Scan · BeforeYouBuy", page_icon="🧾", layout="wide")

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
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="navbar"><div class="nav-brand"><div class="nav-brand-icon">🛒</div>BeforeYouBuy</div><div class="nav-links">',
    unsafe_allow_html=True,
)
st.page_link("app.py", label="Home")
st.page_link("pages/1_Bill_Scan.py", label="🧾 Bill Scan")
st.page_link("pages/2_Product_Scan.py", label="📦 Product Scan")
st.page_link("pages/3_Text_Scan.py", label="✍️ Text Scan")
st.markdown("</div></div>", unsafe_allow_html=True)

st.markdown(
    """
<div class="page-hero">
  <div class="page-eyebrow">🧾 Bill Scan</div>
  <div class="page-title">Upload & Analyze a Receipt</div>
  <p class="page-sub">Upload a photo of your shopping bill/receipt. We'll extract the text and generate health, eco impact, and alternative suggestions.</p>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="content-area">', unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def _cached_ocr(image_bytes: bytes) -> str:
    return extract_text_from_image(io.BytesIO(image_bytes))


@st.cache_data(show_spinner=False)
def _cached_ai(text: str):
    return get_ai_analysis(text)


with st.expander("👤 Profile (optional)", expanded=False):
    user_name = st.text_input("Name", value="User", placeholder="Your name...")
    allergies = st.multiselect("Allergies", ["Gluten", "Nuts", "Dairy", "Soy", "Eggs", "Shellfish"])
    diet = st.selectbox("Diet", ["Regular", "Vegan", "Vegetarian", "Diabetic", "Low-sodium"])

st.markdown('<p class="step-label">Step 1 — Upload</p>', unsafe_allow_html=True)
st.markdown('<p class="step-title">Upload a Receipt Image</p>', unsafe_allow_html=True)

img = st.file_uploader("Receipt image", type=["png", "jpg", "jpeg", "webp"], label_visibility="collapsed")
analyze = st.button("🔍 Extract & Analyze")

if img is not None:
    img_bytes = img.getvalue()
    img_hash = hashlib.sha256(img_bytes).hexdigest()

    if st.session_state.get("bill_img_hash") != img_hash:
        st.session_state["bill_img_hash"] = img_hash
        st.session_state.pop("bill_extracted", None)
        st.session_state.pop("bill_result", None)

if img and analyze:
    st.divider()
    st.markdown('<p class="step-label">Step 2 — Extracted Text</p>', unsafe_allow_html=True)

    with st.spinner("🧾 Extracting text from receipt..."):
        try:
            extracted = _cached_ocr(img_bytes)
            st.session_state["bill_extracted"] = extracted
        except Exception as e:
            err = str(e)
            if "429" in err or "ResourceExhausted" in err or "quota" in err.lower():
                st.error(
                    "⚠️ The Gemini API free tier quota has been exceeded for today.\n\n"
                    "Please wait until your quota resets or add billing to your Google AI Studio project.\n"
                    "You can still use the **Text Scan** page by pasting text manually once quota is available again."
                )
            else:
                st.error(f"Unexpected error while extracting text: {e}")
            st.stop()

    st.text_area("Extracted text", extracted, height=160)

    st.divider()
    st.markdown('<p class="step-label">Step 3 — Results</p>', unsafe_allow_html=True)
    st.markdown('<p class="step-title">AI Analysis</p>', unsafe_allow_html=True)

    with st.spinner("🤖 Running AI analysis... (~40 seconds)"):
        try:
            context = f"User allergies: {allergies}, Diet: {diet}\n\n"
            result = _cached_ai(context + extracted)
            st.session_state["bill_result"] = result
        except Exception as e:
            err = str(e)
            if "429" in err or "ResourceExhausted" in err or "quota" in err.lower():
                st.error(
                    "⚠️ The Gemini API free tier quota has been exceeded for today.\n\n"
                    "Please wait until your quota resets or add billing to your Google AI Studio project."
                )
            else:
                st.error(f"Unexpected error while running AI analysis: {e}")
            st.stop()

    if isinstance(result, str):
        result = {"health": result, "eco": result, "alternatives": result}

    tab1, tab2, tab3 = st.tabs(["🥗 Health & Risks", "🌍 Eco Impact", "💡 Alternatives & Recipe"])
    with tab1:
        st.markdown(result["health"])
    with tab2:
        st.markdown(result["eco"])
    with tab3:
        st.markdown(result["alternatives"])

    save_scan(
        user_name,
        extracted,
        result["health"] + "\n\n" + result["eco"] + "\n\n" + result["alternatives"],
    )
    st.success("✅ Scan saved to your history!")

# If we already computed results, show them without recomputing on rerun.
if st.session_state.get("bill_extracted") and st.session_state.get("bill_result"):
    extracted = st.session_state["bill_extracted"]
    result = st.session_state["bill_result"]
    if isinstance(result, str):
        result = {"health": result, "eco": result, "alternatives": result}

    st.divider()
    st.markdown('<p class="step-label">Extracted Text</p>', unsafe_allow_html=True)
    st.text_area("Extracted text (cached)", extracted, height=160)

    st.divider()
    st.markdown('<p class="step-title">AI Analysis (cached)</p>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["🥗 Health & Risks", "🌍 Eco Impact", "💡 Alternatives & Recipe"])
    with tab1:
        st.markdown(result["health"])
    with tab2:
        st.markdown(result["eco"])
    with tab3:
        st.markdown(result["alternatives"])

st.divider()
with st.expander("📜 View My Scan History"):
    history = get_scan_history(user_name)
    if history:
        for i, scan in enumerate(reversed(history)):
            st.markdown(f"**Scan {i+1}** — {scan['timestamp']}")
            st.markdown(scan["ai_result"])
            st.divider()
    else:
        st.info("No scans yet. Upload a receipt to get started!")

st.markdown("</div>", unsafe_allow_html=True)


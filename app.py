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

# ─── Header ────────────────────────────────────────────────
st.title("🛒 BeforeYouBuy")
st.subheader("AI-Powered Product & Bill Analyzer")
st.markdown("Upload a **product label** or **shopping bill** to get instant health, eco, and alternative insights!")
st.divider()

# ─── Sidebar ───────────────────────────────────────────────
with st.sidebar:
    st.header("👤 Your Profile")
    user_name = st.text_input("Your Name", value="User")
    allergies = st.multiselect("Known Allergies", 
        ["Gluten", "Nuts", "Dairy", "Soy", "Eggs", "Shellfish"])
    diet = st.selectbox("Diet Type", 
        ["Regular", "Vegan", "Vegetarian", "Diabetic", "Low-sodium"])
    st.divider()
    st.info("Your preferences help personalize the AI analysis!")

# ─── Input Method ──────────────────────────────────────────
input_method = st.radio("📤 Choose Input Method", 
    ["📷 Upload Product Image", "🧾 Upload Bill / Receipt", "✍️ Paste Text Manually"],
    horizontal=True)

st.divider()

extracted_text = ""

# ─── Image Upload ──────────────────────────────────────────
if input_method == "📷 Upload Product Image":
    uploaded_file = st.file_uploader("Upload product label image", 
        type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", width=300)
        if st.button("🔍 Analyze Product"):
            with st.spinner("Reading image..."):
                extracted_text = extract_text_from_image(uploaded_file)
            st.success("Text extracted!")

# ─── Bill Upload ───────────────────────────────────────────
elif input_method == "🧾 Upload Bill / Receipt":
    uploaded_file = st.file_uploader("Upload your shopping bill", 
        type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Bill", width=300)
        if st.button("🔍 Analyze Bill"):
            with st.spinner("Reading bill..."):
                extracted_text = extract_text_from_image(uploaded_file)
            st.success("Bill scanned!")

# ─── Manual Text ───────────────────────────────────────────
elif input_method == "✍️ Paste Text Manually":
    extracted_text = st.text_area("Paste product ingredients or bill text here", 
        height=200)
    st.button("🔍 Analyze Text")

# ─── AI Analysis ───────────────────────────────────────────
if extracted_text:
    st.divider()
    st.subheader("📊 Analysis Results")
    
    with st.spinner("AI is analyzing your product..."):
        # Add user profile context
        context = f"User allergies: {allergies}, Diet: {diet}\n\n"
        result = get_ai_analysis(context + extracted_text)
    
    # Display in tabs
    tab1, tab2, tab3 = st.tabs(["🥗 Health & Risks", "🌍 Eco Impact", "💡 Alternatives & Recipe"])
    
    with tab1:
        st.markdown(result)
    
    with tab2:
        st.markdown(result)
    
    with tab3:
        st.markdown(result)
    
    # Save to Firebase
    save_scan(user_name, extracted_text, result)
    st.success("✅ Scan saved to your history!")
    
    st.divider()

# ─── Scan History ──────────────────────────────────────────
with st.expander("📜 View My Scan History"):
    history = get_scan_history(user_name)
    if history:
        for i, scan in enumerate(reversed(history)):
            st.markdown(f"**Scan {i+1}** — {scan['timestamp']}")
            st.markdown(scan['ai_result'])
            st.divider()
    else:
        st.info("No scans yet. Upload a product to get started!")
import streamlit as st
import random
from modules.ocr_engine import extract_text_from_image
from modules.ai_suggester import get_ai_analysis
from utils.firebase_ops import save_scan, get_scan_history

st.set_page_config(page_title="BeforeYouBuy", page_icon="🛒", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&family=DM+Serif+Display:ital@0;1&display=swap');

    * { font-family: 'DM Sans', sans-serif; }
    #MainMenu, footer, header { visibility: hidden; }
    .stApp { background: #07070f; color: #dddde8; }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: #0c0c16 !important;
        border-right: 1px solid #1a1a2e !important;
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #9999b0;
        font-size: 14px;
    }
    /* Sidebar toggle arrow button */
    [data-testid="collapsedControl"] {
        color: #00d68f !important;
        background: #0e0e1c !important;
        border: 1px solid #1a1a2e !important;
        border-radius: 0 8px 8px 0 !important;
    }

    /* ── Top bar ── */
    .top-bar {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 20px 0 0 0;
        border-bottom: 1px solid #13131f;
        margin-bottom: 0;
    }
    .top-title {
        font-family: 'DM Serif Display', serif;
        font-size: 36px;
        color: #ffffff;
        margin: 0;
        letter-spacing: -0.5px;
        line-height: 1;
    }
    .top-title span { color: #00d68f; }
    .top-quote {
        font-size: 13px;
        color: #3a3a50;
        font-style: italic;
        font-weight: 300;
        margin: 6px 0 16px 0;
        text-align: center;
    }

    .setup-card { background: #0e0e1c; border: 1px solid #1a1a2e; border-radius: 24px; padding: 40px; max-width: 480px; margin: 40px auto; text-align: center; }
    .setup-title { font-family: 'DM Serif Display', serif; font-size: 28px; color: #fff; margin: 0 0 8px; }
    .setup-subtitle { font-size: 14px; color: #55556a; margin: 0 0 32px; }

    .label { font-size: 11px; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; color: #3a3a50; margin-bottom: 12px; }

    .badge-recommended { display: inline-block; background: rgba(0,214,143,0.12); border: 1px solid rgba(0,214,143,0.3); color: #00d68f; padding: 6px 18px; border-radius: 100px; font-size: 13px; font-weight: 600; }
    .badge-not-recommended { display: inline-block; background: rgba(239,68,68,0.12); border: 1px solid rgba(239,68,68,0.3); color: #ef4444; padding: 6px 18px; border-radius: 100px; font-size: 13px; font-weight: 600; }
    .badge-caution { display: inline-block; background: rgba(245,158,11,0.12); border: 1px solid rgba(245,158,11,0.3); color: #f59e0b; padding: 6px 18px; border-radius: 100px; font-size: 13px; font-weight: 600; }

    .scores-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin: 24px 0; }
    .score-card { background: #0e0e1c; border: 1px solid #1a1a2e; border-radius: 16px; padding: 20px; text-align: center; }
    .score-val { font-family: 'DM Serif Display', serif; font-size: 48px; line-height: 1; }
    .score-lbl { font-size: 11px; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; color: #3a3a50; margin-top: 8px; }
    .green { color: #00d68f; }
    .amber { color: #f59e0b; }
    .red   { color: #ef4444; }

    .result-block { background: #0e0e1c; border: 1px solid #1a1a2e; border-radius: 20px; padding: 28px 32px; margin-bottom: 16px; }
    .result-block h3 { font-family: 'DM Serif Display', serif; font-size: 20px; font-weight: 400; color: #fff; margin: 0 0 16px; padding-bottom: 14px; border-bottom: 1px solid #13131f; }
    .result-block p { font-size: 14px; color: #9999b0; line-height: 1.8; margin: 0; white-space: pre-line; }

    .homemade-block { background: linear-gradient(135deg, #0a1a0e, #0e0e1c); border: 1px solid rgba(0,214,143,0.2); border-radius: 20px; padding: 28px 32px; margin-bottom: 16px; }
    .homemade-block h3 { font-family: 'DM Serif Display', serif; font-size: 20px; color: #00d68f; margin: 0 0 16px; padding-bottom: 14px; border-bottom: 1px solid rgba(0,214,143,0.15); }
    .homemade-block p { font-size: 14px; color: #9999b0; line-height: 1.8; margin: 0; white-space: pre-line; }

    .bill-card { background: #0e0e1c; border: 1px solid #1a1a2e; border-radius: 20px; padding: 28px 32px; margin-bottom: 16px; }
    .bill-card h3 { font-family: 'DM Serif Display', serif; font-size: 20px; color: #fff; margin: 0 0 16px; padding-bottom: 14px; border-bottom: 1px solid #13131f; }
    .bill-card p { font-size: 14px; color: #9999b0; line-height: 1.8; margin: 0; white-space: pre-line; }
    .savings-highlight { background: rgba(0,214,143,0.08); border: 1px solid rgba(0,214,143,0.2); border-radius: 12px; padding: 16px 20px; margin: 12px 0; font-size: 14px; color: #00d68f; }

    .sidebar-section-title { font-family: 'DM Serif Display', serif; font-size: 22px; color: #fff; margin: 0 0 16px; }
    .history-item { background: #13131f; border: 1px solid #1a1a2e; border-radius: 12px; padding: 14px 16px; margin-bottom: 8px; font-size: 13px; color: #9999b0; }
    .history-date { font-size: 11px; color: #3a3a50; margin-bottom: 4px; }
    .bookmark-card { background: #13131f; border: 1px solid rgba(0,214,143,0.15); border-radius: 12px; padding: 14px 16px; margin-bottom: 8px; }
    .bookmark-title { font-size: 13px; font-weight: 600; color: #fff; margin-bottom: 4px; }
    .bookmark-desc { font-size: 12px; color: #55556a; }

    .info-bar { display: flex; align-items: center; gap: 24px; padding: 12px 0; border-bottom: 1px solid #13131f; margin-bottom: 28px; flex-wrap: wrap; }
    .info-bar-item { font-size: 13px; color: #55556a; }
    .info-bar-item span { color: #fff; font-weight: 500; }

    .stButton > button { background: #00d68f; color: #07070f; font-weight: 600; font-size: 14px; border: none; border-radius: 12px; padding: 14px 32px; width: 100%; transition: all 0.2s; }
    .stButton > button:hover { background: #00c07f; transform: translateY(-1px); box-shadow: 0 8px 24px rgba(0,214,143,0.2); }

    .stTabs [data-baseweb="tab-list"] { background: transparent; border-bottom: 1px solid #1a1a2e; gap: 0; padding: 0; }
    .stTabs [data-baseweb="tab"] { background: transparent; color: #3a3a50; font-size: 13px; font-weight: 500; padding: 12px 24px; border-radius: 0; border-bottom: 2px solid transparent; }
    .stTabs [aria-selected="true"] { background: transparent !important; color: #00d68f !important; border-bottom: 2px solid #00d68f !important; }

    hr { border-color: #13131f; margin: 28px 0; }
    [data-testid="stFileUploader"] { background: #0e0e1c; border: 1px dashed #1a1a2e; border-radius: 16px; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar — Bookmarks & History ────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-section-title">Bookmarks</div>', unsafe_allow_html=True)
    bookmarks = st.session_state.get("bookmarks", [])
    if bookmarks:
        for i, b in enumerate(bookmarks):
            st.markdown(f"""
            <div class="bookmark-card">
                <div class="bookmark-title">Recipe {i+1}</div>
                <div class="bookmark-desc">{b['product'][:50]}...</div>
            </div>
            """, unsafe_allow_html=True)
            with st.expander(f"View recipe {i+1}"):
                st.markdown(f"**Ingredients:**\n\n{b['ingredients']}")
                st.markdown(f"**Steps:**\n\n{b['howto']}")
    else:
        st.markdown('<p style="color:#3a3a50;font-size:13px">No bookmarks yet. Scan a product and save a recipe!</p>', unsafe_allow_html=True)

    st.markdown("<hr style='border-color:#1a1a2e;margin:20px 0'>", unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-title">History</div>', unsafe_allow_html=True)
    user_id = st.session_state.get("user_name", "User")
    history = get_scan_history(user_id)
    if history:
        for i, scan in enumerate(reversed(history)):
            st.markdown(f"""
            <div class="history-item">
                <div class="history-date">Scan {i+1} · {scan.get('timestamp', '')}</div>
                {str(scan.get('ai_result', ''))[:150]}...
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<p style="color:#3a3a50;font-size:13px">No scans yet.</p>', unsafe_allow_html=True)

# ── Top Title ─────────────────────────────────────────────────
st.markdown("""
<div class="top-bar">
    <h1 class="top-title">Before<span>You</span>Buy</h1>
</div>
<p class="top-quote">"Buy smart today, live healthier tomorrow."</p>
""", unsafe_allow_html=True)

# ── Step 1: Profile Setup ─────────────────────────────────────
if "profile_done" not in st.session_state:
    st.markdown("""
    <div class="setup-card">
        <div class="setup-title">Personalize Your Results</div>
        <div class="setup-subtitle">Enter your details so we can tailor health recommendations just for you.</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        name      = st.text_input("Your Name", placeholder="e.g. Mithura")
        height    = st.number_input("Height (cm)", min_value=100, max_value=250, value=165)
        weight    = st.number_input("Weight (kg)", min_value=20,  max_value=200, value=60)
        allergies = st.multiselect("Known Allergies (optional)",
            ["Gluten", "Nuts", "Dairy", "Soy", "Eggs", "Shellfish"])
        diet      = st.selectbox("Diet Type",
            ["Regular", "Vegan", "Vegetarian", "Diabetic", "Low-sodium"])
        if st.button("Continue"):
            if name:
                bmi = round(weight / ((height / 100) ** 2), 1)
                st.session_state.profile_done = True
                st.session_state.user_name    = name
                st.session_state.height       = height
                st.session_state.weight       = weight
                st.session_state.bmi          = bmi
                st.session_state.allergies    = allergies
                st.session_state.diet         = diet
                st.rerun()
            else:
                st.warning("Please enter your name.")

# ── Step 2: Main App ──────────────────────────────────────────
else:
    name      = st.session_state.user_name
    bmi       = st.session_state.bmi
    height    = st.session_state.height
    weight    = st.session_state.weight
    allergies = st.session_state.allergies
    diet      = st.session_state.diet

    bmi_status = ("Underweight" if bmi < 18.5 else "Healthy" if bmi < 25 else "Overweight" if bmi < 30 else "Obese")
    bmi_color  = ("#f59e0b" if bmi < 18.5 else "#00d68f" if bmi < 25 else "#f59e0b" if bmi < 30 else "#ef4444")

    st.markdown(f"""
    <div class="info-bar">
        <div class="info-bar-item">Hello, <span>{name}</span></div>
        <div class="info-bar-item">BMI: <span style="color:{bmi_color}">{bmi} ({bmi_status})</span></div>
        <div class="info-bar-item">{height} cm · {weight} kg</div>
        <div class="info-bar-item">Diet: <span>{diet}</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="label">Choose Scan Method</div>', unsafe_allow_html=True)
    method = st.radio("", ["Upload Product Image", "Scan Bill / Receipt", "Enter Ingredients as Text"],
        horizontal=True, label_visibility="collapsed")
    st.markdown("<br>", unsafe_allow_html=True)

    if method == "Upload Product Image":
        uploaded = st.file_uploader("Upload product label or packaging", type=["jpg","jpeg","png"])
        if uploaded:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(uploaded, use_column_width=True)
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Analyze Product"):
                    with st.spinner("Reading product..."):
                        extracted_text = extract_text_from_image(uploaded)
                    st.session_state.last_scan     = extracted_text
                    st.session_state.scan_type     = "product"
                    st.session_state.show_homemade = False
                    st.session_state.show_howto    = False
                    st.session_state.last_result   = None
                    st.session_state.health_result = None
                    st.session_state.eco_result    = None
                    st.session_state.unsafe_result = None

    elif method == "Scan Bill / Receipt":
        uploaded = st.file_uploader("Upload your shopping bill or receipt", type=["jpg","jpeg","png"])
        if uploaded:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(uploaded, use_column_width=True)
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Analyze Bill"):
                    with st.spinner("Reading bill..."):
                        extracted_text = extract_text_from_image(uploaded)
                    st.session_state.last_scan     = extracted_text
                    st.session_state.scan_type     = "bill"
                    st.session_state.show_homemade = False
                    st.session_state.show_howto    = False
                    st.session_state.last_result   = None

    elif method == "Enter Ingredients as Text":
        text_input = st.text_area("Type or paste ingredients / product details", height=180)
        if st.button("Analyze Text"):
            st.session_state.last_scan     = text_input
            st.session_state.scan_type     = "product"
            st.session_state.show_homemade = False
            st.session_state.show_howto    = False
            st.session_state.last_result   = None
            st.session_state.health_result = None
            st.session_state.eco_result    = None
            st.session_state.unsafe_result = None

    # ── Results ───────────────────────────────────────────────
    if "last_scan" in st.session_state and st.session_state.last_scan:
        scan_text = st.session_state.last_scan
        scan_type = st.session_state.get("scan_type", "product")

        st.markdown("<hr>", unsafe_allow_html=True)

        if not st.session_state.get("last_result"):
            with st.spinner("Analyzing..."):
                if scan_type == "product":
                    health_result = get_ai_analysis(f"""
                    User: Height {height}cm, Weight {weight}kg, BMI {bmi} ({bmi_status}), Diet: {diet}, Allergies: {allergies}
                    Product: {scan_text}
                    Give ONLY:
                    1. RECOMMENDED or NOT RECOMMENDED verdict with reason (2-3 sentences)
                    2. Top 3 health risks for this specific person
                    3. Health score out of 100
                    Keep it short and direct.
                    """)
                    eco_result = get_ai_analysis(f"""
                    Product: {scan_text}
                    Give ONLY:
                    1. Packaging type and recyclability
                    2. Carbon footprint estimate
                    3. Eco-friendly packaging alternatives
                    4. Eco score out of 100
                    Keep it short and factual.
                    """)
                    unsafe_result = get_ai_analysis(f"""
                    Product: {scan_text}
                    List TOP 4-5 most unsafe ingredients in this product.
                    For each explain in ONE sentence why it is harmful.
                    Format:
                    - Ingredient Name: Why it is harmful
                    If all are safe, say: "All ingredients appear to be safe."
                    Nothing else.
                    """)
                    st.session_state.health_result = health_result
                    st.session_state.eco_result    = eco_result
                    st.session_state.unsafe_result = unsafe_result
                    st.session_state.last_result   = health_result
                    save_scan(name, scan_text, health_result)

                else:
                    bill_result = get_ai_analysis(f"""
                    User: Height {height}cm, Weight {weight}kg, BMI {bmi} ({bmi_status}), Diet: {diet}, Allergies: {allergies}
                    Bill: {scan_text}
                    Provide these 4 sections with exact headers:
                    BILL SUMMARY:
                    HEALTH IMPACT:
                    COST SAVINGS:
                    BETTER ALTERNATIVES:
                    """)
                    st.session_state.last_result = bill_result
                    save_scan(name, scan_text, bill_result)

        # ── Product results ───────────────────────────────────
        if scan_type == "product":
            health_result = st.session_state.get("health_result", "")
            eco_result    = st.session_state.get("eco_result", "")
            unsafe_result = st.session_state.get("unsafe_result", "")

            result_lower = health_result.lower()
            if "not recommended" in result_lower:
                badge = '<span class="badge-not-recommended">Not Recommended</span>'
            elif "caution" in result_lower or "moderate" in result_lower:
                badge = '<span class="badge-caution">Use with Caution</span>'
            else:
                badge = '<span class="badge-recommended">Recommended</span>'

            hs = random.randint(30, 90)
            es = random.randint(30, 85)
            ss = random.randint(40, 95)
            def sc(s): return "green" if s >= 70 else "amber" if s >= 40 else "red"

            st.markdown(f"""
            <div style="margin-bottom:20px">{badge}</div>
            <div class="scores-row">
                <div class="score-card"><div class="score-val {sc(hs)}">{hs}</div><div class="score-lbl">Health Score</div></div>
                <div class="score-card"><div class="score-val {sc(es)}">{es}</div><div class="score-lbl">Eco Score</div></div>
                <div class="score-card"><div class="score-val {sc(ss)}">{ss}</div><div class="score-lbl">Safety Score</div></div>
            </div>
            """, unsafe_allow_html=True)

            # Make it Yourself — right below scores
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("Make it Yourself — Healthier Version"):
                    st.session_state.show_homemade = True
                    st.session_state.show_howto    = False
                    with st.spinner("Getting ingredients..."):
                        st.session_state.homemade_info = get_ai_analysis(f"""
                        Product: {scan_text}
                        List ONLY the ingredients needed to make a healthier homemade version.
                        Clean bullet list only. No intro, no explanation.
                        - ingredient 1
                        - ingredient 2
                        """)

            st.markdown("<br>", unsafe_allow_html=True)

            # Tabs — unique content each
            tab1, tab2, tab3 = st.tabs(["Health Analysis", "Eco Impact", "Unsafe Ingredients"])
            with tab1:
                st.markdown(f'<div class="result-block"><h3>Health Analysis</h3><p>{health_result}</p></div>', unsafe_allow_html=True)
            with tab2:
                st.markdown(f'<div class="result-block"><h3>Environmental Impact</h3><p>{eco_result}</p></div>', unsafe_allow_html=True)
            with tab3:
                st.markdown(f'<div class="result-block"><h3>Unsafe Ingredients</h3><p>{unsafe_result}</p></div>', unsafe_allow_html=True)

            # Make it Yourself section
            if st.session_state.get("show_homemade"):
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown(f"""
                <div class="homemade-block">
                    <h3>Ingredients to Buy</h3>
                    <p>{st.session_state.get('homemade_info', '')}</p>
                </div>
                """, unsafe_allow_html=True)

                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("How to Make it"):
                        with st.spinner("Getting recipe..."):
                            st.session_state.howto_info = get_ai_analysis(f"""
                            Product: {scan_text}
                            Give ONLY step by step instructions to make a healthier homemade version.
                            Step 1: ...
                            Step 2: ...
                            No intro, just steps.
                            """)
                            st.session_state.show_howto = True

            # How to Make section
            if st.session_state.get("show_howto"):
                howto_info = st.session_state.get("howto_info", "")
                st.markdown(f"""
                <div class="result-block">
                    <h3>How to Make it</h3>
                    <p>{howto_info}</p>
                </div>
                """, unsafe_allow_html=True)

                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("Save to Bookmarks"):
                        if "bookmarks" not in st.session_state:
                            st.session_state.bookmarks = []
                        already = any(b["product"] == scan_text[:60] for b in st.session_state.bookmarks)
                        if not already:
                            st.session_state.bookmarks.append({
                                "product":     scan_text[:60],
                                "ingredients": st.session_state.get("homemade_info", ""),
                                "howto":       howto_info
                            })
                            st.success("Saved to Bookmarks!")
                        else:
                            st.info("Already in bookmarks!")

        # ── Bill results ──────────────────────────────────────
        else:
            bill_result = st.session_state.get("last_result", "")
            sections    = bill_result.split("\n\n")

            def get_section(keyword):
                for s in sections:
                    if keyword.upper() in s.upper():
                        lines = s.split("\n")
                        return "\n".join(l for l in lines if keyword.upper() not in l.upper()).strip()
                return bill_result

            tab1, tab2, tab3, tab4 = st.tabs(["Bill Summary", "Health Impact", "Cost Savings", "Better Alternatives"])
            with tab1:
                st.markdown(f'<div class="bill-card"><h3>Bill Breakdown</h3><p>{get_section("BILL SUMMARY")}</p></div>', unsafe_allow_html=True)
            with tab2:
                st.markdown(f'<div class="bill-card"><h3>Health Impact</h3><p>{get_section("HEALTH IMPACT")}</p></div>', unsafe_allow_html=True)
            with tab3:
                st.markdown(f"""
                <div class="bill-card">
                    <h3>Potential Savings</h3>
                    <div class="savings-highlight">Here is where you could have saved!</div>
                    <p>{get_section("COST SAVINGS")}</p>
                </div>
                """, unsafe_allow_html=True)
            with tab4:
                st.markdown(f'<div class="bill-card"><h3>What to Buy Next Time</h3><p>{get_section("BETTER ALTERNATIVES")}</p></div>', unsafe_allow_html=True)

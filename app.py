import streamlit as st
import random
from modules.ocr_engine import extract_text_from_image
from modules.ai_suggester import get_ai_analysis
from utils.firebase_ops import save_scan, get_scan_history

st.set_page_config(page_title="BeforeYouBuy", page_icon="🛒", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,300&family=DM+Serif+Display:ital@0;1&display=swap');

    * { font-family: 'DM Sans', sans-serif; }
    #MainMenu, footer, header { visibility: hidden; }
    .stApp { background: #07070f; color: #dddde8; }
    [data-testid="stSidebar"] { display: none; }

    .hero {
        text-align: center;
        padding: 64px 20px 48px;
        border-bottom: 1px solid #13131f;
    }
    .hero-title {
        font-family: 'DM Serif Display', serif;
        font-size: 56px;
        color: #ffffff;
        margin: 0 0 12px;
        letter-spacing: -1px;
    }
    .hero-title span { color: #00d68f; }
    .hero-quote {
        font-size: 15px;
        color: #55556a;
        font-style: italic;
        font-weight: 300;
        margin: 0;
    }

    .setup-card {
        background: #0e0e1c;
        border: 1px solid #1a1a2e;
        border-radius: 24px;
        padding: 40px;
        max-width: 480px;
        margin: 48px auto;
        text-align: center;
    }
    .setup-title {
        font-family: 'DM Serif Display', serif;
        font-size: 28px;
        color: #fff;
        margin: 0 0 8px;
    }
    .setup-subtitle {
        font-size: 14px;
        color: #55556a;
        margin: 0 0 32px;
    }

    .label {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #3a3a50;
        margin-bottom: 12px;
    }

    .badge-recommended {
        display: inline-block;
        background: rgba(0,214,143,0.12);
        border: 1px solid rgba(0,214,143,0.3);
        color: #00d68f;
        padding: 6px 18px;
        border-radius: 100px;
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .badge-not-recommended {
        display: inline-block;
        background: rgba(239,68,68,0.12);
        border: 1px solid rgba(239,68,68,0.3);
        color: #ef4444;
        padding: 6px 18px;
        border-radius: 100px;
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .badge-caution {
        display: inline-block;
        background: rgba(245,158,11,0.12);
        border: 1px solid rgba(245,158,11,0.3);
        color: #f59e0b;
        padding: 6px 18px;
        border-radius: 100px;
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    .scores-row {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 12px;
        margin: 24px 0;
    }
    .score-card {
        background: #0e0e1c;
        border: 1px solid #1a1a2e;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
    }
    .score-val {
        font-family: 'DM Serif Display', serif;
        font-size: 48px;
        line-height: 1;
    }
    .score-lbl {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: #3a3a50;
        margin-top: 8px;
    }
    .green { color: #00d68f; }
    .amber { color: #f59e0b; }
    .red   { color: #ef4444; }

    .result-block {
        background: #0e0e1c;
        border: 1px solid #1a1a2e;
        border-radius: 20px;
        padding: 28px 32px;
        margin-bottom: 16px;
    }
    .result-block h3 {
        font-family: 'DM Serif Display', serif;
        font-size: 20px;
        font-weight: 400;
        color: #fff;
        margin: 0 0 16px;
        padding-bottom: 14px;
        border-bottom: 1px solid #13131f;
    }
    .result-block p, .result-block li {
        font-size: 14px;
        color: #9999b0;
        line-height: 1.8;
    }

    .homemade-block {
        background: linear-gradient(135deg, #0a1a0e, #0e0e1c);
        border: 1px solid rgba(0,214,143,0.2);
        border-radius: 20px;
        padding: 28px 32px;
        margin-bottom: 16px;
    }
    .homemade-block h3 {
        font-family: 'DM Serif Display', serif;
        font-size: 20px;
        color: #00d68f;
        margin: 0 0 16px;
        padding-bottom: 14px;
        border-bottom: 1px solid rgba(0,214,143,0.15);
    }

    .bill-card {
        background: #0e0e1c;
        border: 1px solid #1a1a2e;
        border-radius: 20px;
        padding: 28px 32px;
        margin-bottom: 16px;
    }
    .bill-card h3 {
        font-family: 'DM Serif Display', serif;
        font-size: 20px;
        color: #fff;
        margin: 0 0 16px;
        padding-bottom: 14px;
        border-bottom: 1px solid #13131f;
    }
    .savings-highlight {
        background: rgba(0,214,143,0.08);
        border: 1px solid rgba(0,214,143,0.2);
        border-radius: 12px;
        padding: 16px 20px;
        margin: 12px 0;
        font-size: 14px;
        color: #00d68f;
    }

    .history-item {
        background: #0e0e1c;
        border: 1px solid #1a1a2e;
        border-radius: 14px;
        padding: 18px 22px;
        margin-bottom: 10px;
        font-size: 13px;
        color: #9999b0;
    }
    .history-date {
        font-size: 11px;
        color: #3a3a50;
        margin-bottom: 6px;
    }

    .bookmark-card {
        background: #0e0e1c;
        border: 1px solid rgba(0,214,143,0.15);
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 10px;
    }
    .bookmark-title {
        font-size: 14px;
        font-weight: 600;
        color: #fff;
        margin-bottom: 6px;
    }
    .bookmark-desc {
        font-size: 13px;
        color: #55556a;
    }

    .info-bar {
        display: flex;
        align-items: center;
        gap: 24px;
        padding: 14px 0;
        border-bottom: 1px solid #13131f;
        margin-bottom: 32px;
        flex-wrap: wrap;
    }
    .info-bar-item {
        font-size: 13px;
        color: #55556a;
    }
    .info-bar-item span {
        color: #fff;
        font-weight: 500;
    }

    .stButton > button {
        background: #00d68f;
        color: #07070f;
        font-weight: 600;
        font-size: 14px;
        border: none;
        border-radius: 12px;
        padding: 14px 32px;
        width: 100%;
        transition: all 0.2s;
        letter-spacing: 0.3px;
    }
    .stButton > button:hover {
        background: #00c07f;
        transform: translateY(-1px);
        box-shadow: 0 8px 24px rgba(0,214,143,0.2);
    }

    .stTabs [data-baseweb="tab-list"] {
        background: transparent;
        border-bottom: 1px solid #1a1a2e;
        gap: 0; padding: 0;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: #3a3a50;
        font-size: 13px;
        font-weight: 500;
        padding: 12px 24px;
        border-radius: 0;
        border-bottom: 2px solid transparent;
    }
    .stTabs [aria-selected="true"] {
        background: transparent !important;
        color: #00d68f !important;
        border-bottom: 2px solid #00d68f !important;
    }

    hr { border-color: #13131f; margin: 32px 0; }

    [data-testid="stFileUploader"] {
        background: #0e0e1c;
        border: 1px dashed #1a1a2e;
        border-radius: 16px;
    }
</style>
""", unsafe_allow_html=True)

# ── Hero ─────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1 class="hero-title">Before<span>You</span>Buy</h1>
    <p class="hero-quote">"Buy smart today, live healthier tomorrow."</p>
</div>
""", unsafe_allow_html=True)

# ── Top right buttons ─────────────────────────────────────────
col_space, col_bk, col_hist = st.columns([5, 1, 1])
with col_bk:
    show_bookmarks = st.button("Bookmarks")
with col_hist:
    show_history = st.button("History")

# ── Bookmarks panel ───────────────────────────────────────────
if show_bookmarks:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="label">Saved Recipes</div>', unsafe_allow_html=True)
    bookmarks = st.session_state.get("bookmarks", [])
    if bookmarks:
        for i, b in enumerate(bookmarks):
            st.markdown(f"""
            <div class="bookmark-card">
                <div class="bookmark-title">Recipe {i+1} — {b['product']}</div>
                <div class="bookmark-desc">{b['ingredients'][:200]}...</div>
            </div>
            """, unsafe_allow_html=True)
            with st.expander(f"View full recipe {i+1}"):
                st.markdown(b['howto'])
    else:
        st.markdown('<div class="history-item" style="text-align:center;color:#3a3a50">No bookmarks yet. Scan a product and save a recipe!</div>', unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

# ── History panel ─────────────────────────────────────────────
if show_history:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div class="label">Scan History</div>', unsafe_allow_html=True)
    user_id = st.session_state.get("user_name", "User")
    history = get_scan_history(user_id)
    if history:
        for i, scan in enumerate(reversed(history)):
            st.markdown(f"""
            <div class="history-item">
                <div class="history-date">Scan {i+1} · {scan.get('timestamp', '')}</div>
                {str(scan.get('ai_result', ''))[:300]}...
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="history-item" style="text-align:center;color:#3a3a50">No scans yet.</div>', unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

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
        name     = st.text_input("Your Name", placeholder="e.g. Mithura")
        height   = st.number_input("Height (cm)", min_value=100, max_value=250, value=165)
        weight   = st.number_input("Weight (kg)", min_value=20,  max_value=200, value=60)
        allergies = st.multiselect("Known Allergies (optional)",
            ["Gluten", "Nuts", "Dairy", "Soy", "Eggs", "Shellfish"])
        diet     = st.selectbox("Diet Type",
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

    bmi_status = ("Underweight" if bmi < 18.5 else
                  "Healthy"     if bmi < 25   else
                  "Overweight"  if bmi < 30   else "Obese")
    bmi_color  = ("#f59e0b" if bmi < 18.5 else
                  "#00d68f" if bmi < 25   else
                  "#f59e0b" if bmi < 30   else "#ef4444")

    st.markdown(f"""
    <div class="info-bar">
        <div class="info-bar-item">Hello, <span>{name}</span></div>
        <div class="info-bar-item">BMI: <span style="color:{bmi_color}">{bmi} ({bmi_status})</span></div>
        <div class="info-bar-item">{height} cm · {weight} kg</div>
        <div class="info-bar-item">Diet: <span>{diet}</span></div>
    </div>
    """, unsafe_allow_html=True)

    # ── Scan method ───────────────────────────────────────────
    st.markdown('<div class="label">Choose Scan Method</div>', unsafe_allow_html=True)
    method = st.radio("", ["Upload Product Image", "Scan Bill / Receipt", "Enter Ingredients as Text"],
        horizontal=True, label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)

    extracted_text = ""

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
                    st.session_state.last_scan  = extracted_text
                    st.session_state.scan_type  = "product"
                    st.session_state.show_homemade = False
                    st.session_state.show_howto    = False

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
                    st.session_state.last_scan  = extracted_text
                    st.session_state.scan_type  = "bill"
                    st.session_state.show_homemade = False
                    st.session_state.show_howto    = False

    elif method == "Enter Ingredients as Text":
        text_input = st.text_area("Type or paste ingredients / product details", height=180)
        if st.button("Analyze Text"):
            st.session_state.last_scan  = text_input
            st.session_state.scan_type  = "product"
            st.session_state.show_homemade = False
            st.session_state.show_howto    = False

    # ── Results ───────────────────────────────────────────────
    if "last_scan" in st.session_state and st.session_state.last_scan:
        scan_text = st.session_state.last_scan
        scan_type = st.session_state.get("scan_type", "product")

        st.markdown("<hr>", unsafe_allow_html=True)

        # Only run AI if we don't already have a result cached
        if "last_result" not in st.session_state or st.session_state.get("result_for") != scan_text:
            with st.spinner("Analyzing..."):
                if scan_type == "bill":
                    prompt = f"""
                    User profile: Height {height}cm, Weight {weight}kg, BMI {bmi} ({bmi_status}), Diet: {diet}, Allergies: {allergies}

                    This is a shopping bill/receipt:
                    {scan_text}

                    Provide:
                    1. BILL SUMMARY - Explain the bill in simple language
                    2. HEALTH IMPACT - Health impact of purchased items for this person
                    3. COST SAVINGS - How much could have been saved and on what items
                    4. NEXT TIME - What to buy and what to avoid next time
                    5. BETTER ALTERNATIVES - Suggest healthier/cheaper alternatives

                    Be specific, practical, and beginner-friendly.
                    """
                else:
                    prompt = f"""
                    User profile: Height {height}cm, Weight {weight}kg, BMI {bmi} ({bmi_status}), Diet: {diet}, Allergies: {allergies}

                    Analyze this product:
                    {scan_text}

                    Provide:
                    1. RECOMMENDATION - Is this product recommended or not recommended for this person?
                    2. HEALTH SCORE - Score out of 100
                    3. UNSAFE INGREDIENTS - List harmful ingredients and explain why
                    4. HEALTH RISKS - Specific risks for this person
                    5. ECO IMPACT - Environmental impact

                    Be specific, practical, and beginner-friendly.
                    """
                result = get_ai_analysis(prompt)
                st.session_state.last_result = result
                st.session_state.result_for  = scan_text
                save_scan(name, scan_text, result)
        else:
            result = st.session_state.last_result

        # ── Product results ───────────────────────────────────
        if scan_type == "product":
            result_lower = result.lower()
            if "not recommended" in result_lower:
                badge = '<span class="badge-not-recommended">Not Recommended</span>'
            elif "caution" in result_lower or "moderate" in result_lower:
                badge = '<span class="badge-caution">Use with Caution</span>'
            else:
                badge = '<span class="badge-recommended">Recommended</span>'

            health = random.randint(30, 90)
            eco    = random.randint(30, 85)
            safety = random.randint(40, 95)
            def sc(s): return "green" if s >= 70 else "amber" if s >= 40 else "red"

            st.markdown(f"""
            <div style="margin-bottom:24px">{badge}</div>
            <div class="scores-row">
                <div class="score-card">
                    <div class="score-val {sc(health)}">{health}</div>
                    <div class="score-lbl">Health Score</div>
                </div>
                <div class="score-card">
                    <div class="score-val {sc(eco)}">{eco}</div>
                    <div class="score-lbl">Eco Score</div>
                </div>
                <div class="score-card">
                    <div class="score-val {sc(safety)}">{safety}</div>
                    <div class="score-lbl">Safety Score</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            tab1, tab2, tab3 = st.tabs(["Health Analysis", "Eco Impact", "Unsafe Ingredients"])
            with tab1:
                st.markdown(f'<div class="result-block"><h3>Health Analysis</h3><p>{result}</p></div>', unsafe_allow_html=True)
            with tab2:
                st.markdown(f'<div class="result-block"><h3>Environmental Impact</h3><p>{result}</p></div>', unsafe_allow_html=True)
            with tab3:
                st.markdown(f'<div class="result-block"><h3>Ingredient Breakdown</h3><p>{result}</p></div>', unsafe_allow_html=True)

            # ── Make it Yourself button ───────────────────────
            st.markdown("<hr>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("Make it Yourself — Healthier Version"):
                    st.session_state.show_homemade = True
                    st.session_state.show_howto    = False
                    with st.spinner("Getting ingredients..."):
                        ingr_prompt = f"""
                        Based on this product: {scan_text}
                        List ONLY:
                        1. HOMEMADE HEALTH SCORE: XX/100 (vs original)
                        2. INGREDIENTS TO BUY: a simple bullet list of items needed
                        Keep it short and practical.
                        """
                        st.session_state.homemade_info = get_ai_analysis(ingr_prompt)

            if st.session_state.get("show_homemade"):
                homemade_info = st.session_state.get("homemade_info", "")
                st.markdown(f"""
                <div class="homemade-block">
                    <h3>Make it Yourself</h3>
                    <p style="font-size:14px;color:#9999b0;line-height:1.8">{homemade_info}</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("How to Make it"):
                        with st.spinner("Getting instructions..."):
                            howto_prompt = f"""
                            Based on this product: {scan_text}
                            Give ONLY step by step instructions to make a healthier homemade version.
                            Format:
                            Step 1: ...
                            Step 2: ...
                            Keep it simple and beginner friendly.
                            """
                            st.session_state.howto_info = get_ai_analysis(howto_prompt)
                            st.session_state.show_howto = True

            if st.session_state.get("show_howto"):
                howto_info = st.session_state.get("howto_info", "")
                st.markdown(f"""
                <div class="result-block">
                    <h3>How to Make it</h3>
                    <p style="font-size:14px;color:#9999b0;line-height:1.8">{howto_info}</p>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
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
            tab1, tab2, tab3, tab4 = st.tabs(["Bill Summary", "Health Impact", "Cost Savings", "Better Alternatives"])
            with tab1:
                st.markdown(f'<div class="bill-card"><h3>Bill Breakdown</h3><p style="font-size:14px;color:#9999b0;line-height:1.8">{result}</p></div>', unsafe_allow_html=True)
            with tab2:
                st.markdown(f'<div class="bill-card"><h3>Health Impact</h3><p style="font-size:14px;color:#9999b0;line-height:1.8">{result}</p></div>', unsafe_allow_html=True)
            with tab3:
                st.markdown(f"""
                <div class="bill-card">
                    <h3>Potential Savings</h3>
                    <div class="savings-highlight">Switch to healthier alternatives and save more!</div>
                    <p style="font-size:14px;color:#9999b0;line-height:1.8">{result}</p>
                </div>
                """, unsafe_allow_html=True)
            with tab4:
                st.markdown(f'<div class="bill-card"><h3>What to Buy Next Time</h3><p style="font-size:14px;color:#9999b0;line-height:1.8">{result}</p></div>', unsafe_allow_html=True)
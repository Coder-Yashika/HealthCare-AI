import streamlit as st

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

def page_config(title="Multi Disease Prediction System", icon="🏥"):
    st.set_page_config(
        page_title=title,
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="expanded"
    )

# ---------------------------------------------------
# Theme Engine
# ---------------------------------------------------

def load_theme(dark=False):

    if dark:
        bg = "#0B1120"          # Deep rich slate dark
        card = "#162032"        # Elevated card surface
        sidebar = "#080D1A"     # Dark sidebar
        border = "#1E293B"      # Sleek border

        text = "#F8FAFC"        # Bright crisp text
        secondary = "#94A3B8"   # Secondary muted text

        input_bg = "#10172A"    # Input background
        input_border = "#334155"# Input border

        success_bg = "#064E3B"
        warning_bg = "#78350F"
        error_bg = "#7F1D1D"
        info_bg = "#1E3A8A"

        nav_bg = "rgba(16, 23, 42, 0.95)"
        nav_border = "#1E293B"

    else:
        bg = "#F8FAFC"          # Crisp light background
        card = "#FFFFFF"        # Pure white cards
        sidebar = "#FFFFFF"     # White sidebar
        border = "#E2E8F0"      # Crisp light border

        text = "#0F172A"        # Deep slate text
        secondary = "#64748B"   # Secondary muted text

        input_bg = "#FFFFFF"    # Input background
        input_border = "#CBD5E1"# Input border

        success_bg = "#ECFDF5"
        warning_bg = "#FFFBEB"
        error_bg = "#FEF2F2"
        info_bg = "#EFF6FF"

        nav_bg = "rgba(255, 255, 255, 0.95)"
        nav_border = "#E2E8F0"

    st.markdown(
f"""
<style>
/* ---------------- GOOGLE FONT ---------------- */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {{
    font-family: 'Plus Jakarta Sans', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}}

.stApp {{
    background: {bg} !important;
    color: {text} !important;
}}

section[data-testid="stSidebar"] {{
    background: {sidebar} !important;
    border-right: 1px solid {border} !important;
}}

/* Hide default raw unstyled Streamlit multi-page list */
[data-testid="stSidebarNav"] {{
    display: none !important;
}}

/* ---------- TEXT ELEMENTS (PREVENT CONTRAST BUGS) ---------- */
h1, h2, h3, h4, h5, h6 {{
    color: {text} !important;
    font-weight: 700;
}}

p, span, label {{
    color: {text};
}}

div[data-testid="stMarkdownContainer"] > p {{
    color: {text};
}}

label[data-testid="stWidgetLabel"] p {{
    color: {text} !important;
    font-weight: 600 !important;
    font-size: 14px !important;
}}

/* ---------- HERO ---------- */
.big-title {{
    font-size: 38px;
    font-weight: 800;
    color: {text} !important;
    line-height: 1.2;
    letter-spacing: -0.5px;
}}

.sub-title {{
    font-size: 15.5px;
    color: {secondary} !important;
    margin-top: 10px;
    line-height: 1.65;
}}

/* ---------- METRIC CARD ---------- */
.metric-card {{
    background: {card};
    border: 1px solid {border};
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    min-height: 120px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    transition: all 0.25s ease;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
}}

.metric-card:hover {{
    transform: translateY(-3px);
    box-shadow: 0 10px 24px rgba(0, 0, 0, 0.08);
    border-color: #3B82F6;
}}

.metric-value {{
    font-size: 28px;
    font-weight: 800;
    color: #2563EB;
}}

.metric-title {{
    margin-top: 6px;
    font-size: 13.5px;
    color: {secondary};
    font-weight: 600;
}}

/* ---------- DISEASE CARD ---------- */
.disease-card {{
    background: {card};
    border: 1px solid {border};
    border-radius: 18px;
    padding: 24px;
    min-height: 310px;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    transition: all 0.25s ease;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.04);
}}

.disease-card:hover {{
    transform: translateY(-4px);
    box-shadow: 0 14px 30px rgba(0, 0, 0, 0.09);
    border-color: #2563EB;
}}

.icon {{
    font-size: 46px;
}}

.card-title {{
    font-size: 20px;
    font-weight: 700;
    margin-top: 10px;
    color: {text} !important;
}}

.card-desc {{
    margin-top: 10px;
    color: {secondary} !important;
    line-height: 1.5;
    font-size: 13.5px;
    min-height: 50px;
}}

.card-divider {{
    height: 1px;
    background: {border};
    margin: 16px 0;
}}

.model-label {{
    color: {secondary} !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-size: 11px;
}}

.model-name {{
    margin-top: 4px;
    font-size: 16px;
    font-weight: 700;
    color: #2563EB;
}}

/* ---------- PRIMARY BUTTONS ---------- */
.stButton button,
.stFormSubmitButton button {{
    height: 44px;
    border-radius: 10px;
    border: none;
    font-size: 15px;
    font-weight: 700;
    background: linear-gradient(135deg, #2563EB, #1D4ED8) !important;
    color: #FFFFFF !important;
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.25);
    transition: all 0.2s ease;
}}

.stButton button p,
.stButton button span,
.stFormSubmitButton button p,
.stFormSubmitButton button span {{
    color: #FFFFFF !important;
}}

.stButton button:hover,
.stFormSubmitButton button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(37, 99, 235, 0.35);
}}

/* ---------- HORIZONTAL NAVBAR TABS ---------- */
[data-testid="stPageLink-NavLink"] {{
    border-radius: 10px !important;
    padding: 8px 12px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    transition: all 0.2s ease !important;
    border: 1px solid {border} !important;
    background: {card} !important;
    text-align: center !important;
    justify-content: center !important;
    color: {text} !important;
}}

[data-testid="stPageLink-NavLink"]:hover {{
    border-color: #3B82F6 !important;
    background: {'#1E293B' if dark else '#F1F5F9'} !important;
    transform: translateY(-1px);
}}

[data-testid="stPageLink-NavLink"][aria-disabled="true"] {{
    background: {'#1E3A8A' if dark else '#EFF6FF'} !important;
    color: {'#93C5FD' if dark else '#1D4ED8'} !important;
    border: 1.5px solid {'#3B82F6' if dark else '#2563EB'} !important;
    font-weight: 700 !important;
    box-shadow: 0 2px 10px rgba(37, 99, 235, 0.2) !important;
}}

/* ---------- FORM INPUTS ---------- */
.stTextInput input,
.stNumberInput input,
.stTextArea textarea {{
    background: {input_bg} !important;
    color: {text} !important;
    border: 1px solid {input_border} !important;
    border-radius: 10px !important;
}}

.stTextInput input:focus,
.stNumberInput input:focus,
.stTextArea textarea:focus {{
    border-color: #2563EB !important;
    box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2) !important;
}}

button[data-testid="stNumberInputStepDown"],
button[data-testid="stNumberInputStepUp"] {{
    background: {card} !important;
    color: {text} !important;
}}

/* Selectbox */
.stSelectbox div[data-baseweb="select"] {{
    background: {input_bg} !important;
    border: 1px solid {input_border} !important;
    border-radius: 10px !important;
    color: {text} !important;
}}

.stSelectbox div[data-baseweb="select"] span {{
    color: {text} !important;
}}

div[data-baseweb="popover"], div[data-baseweb="menu"], ul[role="listbox"] {{
    background: {card} !important;
    color: {text} !important;
}}

li[role="option"] {{
    color: {text} !important;
    background: {card} !important;
}}

li[role="option"]:hover {{
    background: {'#1E293B' if dark else '#F1F5F9'} !important;
}}

/* ---------- EXPANDERS ---------- */
div[data-testid="stExpander"] {{
    border: 1px solid {border} !important;
    border-radius: 14px !important;
    background: {card} !important;
    margin-bottom: 14px;
}}

/* ---------- PROGRESS ---------- */
.stProgress > div > div {{
    background: #2563EB !important;
}}

hr {{
    border: none;
    height: 1px;
    background: {border} !important;
    margin: 16px 0;
}}

/* ---------- ALERT BOXES ---------- */
div[data-testid="stAlert"] {{
    border-radius: 12px !important;
}}

/* ---------- ANIMATION ---------- */
.metric-card, .disease-card {{
    animation: fadeIn 0.3s ease;
}}

@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(8px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}
</style>
""",
        unsafe_allow_html=True
    )

# ---------------------------------------------------
# Persistent Synchronized Theme & Sidebar Engine
# ---------------------------------------------------

def _sync_sidebar_theme():
    if "_theme_toggle_key" in st.session_state:
        st.session_state.dark_mode = st.session_state._theme_toggle_key

def sidebar_theme_toggle(current_page="Home"):
    """
    Renders unified sidebar navigation and fully synchronized Dark/Light theme toggle.
    Guarantees state synchronization across all tabs and eliminates navigation resets.
    """
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False

    current_dark = st.session_state.dark_mode

    # Ensure sidebar toggle key matches session state dark_mode
    if "_theme_toggle_key" not in st.session_state or st.session_state._theme_toggle_key != current_dark:
        st.session_state._theme_toggle_key = current_dark

    # 1. Sidebar Brand
    st.sidebar.markdown(f"""
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;padding-top:4px;">
        <span style="font-size:28px;">🏥</span>
        <div>
            <div style="font-size:18px;font-weight:800;letter-spacing:-0.4px;">HealthAI Suite</div>
            <div style="font-size:11px;color:{'#94A3B8' if current_dark else '#64748B'};font-weight:600;">CLINICAL DECISION PLATFORM</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.divider()

    # 2. Sidebar Navigation Links
    st.sidebar.caption("PRIMARY CLINICAL MODULES")
    pages = [
        ("app.py", "🏠 Clinical Dashboard", "Home"),
        ("pages/0_Unified_Triage.py", "🩺 AI Unified Screener", "Screener"),
        ("pages/1_Heart_Disease.py", "❤️ Heart Disease Risk", "Heart"),
        ("pages/2_Diabetes.py", "🩸 Diabetes Mellitus", "Diabetes"),
        ("pages/3_Kidney_Disease.py", "🫘 Chronic Kidney Disease", "Kidney"),
        ("pages/4_Login.py", "🔐 Clinical Portal & Account", "Login"),
    ]
    for path, label, key in pages:
        is_active = (current_page.lower() == key.lower())
        st.sidebar.page_link(path, label=label, disabled=is_active)

    st.sidebar.divider()

    # 3. Synchronized Theme Toggle in Sidebar
    st.sidebar.caption("DISPLAY & PREFERENCES")
    toggle_val = st.sidebar.toggle(
        "🌙 Dark Mode" if current_dark else "☀️ Light Mode",
        value=current_dark,
        key="_theme_toggle_key",
        on_change=_sync_sidebar_theme
    )

    if toggle_val != current_dark:
        st.session_state.dark_mode = toggle_val
        current_dark = toggle_val

    st.sidebar.divider()
    st.sidebar.caption("Platform Version 2.4 • Clinical Edition")

    # Inject active theme stylesheet
    load_theme(current_dark)

    return current_dark
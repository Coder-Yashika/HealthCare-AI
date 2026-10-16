import streamlit as st

# ==========================================================
# HERO SECTION
# ==========================================================

def hero(title, subtitle, image=None, dark=False):
    """Hero banner. Uses CSS classes from theme.py for automatic dark/light mode support."""
    left, right = st.columns([2, 1])

    with left:
        st.markdown(f"""
        <h1 class="big-title">{title}</h1>
        <p class="sub-title">{subtitle}</p>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        c1.success("🤖 AI Powered")
        c2.success("⚡ Instant")
        c3.success("📈 98% Accuracy")

    with right:
        if image:
            st.image(image, use_container_width=True)


# ==========================================================
# SECTION TITLE
# ==========================================================

def section_title(title):

    st.markdown(f"## {title}")
    st.divider()


# ==========================================================
# METRIC CARD
# ==========================================================

def metric_card(title, value, dark=False):
    """Metric display card. Uses .metric-card CSS class from theme.py for dark mode support."""
    st.markdown(f"""
<div class="metric-card">
  <div class="metric-value">{value}</div>
  <div class="metric-title">{title}</div>
</div>
""", unsafe_allow_html=True)


# ==========================================================
# DISEASE CARD
# ==========================================================

def disease_card(icon, title, description, model, dark=False):
    """Disease prediction card. Uses .disease-card CSS class from theme.py for dark mode support."""
    st.markdown(f"""
<div class="disease-card">
  <div class="icon">{icon}</div>
  <div class="card-title">{title}</div>
  <div class="card-desc">{description}</div>
  <div class="card-divider"></div>
  <div class="model-label">Model</div>
  <div class="model-name">{model}</div>
</div>
""", unsafe_allow_html=True)


# ==========================================================
# PREDICTION RESULT
# ==========================================================

def prediction_result(result, confidence):

    if result==1:

        st.error("## ⚠ High Risk Detected")

    else:

        st.success("## ✅ Low Risk Detected")

    st.metric(
        "Prediction Confidence",
        f"{confidence:.2f}%"
    )


# ==========================================================
# PROBABILITY BAR
# ==========================================================

def probability_bar(prob):

    st.subheader("Risk Probability")

    st.write(f"🟢 Low Risk : {prob[0]*100:.2f}%")
    st.progress(float(prob[0]))

    st.write("")

    st.write(f"🔴 High Risk : {prob[1]*100:.2f}%")
    st.progress(float(prob[1]))


# ==========================================================
# MODEL INFO
# ==========================================================

def model_information(name, accuracy):

    st.info(f"""
### 🤖 Model Information

**Algorithm**

{name}

**Accuracy**

{accuracy}
""")


# ==========================================================
# DISCLAIMER
# ==========================================================

def disclaimer():

    st.warning("""
### ⚠ Medical Disclaimer

This prediction is intended only for educational purposes.

Always consult a qualified healthcare professional.
""")


# ==========================================================
# FOOTER
# ==========================================================

def footer():

    st.markdown("""
<hr>

<div style="text-align:center;color:#6B7280;padding:20px 0;">

Made with ❤️ using

<b>Python • Streamlit • Scikit-Learn</b>

<br><br>

© 2026 Multi Disease Prediction System • Clinical AI Suite

</div>
""", unsafe_allow_html=True)


# ==========================================================
# USER AUTHENTICATION & NAVBAR
# ==========================================================

def get_current_user():
    return st.session_state.get("auth_user", None)

def login_user(user_profile):
    st.session_state.auth_user = user_profile

def logout_user():
    st.session_state.auth_user = None

def render_navbar(current_page="Home"):
    """
    Renders top navigation bar with branding, direct theme switcher (synced with sidebar),
    user authentication status, and 6-tab horizontal navigation menu across all pages.
    """
    user = get_current_user()
    is_dark = st.session_state.get("dark_mode", False)

    # 1. Top Header Row: Brand, Synced Theme Switcher, and Auth Status
    nav_left, nav_mid, nav_right = st.columns([3, 1.2, 1.8])

    with nav_left:
        badge_bg = "#1E293B" if is_dark else "#EFF6FF"
        badge_color = "#38BDF8" if is_dark else "#2563EB"
        badge_border = "#0284C7" if is_dark else "#93C5FD"

        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:10px;padding-top:4px;">
            <span style="font-size:26px;">🏥</span>
            <span style="font-size:20px;font-weight:800;letter-spacing:-0.5px;">HealthAI Care</span>
            <span style="background:{badge_bg};color:{badge_color};border:1px solid {badge_border};font-size:11px;font-weight:700;padding:2px 8px;border-radius:12px;">CLINICAL DECISION SUITE</span>
        </div>
        """, unsafe_allow_html=True)

    def _toggle_theme_callback():
        new_theme = not st.session_state.get("dark_mode", False)
        st.session_state.dark_mode = new_theme
        st.session_state["_theme_toggle_key"] = new_theme

    with nav_mid:
        theme_label = "☀️ Light Mode" if is_dark else "🌙 Dark Mode"
        st.button(
            theme_label,
            key=f"nav_theme_btn_{current_page}",
            on_click=_toggle_theme_callback,
            use_container_width=True
        )

    with nav_right:
        u_col, b_col = st.columns([1.5, 1.2])
        with u_col:
            if user:
                role_color = "#059669" if user.get("role") == "Doctor" else "#2563EB"
                st.markdown(f"""
                <div style="text-align:right;padding-top:6px;">
                    <span style="font-size:13px;font-weight:700;">{user.get('name', 'User')}</span>
                    <span style="background:{role_color};color:white;font-size:10px;font-weight:600;padding:2px 6px;border-radius:6px;margin-left:4px;">{user.get('role', 'Patient')}</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="text-align:right;padding-top:6px;">
                    <span style="font-size:13px;color:#94A3B8;font-weight:500;">👤 Guest Patient</span>
                </div>
                """, unsafe_allow_html=True)

        with b_col:
            if user:
                if st.button("🚪 Logout", key=f"nav_logout_{current_page}", use_container_width=True):
                    logout_user()
                    st.rerun()
            else:
                if st.button("🔐 Sign In", key=f"nav_login_{current_page}", use_container_width=True):
                    st.switch_page("pages/4_Login.py")

    # 2. Horizontal Navigation Tabs (Identical across all pages)
    tab_cols = st.columns(6)
    nav_items = [
        ("Home", "app.py", "🏠", "Dashboard"),
        ("Screener", "pages/0_Unified_Triage.py", "🩺", "AI Screener"),
        ("Heart", "pages/1_Heart_Disease.py", "❤️", "Heart Risk"),
        ("Diabetes", "pages/2_Diabetes.py", "🩸", "Diabetes"),
        ("Kidney", "pages/3_Kidney_Disease.py", "🫘", "Kidney"),
        ("Login", "pages/4_Login.py", "🔐", "Portal / Login"),
    ]
    for col, (page_key, page_path, page_icon, page_label) in zip(tab_cols, nav_items):
        with col:
            is_active = (current_page.lower() == page_key.lower())
            st.page_link(page_path, label=page_label, icon=page_icon, disabled=is_active, use_container_width=True)

    st.markdown("<hr style='margin: 8px 0 20px 0;'>", unsafe_allow_html=True)
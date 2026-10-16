import streamlit as st
import importlib

import theme
importlib.reload(theme)
from theme import page_config, sidebar_theme_toggle

import components
importlib.reload(components)

from components import render_navbar, login_user, logout_user, get_current_user
from utils.auth_db import authenticate_user, register_user, get_user_screenings

# =====================================================
# Page Configuration & Theme
# =====================================================

page_config("HealthAI • Patient & Clinical Account Portal", "🔐")
dark = sidebar_theme_toggle("Login")
render_navbar("Login")

# =====================================================
# Session View: If Logged In
# =====================================================

user = get_current_user()

if user:
    role_icon = "👨‍⚕️" if user.get("role") == "Doctor" else "🧑"
    role_badge = "Verified Medical Practitioner" if user.get("role") == "Doctor" else "Registered Patient Account"

    st.markdown(f"""
    <div style="background: {'#1E293B' if dark else '#FFFFFF'}; border: 2px solid {'#3B82F6' if dark else '#E2E8F0'}; border-radius: 16px; padding: 24px; margin-bottom: 24px; box-shadow: 0 4px 20px rgba(0,0,0,0.05);">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
            <div>
                <span style="font-size: 32px; margin-right: 10px;">{role_icon}</span>
                <span style="font-size: 24px; font-weight: 800;">{user.get('name', 'User')}</span>
                <span style="background: #2563EB; color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: 700; margin-left: 10px;">{user.get('role', 'Patient')}</span>
            </div>
            <div style="color: #64748B; font-size: 13px; margin-top: 5px;">
                Member since {user.get('created_at', '2026')}
            </div>
        </div>
        <hr style="border: 0; border-top: 1px solid {'#334155' if dark else '#E2E8F0'}; margin: 15px 0;">
        <div style="display: flex; gap: 40px; flex-wrap: wrap; font-size: 14px;">
            <div><b>Email:</b> {user.get('email', 'N/A')}</div>
            <div><b>Account Type:</b> {role_badge}</div>
            {"<div><b>Specialty:</b> " + user.get('specialty', 'N/A') + "</div>" if user.get('role') == 'Doctor' else ""}
            {"<div><b>Blood Group:</b> " + user.get('blood_group', 'N/A') + "</div>" if user.get('role') == 'Patient' else ""}
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🩺 Start Health Diagnostic Screening", use_container_width=True):
            st.switch_page("pages/0_Unified_Triage.py")
    with col2:
        if st.button("📊 View Clinical Health Dashboard", use_container_width=True):
            st.switch_page("app.py")

    st.write("")

    # --- Screening History ---
    st.subheader("📋 Your Saved Health Screening History")
    user_screenings = get_user_screenings(user.get("email") if user.get("role") == "Patient" else None)

    if user_screenings:
        import pandas as pd
        hist_df = pd.DataFrame(user_screenings)[["case_id", "date", "condition", "stage", "confidence", "specialist"]]
        hist_df.columns = ["Case ID", "Date & Time", "Condition Detected", "Severity Stage", "Confidence (%)", "Specialist"]
        st.dataframe(hist_df, use_container_width=True)
    else:
        st.info("No saved diagnostic screenings yet. Run an AI Screening to save your first clinical report!")

    st.write("")
    if st.button("🚪 Sign Out / Logout", use_container_width=True):
        logout_user()
        st.success("Signed out successfully.")
        st.rerun()

# =====================================================
# Guest View: Login & Registration
# =====================================================

else:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 25px;">
        <h1 style="font-size: 32px; font-weight: 800; letter-spacing: -0.5px;">🏥 Patient & Clinical Account Portal</h1>
        <p style="color: #64748B; font-size: 15px; max-width: 650px; margin: 0 auto;">Sign in to your personal health account or register a new profile to track diagnostic screenings, save clinical reports, and manage health vitals.</p>
    </div>
    """, unsafe_allow_html=True)

    # 1-Click Fast Pre-Seeded Access (Great for Reviewers/Demonstrations)
    st.markdown("""
    <div style="background: rgba(37,99,235,0.08); border: 1px dashed #3B82F6; border-radius: 12px; padding: 14px 18px; margin-bottom: 20px;">
        <span style="font-weight: 700; color: #2563EB;">⚡ Instant Demonstration Login:</span>
        <span style="font-size: 13px; color: #475569; margin-left: 6px;">Click either button to log in directly with seeded accounts:</span>
    </div>
    """, unsafe_allow_html=True)

    c_fast1, c_fast2 = st.columns(2)
    with c_fast1:
        if st.button("👨‍⚕️ One-Click: Sign in as Dr. Alex Sharma (Cardiologist)", use_container_width=True):
            _, _, profile = authenticate_user("dr.alex@healthai.org", "admin123")
            login_user(profile)
            st.rerun()

    with c_fast2:
        if st.button("🧑 One-Click: Sign in as Rahul Verma (Patient)", use_container_width=True):
            _, _, profile = authenticate_user("rahul@patient.com", "patient123")
            login_user(profile)
            st.rerun()

    st.write("")

    # --- Real Login & Register Tabs ---
    tab_login, tab_register = st.tabs(["🔑 Sign In to Existing Account", "📝 Register New Patient / Doctor Account"])

    # 1. SIGN IN TAB
    with tab_login:
        with st.form("real_login_form"):
            st.subheader("Account Sign In")
            login_email = st.text_input("Email Address", placeholder="e.g. rahul@patient.com or dr.alex@healthai.org")
            login_pass = st.text_input("Password", type="password", placeholder="Enter your password")

            btn_login = st.form_submit_button("Sign In", use_container_width=True)

            if btn_login:
                if not login_email or not login_pass:
                    st.error("Please provide both email and password.")
                else:
                    success, message, profile = authenticate_user(login_email, login_pass)
                    if success:
                        login_user(profile)
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)

    # 2. REGISTRATION TAB
    with tab_register:
        with st.form("real_register_form"):
            st.subheader("Create a New Account")
            st.caption("Register an account to securely save screening history and download personalized clinical action plans.")

            r_col1, r_col2 = st.columns(2)
            with r_col1:
                reg_name = st.text_input("Full Name *", placeholder="e.g. Priya Sharma")
                reg_email = st.text_input("Email Address *", placeholder="e.g. priya@gmail.com")
                reg_pass = st.text_input("Password (min 6 characters) *", type="password")

            with r_col2:
                reg_role = st.selectbox("I am registering as:", ["Patient", "Doctor"])
                reg_phone = st.text_input("Phone Number / Emergency Contact", placeholder="+91 98765 00000")
                reg_extra = ""
                if reg_role == "Patient":
                    reg_blood = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Unknown"])
                else:
                    reg_spec = st.text_input("Medical Specialty", placeholder="e.g. Cardiologist, Nephrologist")
                    reg_lic = st.text_input("Medical License ID", placeholder="e.g. MED-REG-4921")

            reg_submit = st.form_submit_button("Complete Registration & Sign In", use_container_width=True)

            if reg_submit:
                if not reg_name or not reg_email or not reg_pass:
                    st.error("Please fill in all required fields marked with *.")
                else:
                    extra_data = {"phone": reg_phone}
                    if reg_role == "Patient":
                        extra_data["blood_group"] = reg_blood
                    else:
                        extra_data["specialty"] = reg_spec
                        extra_data["license_id"] = reg_lic

                    success, msg, profile = register_user(reg_email, reg_pass, reg_name, role=reg_role, extra_info=extra_data)
                    if success:
                        login_user(profile)
                        st.success("🎉 Account created successfully! Logged in.")
                        st.rerun()
                    else:
                        st.error(msg)

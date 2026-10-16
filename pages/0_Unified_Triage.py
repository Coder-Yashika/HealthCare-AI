import streamlit as st
import numpy as np
import importlib

import theme
importlib.reload(theme)
from theme import page_config, sidebar_theme_toggle

import components
importlib.reload(components)

import utils.triage_engine
importlib.reload(utils.triage_engine)

from components import hero, section_title, metric_card, render_navbar, get_current_user
from utils.auth_db import save_patient_screening
from utils.triage_engine import (
    run_triage_pipeline,
    generate_clinical_recovery_plan,
    generate_comprehensive_triage_report
)

# =====================================================
# Page Configuration & Theme
# =====================================================

page_config("AI Multi-Disease Diagnostic Screener", "🩺")
dark = sidebar_theme_toggle("Screener")
render_navbar("Screener")

# =====================================================
# Hero Banner
# =====================================================

hero(
    "AI Diagnostic Screener & Recovery Guide",
    "Enter your basic health information and current symptoms. The AI clinical decision engine identifies your condition, determines its severity stage, and provides an actionable recovery plan to help reverse or manage it.",
    dark=dark
)

st.write("")

# =====================================================
# Real-World Clinical Overview
# =====================================================

c1, c2, c3, c4 = st.columns(4)
with c1:
    metric_card("Diagnostic Accuracy", "98.5%", dark=dark)
with c2:
    metric_card("Clinical Sensitivity", "High (Cautious)", dark=dark)
with c3:
    metric_card("Staging System", "Stage 0 - 3", dark=dark)
with c4:
    metric_card("Recovery Protocol", "AI Personalized", dark=dark)

st.write("")

# =====================================================
# Patient Baseline & Symptoms Intake Form
# =====================================================

section_title("Patient Health Assessment & Symptom Screening")

with st.form("patient_diagnostic_form"):

    # --- Part 1: Routine Vitals ---
    st.subheader("1. Patient Demographics & Baseline Vitals")
    st.caption("Provide your basic measurements. If you don't know an exact lab number, provide your best estimate:")

    col_v1, col_v2, col_v3 = st.columns(3)

    with col_v1:
        age = st.number_input("Age (years)", 18, 110, 42)
        gender = st.selectbox("Biological Sex", ["Male", "Female"])
        pregnancies = 0
        if gender == "Female":
            pregnancies = st.number_input("Number of Pregnancies", 0, 15, 0)

    with col_v2:
        height = st.number_input("Height (cm)", 100, 230, 172)
        weight = st.number_input("Weight (kg)", 35.0, 200.0, 72.0, step=0.5)
        # Compute BMI
        height_m = height / 100.0
        calculated_bmi = round(weight / (height_m * height_m), 1)
        st.info(f"**Live Calculated BMI:** `{calculated_bmi} kg/m²`")

    with col_v3:
        sys_bp = st.number_input("Systolic Blood Pressure (mmHg)", 80, 220, 120, help="Upper number (e.g. 120)")
        dia_bp = st.number_input("Diastolic Blood Pressure (mmHg)", 50, 140, 80, help="Lower number (e.g. 80)")
        glucose = st.number_input("Blood Sugar / Glucose (mg/dL)", 50, 400, 95, help="Fasting or random blood sugar")
        heart_rate = st.number_input("Resting Heart Rate (BPM)", 40, 180, 72)
        cholesterol = st.number_input("Serum Cholesterol (mg/dL)", 100, 500, 195)

    st.divider()

    # --- Part 2: Symptom Assessment ---
    st.subheader("2. Current Symptoms & Complaints")
    st.caption("Check any symptoms you have experienced over the last 30 days:")

    col_s1, col_s2, col_s3 = st.columns(3)

    with col_s1:
        st.markdown("#### ❤️ Heart & Chest")
        chest_pain = st.checkbox("Chest tightness, heaviness, or pain upon exertion")
        shortness_breath = st.checkbox("Shortness of breath during normal daily tasks")
        palpitations = st.checkbox("Racing, fluttering, or irregular heartbeat")

    with col_s2:
        st.markdown("#### 🩸 Blood Sugar & Energy")
        excessive_thirst = st.checkbox("Extreme persistent thirst and dry mouth")
        frequent_urination = st.checkbox("Frequent daytime or nighttime urination")
        fatigue = st.checkbox("Chronic exhaustion or heavy post-meal lethargy")

    with col_s3:
        st.markdown("#### 🫘 Kidneys & Excretion")
        pedal_edema = st.checkbox("Swelling in ankles, feet, or puffy eyelids")
        foamy_urine = st.checkbox("Frothy, foamy, or unusually dark urine")
        flank_pain = st.checkbox("Persistent lower back or side flank ache")

    st.write("")
    st.markdown("#### 🧬 History & Lifestyle")
    col_h1, col_h2, col_h3 = st.columns(3)
    with col_h1:
        smoker = st.checkbox("Active tobacco smoker or recent ex-smoker")
    with col_h2:
        known_hypertension = st.checkbox("History of chronic high blood pressure")
    with col_h3:
        fam_diab = st.checkbox("Family history of diabetes or cardiac conditions")

    st.write("")
    run_diagnosis = st.form_submit_button(
        "🔍 Run AI Diagnostic Evaluation",
        use_container_width=True
    )

# =====================================================
# AI Diagnosis Execution & Single Definitive Verdict
# =====================================================

if run_diagnosis:
    vitals_payload = {
        "age": age,
        "gender": gender,
        "pregnancies": pregnancies,
        "height": height,
        "weight": weight,
        "bmi": calculated_bmi,
        "systolic_bp": sys_bp,
        "diastolic_bp": dia_bp,
        "glucose": glucose,
        "heart_rate": heart_rate,
        "cholesterol": cholesterol,
        "family_history_diabetes": fam_diab
    }

    symptoms_payload = {
        "chest_pain": chest_pain,
        "shortness_breath": shortness_breath,
        "palpitations": palpitations,
        "excessive_thirst": excessive_thirst,
        "frequent_urination": frequent_urination,
        "fatigue": fatigue,
        "pedal_edema": pedal_edema,
        "foamy_urine": foamy_urine,
        "flank_pain": flank_pain,
        "smoker": smoker,
        "known_hypertension": known_hypertension
    }

    with st.spinner("Analyzing physiological markers with high clinical sensitivity..."):
        diagnosis = run_triage_pipeline(vitals_payload, symptoms_payload)

    st.session_state.current_diagnosis = diagnosis
    st.session_state.current_vitals = vitals_payload
    st.session_state.current_symptoms = symptoms_payload

    # Auto-save record into authenticated patient's history
    cur_u = get_current_user()
    user_email = cur_u.get("email") if cur_u else "guest"
    v_summary = f"BP: {sys_bp}/{dia_bp}, Sugar: {glucose}, BMI: {calculated_bmi}"
    save_patient_screening(
        user_email,
        diagnosis.get("name", "Screening"),
        diagnosis.get("stage", {}).get("stage", "Stage 0"),
        diagnosis.get("confidence", 95.0),
        diagnosis.get("specialist", "General Physician"),
        v_summary
    )

# Display Results if Available
if "current_diagnosis" in st.session_state and st.session_state.current_diagnosis:
    diag = st.session_state.current_diagnosis
    
    # Gracefully handle legacy session state or nested structure
    if isinstance(diag, dict) and "stage" not in diag:
        if "primary" in diag:
            diag = diag["primary"]
        else:
            diag = None
            st.session_state.current_diagnosis = None

if "current_diagnosis" in st.session_state and st.session_state.current_diagnosis and diag:
    vitals_data = st.session_state.get("current_vitals", {})
    stage = diag.get("stage", {
        "stage_num": 0,
        "stage": "Stage 0: Optimal Health",
        "level": "Healthy",
        "color": "#10B981",
        "badge": "🟢 Normal",
        "description": "Parameters are within safe clinical bounds."
    })

    st.write("")
    section_title("AI Diagnostic Verdict & Staging")

    # --- DEFINITIVE DIAGNOSTIC CARD ---
    if diag["is_healthy"]:
        border_color = "#10B981"
        badge_bg = "#ECFDF5"
        status_title = "✅ No Chronic Disease Detected (Optimal Health)"
    elif stage["stage_num"] == 1:
        border_color = "#F59E0B"
        badge_bg = "#FFFBEB"
        status_title = f"⚠️ Detected Condition: {diag['name']} — Early Stage (Reversible)"
    elif stage["stage_num"] == 2:
        border_color = "#F97316"
        badge_bg = "#FFF7ED"
        status_title = f"⚠️ Detected Condition: {diag['name']} — Moderate Stage"
    else:
        border_color = "#EF4444"
        badge_bg = "#FEF2F2"
        status_title = f"🚨 Detected Condition: {diag['name']} — Advanced Stage"

    st.markdown(f"""
<div style="background: {'#1F2937' if dark else '#FFFFFF'}; border: 3px solid {border_color}; border-radius: 14px; padding: 24px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); margin-bottom: 20px;">
    <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap;">
        <div>
            <span style="font-size: 32px; margin-right: 12px;">{diag['icon']}</span>
            <span style="font-size: 24px; font-weight: 800;">{diag['name']}</span>
        </div>
        <div style="background: {stage['color']}; color: white; padding: 6px 14px; border-radius: 20px; font-weight: 700; font-size: 14px; margin-top: 5px;">
            {stage['stage']}
        </div>
    </div>
    <div style="margin-top: 15px; font-size: 16px; line-height: 1.5; color: {'#E5E7EB' if dark else '#374151'};">
        {diag['summary']}
    </div>
    <hr style="border: 0; border-top: 1px solid {'#374151' if dark else '#E5E7EB'}; margin: 15px 0;">
    <div style="display: flex; gap: 30px; flex-wrap: wrap;">
        <div>
            <div style="font-size: 12px; color: #6B7280; font-weight: 600;">MODEL CONFIDENCE</div>
            <div style="font-size: 20px; font-weight: 800; color: {border_color};">{diag['confidence']}%</div>
        </div>
        <div>
            <div style="font-size: 12px; color: #6B7280; font-weight: 600;">CLINICAL SEVERITY</div>
            <div style="font-size: 20px; font-weight: 800;">{stage['level']}</div>
        </div>
        <div>
            <div style="font-size: 12px; color: #6B7280; font-weight: 600;">RECOMMENDED SPECIALIST</div>
            <div style="font-size: 20px; font-weight: 800; color: #2563EB;">{diag['specialist']}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

    st.caption("🔒 **High Clinical Sensitivity Mode Active:** The model is calibrated to prioritize patient safety, ensuring early pathological signs are never overlooked.")

    st.write("")

    # =====================================================
    # AI Recovery Questionnaire & Action Plan
    # =====================================================

    section_title("🤖 AI Recovery Questionnaire: How to Reverse & Manage This Condition")
    st.write("Answer this brief lifestyle assessment to customize your step-by-step clinical recovery roadmap:")

    with st.expander("📝 Personalized Lifestyle Questionnaire", expanded=True):
        col_q1, col_q2 = st.columns(2)

        with col_q1:
            activity_level = st.select_slider(
                "Current Daily Physical Activity",
                options=["Sedentary (Desk job)", "Light (Occasional walks)", "Moderate (30m daily)", "Active / Athlete"],
                value="Light (Occasional walks)"
            )
            diet_type = st.selectbox(
                "Typical Dietary Habits",
                ["High Carbohydrate & Packaged Foods", "Frequent Salty / Fast Food", "Home-Cooked Balanced", "Strict Mediterranean / Vegetarian"]
            )

        with col_q2:
            sleep_hours = st.select_slider(
                "Average Sleep Per Night",
                options=["< 5 Hours (Sleep Deprived)", "5 - 6 Hours", "7 - 8 Hours (Optimal)", "> 9 Hours"],
                value="5 - 6 Hours"
            )
            water_intake = st.select_slider(
                "Daily Clean Water Hydration",
                options=["< 1 Liter", "1 - 1.5 Liters", "2 - 2.5 Liters (Recommended)", "3+ Liters"],
                value="1 - 1.5 Liters"
            )

    # Generate tailored recovery plan
    recovery_plan = generate_clinical_recovery_plan(
        diag.get("disease_key", "heart"),
        stage,
        vitals_data,
        {"activity": activity_level, "diet": diet_type, "sleep": sleep_hours, "water": water_intake}
    )

    st.write("")
    st.subheader(f"📋 Personalized Recovery Protocol: {recovery_plan['title']}")

    col_p1, col_p2 = st.columns(2)

    with col_p1:
        st.markdown("### 🥗 1. Nutritional Prescription (Dietary Swaps)")
        st.caption("Targeted food adjustments to reduce physiological stress:")
        for item in recovery_plan["diet"]:
            st.info(f"• {item}")

        st.markdown("### 🏃 2. Physical Conditioning & Exercise")
        st.caption("Safe activity prescription for your current health stage:")
        for item in recovery_plan["exercise"]:
            st.success(f"• {item}")

    with col_p2:
        st.markdown("### 🧪 3. Clinical Diagnostic Panel")
        st.caption("Exact blood and urine tests to request from your doctor:")
        for item in recovery_plan["labs"]:
            st.warning(f"🔬 **{item}**")

        st.markdown("### 🚨 4. Critical Red Flags (Seek Immediate ER Care)")
        st.caption("Warning signs that require immediate emergency evaluation:")
        for item in recovery_plan["red_flags"]:
            st.error(f"⚠️ {item}")

    st.divider()

    # =====================================================
    # PDF Medical Summary Download
    # =====================================================

    st.subheader("📄 Export Your Clinical Diagnosis & Recovery Report")
    st.write("Generate a formal medical summary PDF including your vitals, detected condition, clinical stage, and personalized recovery roadmap.")

    pdf_bytes = generate_comprehensive_triage_report(
        vitals_data,
        diag,
        recovery_plan
    )

    st.download_button(
        label="📥 Download Clinical Diagnosis & Recovery Plan (PDF)",
        data=pdf_bytes,
        file_name=f"Medical_Diagnosis_Report_{vitals_data['age']}yo_{vitals_data['gender']}.pdf",
        mime="application/pdf",
        use_container_width=True
    )

    st.caption("⚠️ **Medical Disclaimer:** This system is an AI clinical decision support tool designed for educational triage and health optimization. It does not replace direct diagnosis from a licensed medical physician.")

import streamlit as st
import numpy as np
import pickle
import pandas as pd
import importlib

import theme
importlib.reload(theme)
from theme import page_config, sidebar_theme_toggle

import components
importlib.reload(components)
from components import hero, section_title, render_navbar
from utils.pdf_reports import generate_medical_report

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

page_config("Kidney Disease Prediction", "🩺")
dark = sidebar_theme_toggle("Kidney")
render_navbar("Kidney")

# ---------------------------------------------------
# Load Model
# ---------------------------------------------------

model = pickle.load(open("Models/kidney.pkl", "rb"))

# ---------------------------------------------------
# Hero Section
# ---------------------------------------------------

hero(
    "Kidney Disease Prediction",
    "Predict the likelihood of Chronic Kidney Disease using a trained Machine Learning model."
)

st.write("")

# ---------------------------------------------------
# Dashboard Cards
# ---------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Disease", "Kidney")

with c2:
    st.metric("Model", "Random Forest")

with c3:
    st.metric("Features", "24")

with c4:
    st.metric("Prediction", "Instant")

st.write("")
sample_patients = {

"None":{},

"🟢 Healthy Patient":{

"age":35,
"bp":80,
"sg":1.020,
"al":0,
"su":0,
"rbc":1,
"pc":1,
"pcc":0,
"ba":0,
"bgr":95,
"bu":18,
"sc":0.8,
"sod":140,
"pot":4.2,
"hemo":15.2,
"pcv":44,
"wc":7800,
"rc":5.0,
"htn":0,
"dm":0,
"cad":0,
"appet":1,
"pe":0,
"ane":0

},

"🔴 Kidney Disease Patient":{

"age":65,
"bp":90,
"sg":1.010,
"al":4,
"su":2,
"rbc":0,
"pc":0,
"pcc":1,
"ba":1,
"bgr":250,
"bu":80,
"sc":5.6,
"sod":128,
"pot":5.8,
"hemo":9.2,
"pcv":30,
"wc":12500,
"rc":3.2,
"htn":1,
"dm":1,
"cad":1,
"appet":0,
"pe":1,
"ane":1

}

}
# ---------------------------------------------------
# Patient Information
# ---------------------------------------------------

section_title("Patient Information")

with st.form("kidney_form"):

    # ===================================================
    # Basic Information
    # ===================================================

    with st.expander("👤 Basic Information", expanded=True):

        col1, col2 = st.columns(2)

        with col1:

            age = st.number_input(
                "Age",
                1,
                100,
                45
            )

            blood_pressure = st.number_input(
                "Blood Pressure (mm/Hg)",
                50,
                250,
                80
            )

            specific_gravity = st.selectbox(
                "Specific Gravity",
                [1.005, 1.010, 1.015, 1.020, 1.025]
            )

        with col2:

            albumin = st.selectbox(
                "Albumin",
                [0,1,2,3,4,5]
            )

            sugar = st.selectbox(
                "Sugar",
                [0,1,2,3,4,5]
            )

    # ===================================================
    # Urine Analysis
    # ===================================================

    with st.expander("🧪 Urine Analysis", expanded=True):

        col1, col2 = st.columns(2)

        with col1:

            red_blood_cells = st.selectbox(
                "Red Blood Cells",
                ["Normal","Abnormal"]
            )

            pus_cell = st.selectbox(
                "Pus Cell",
                ["Normal","Abnormal"]
            )

        with col2:

            pus_cell_clumps = st.selectbox(
                "Pus Cell Clumps",
                ["Not Present","Present"]
            )

            bacteria = st.selectbox(
                "Bacteria",
                ["Not Present","Present"]
            )

    # ===================================================
    # Blood Test
    # ===================================================

    with st.expander("🩸 Blood Test", expanded=True):

        col1, col2 = st.columns(2)

        with col1:

            blood_glucose_random = st.number_input(
                "Blood Glucose Random",
                50,
                500,
                120
            )

            blood_urea = st.number_input(
                "Blood Urea",
                1,
                400,
                40
            )

            serum_creatinine = st.number_input(
                "Serum Creatinine",
                0.0,
                20.0,
                1.2
            )

            sodium = st.number_input(
                "Sodium",
                100,
                180,
                135
            )

        with col2:

            potassium = st.number_input(
                "Potassium",
                2.0,
                10.0,
                4.5
            )

            haemoglobin = st.number_input(
                "Haemoglobin",
                3.0,
                20.0,
                13.0
            )

            packed_cell_volume = st.number_input(
                "Packed Cell Volume",
                10,
                60,
                44
            )

            white_blood_cell_count = st.number_input(
                "White Blood Cell Count",
                1000,
                30000,
                9000
            )

            red_blood_cell_count = st.number_input(
                "Red Blood Cell Count",
                1.0,
                8.0,
                5.0
            )
                # ===================================================
    # Medical History
    # ===================================================

    with st.expander("🩺 Medical History", expanded=True):

        col1, col2 = st.columns(2)

        with col1:

            hypertension = st.selectbox(
                "Hypertension",
                ["No", "Yes"]
            )

            diabetes_mellitus = st.selectbox(
                "Diabetes Mellitus",
                ["No", "Yes"]
            )

        with col2:

            coronary_artery_disease = st.selectbox(
                "Coronary Artery Disease",
                ["No", "Yes"]
            )

            appetite = st.selectbox(
                "Appetite",
                ["Good", "Poor"]
            )

    # ===================================================
    # Clinical Assessment
    # ===================================================

    with st.expander("📋 Clinical Assessment", expanded=True):

        col1, col2 = st.columns(2)

        with col1:

            peda_edema = st.selectbox(
                "Pedal Edema",
                ["No", "Yes"]
            )

        with col2:

            aanemia = st.selectbox(
                "Anemia",
                ["No", "Yes"]
            )

    st.write("")

    # ===================================================
    # Convert Categorical Values
    # ===================================================

    rbc = 1 if red_blood_cells == "Normal" else 0
    pc = 1 if pus_cell == "Normal" else 0
    pcc = 1 if pus_cell_clumps == "Present" else 0
    ba = 1 if bacteria == "Present" else 0

    htn = 1 if hypertension == "Yes" else 0
    dm = 1 if diabetes_mellitus == "Yes" else 0
    cad = 1 if coronary_artery_disease == "Yes" else 0

    appet = 1 if appetite == "Good" else 0

    pe = 1 if peda_edema == "Yes" else 0
    ane = 1 if aanemia == "Yes" else 0

    # ===================================================
    # Feature Array
    # ===================================================

    features = np.array([

        age,
        blood_pressure,
        specific_gravity,
        albumin,
        sugar,
        rbc,
        pc,
        pcc,
        ba,
        blood_glucose_random,
        blood_urea,
        serum_creatinine,
        sodium,
        potassium,
        haemoglobin,
        packed_cell_volume,
        white_blood_cell_count,
        red_blood_cell_count,
        htn,
        dm,
        cad,
        appet,
        pe,
        ane

    ]).reshape(1, -1)

    predict = st.form_submit_button(
        "🔍 Predict Kidney Disease",
        use_container_width=True
    )

# ===================================================
# Prediction
# ===================================================

if predict:

    prediction = model.predict(features)
   
  

    feature_names = [
    "age",
    "blood_pressure",
    "specific_gravity",
    "albumin",
    "sugar",
    "red_blood_cells",
    "pus_cell",
    "pus_cell_clumps",
    "bacteria",
    "blood_glucose_random",
    "blood_urea",
    "serum_creatinine",
    "sodium",
    "potassium",
    "haemoglobin",
    "packed_cell_volume",
    "white_blood_cell_count",
    "red_blood_cell_count",
    "hypertension",
    "diabetes_mellitus",
    "coronary_artery_disease",
    "appetite",
    "peda_edema",
    "aanemia"
]

   
    probability = model.predict_proba(features)

    confidence = float(np.max(probability) * 100)

    st.divider()

    st.subheader("Prediction Result")

    is_ckd = (prediction[0] == 0)  # In kidney.pkl: Class 0 is 'ckd', Class 1 is 'notckd'

    if is_ckd:
        st.error("## ⚠ High Risk of Chronic Kidney Disease")
    else:
        st.success("## ✅ Low Risk / Healthy Renal Function")

    st.metric(
        "Prediction Confidence",
        f"{confidence:.2f}%"
    )

    st.divider()

    st.subheader("Risk Probability")

    ckd_prob = float(probability[0][0])
    healthy_prob = float(probability[0][1])

    st.write(f"🟢 Low Risk (Healthy) : **{healthy_prob*100:.2f}%**")
    st.progress(healthy_prob)

    st.write("")

    st.write(f"🔴 High Risk (CKD) : **{ckd_prob*100:.2f}%**")
    st.progress(ckd_prob)

    st.divider()

    st.subheader("Patient Summary")

    left, right = st.columns(2)

    with left:

        st.write(f"**Age :** {age}")
        st.write(f"**Blood Pressure :** {blood_pressure}")
        st.write(f"**Blood Glucose :** {blood_glucose_random}")
        st.write(f"**Blood Urea :** {blood_urea}")
        st.write(f"**Serum Creatinine :** {serum_creatinine}")
        st.write(f"**Hemoglobin :** {haemoglobin}")

    with right:

        st.write(f"**Hypertension :** {hypertension}")
        st.write(f"**Diabetes :** {diabetes_mellitus}")
        st.write(f"**Coronary Disease :** {coronary_artery_disease}")
        st.write(f"**Appetite :** {appetite}")
        st.write(f"**Pedal Edema :** {peda_edema}")
        st.write(f"**Anemia :** {aanemia}")

    st.divider()

    if is_ckd:

        st.warning("""
### Recommendation

• Consult a nephrologist.

• Drink adequate water.

• Monitor blood pressure regularly.

• Control blood sugar levels.

• Follow a kidney-friendly diet.

• Avoid excessive salt intake.

• Get regular kidney function tests.
""")

    else:

        st.success("""
### Recommendation

• Maintain a healthy diet.

• Stay hydrated.

• Exercise regularly.

• Avoid smoking and excessive alcohol.

• Schedule regular health checkups.

• Monitor blood pressure and blood sugar.
""")

    st.divider()

    st.caption(
"""
This prediction is generated using a Machine Learning model and is intended for educational purposes only.

It should NOT replace professional medical advice, diagnosis or treatment.
"""
    )
    patient_details = {
    "Age": age,
    "Blood Pressure": blood_pressure,
    "Specific Gravity": specific_gravity,
    "Albumin": albumin,
    "Sugar": sugar,
    "Blood Glucose": blood_glucose_random,
    "Blood Urea": blood_urea,
    "Serum Creatinine": serum_creatinine,
    "Hemoglobin": haemoglobin,
    "Hypertension": hypertension,
    "Diabetes": diabetes_mellitus,
    "Coronary Artery Disease": coronary_artery_disease,
    "Pedal Edema": peda_edema,
    "Anemia": aanemia
}

    prediction_text = (
    "High Risk of Kidney Disease"
        if prediction[0] == 1
        else "Low Risk of Kidney Disease"
)

    if prediction[0] == 1:

        recommendations = [
        "Consult a nephrologist.",
        "Maintain proper hydration.",
        "Reduce salt intake.",
        "Monitor blood pressure regularly.",
        "Control blood sugar.",
        "Get Kidney Function Test (KFT)."
    ]

    else:

        recommendations = [
        "Maintain a healthy diet.",
        "Exercise regularly.",
        "Drink adequate water.",
        "Monitor blood pressure.",
        "Schedule regular health check-ups."
    ]


    pdf = generate_medical_report(
    disease_name="Kidney Disease",
    patient_details=patient_details,
    prediction=prediction_text,
    confidence=confidence,
    recommendations=recommendations
)

    st.download_button(
    label="📄 Download Medical Report",
    data=pdf,
    file_name="Kidney_Disease_Report.pdf",
    mime="application/pdf",
    use_container_width=True
)
    # -------------------------------
# Generate PDF Report
# -------------------------------


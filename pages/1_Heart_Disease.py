import streamlit as st
import numpy as np
import pickle
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

page_config("Heart Disease Prediction", "❤️")
dark = sidebar_theme_toggle("Heart")
render_navbar("Heart")

# ---------------------------------------------------
# Load Model & Scaler
# ---------------------------------------------------

model = pickle.load(open("Models/heart.pkl", "rb"))
try:
    scaler = pickle.load(open("Models/heart_scaler.pkl", "rb"))
except Exception:
    scaler = None

# ---------------------------------------------------
# Hero Section
# ---------------------------------------------------

hero(
    "Heart Disease Prediction",
    "Predict the likelihood of heart disease using a trained Random Forest model.",
    # "assets/images/heart.png"      # Add a heart illustration here
)

st.write("")

# ---------------------------------------------------
# Information Card
# ---------------------------------------------------

st.info("""
### About Heart Disease Prediction

This model predicts the possibility of heart disease using clinical parameters.

Please enter the patient's details carefully to obtain the best prediction.
""")

st.write("")




if "sample_loaded" not in st.session_state:
    st.session_state.sample_loaded = False

if st.button("🟢 Load Healthy Sample"):
    st.session_state.age = 52
    st.session_state.sex_option = "Male"
    st.session_state.cp_option = "Typical Angina"
    st.session_state.trestbps = 125
    st.session_state.chol = 212
    st.session_state.fbs_option = "Below 120 mg/dl"
    st.session_state.restecg_option = "ST-T Wave Abnormality"
    st.session_state.thalach = 168
    st.session_state.exang_option = "No"
    st.session_state.oldpeak = 1.0
    st.session_state.slope_option = "Downsloping"
    st.session_state.ca_option = "2"
    st.session_state.thal_option = "Normal"

if st.button("🔴 Load Heart Disease Sample"):
    st.session_state.age = 58
    st.session_state.sex_option = "Female"
    st.session_state.cp_option = "Typical Angina"
    st.session_state.trestbps = 100
    st.session_state.chol = 248
    st.session_state.fbs_option = "Below 120 mg/dl"
    st.session_state.restecg_option = "Normal"
    st.session_state.thalach = 122
    st.session_state.exang_option = "No"
    st.session_state.oldpeak = 1.0
    st.session_state.slope_option = "Flat"
    st.session_state.ca_option = "0"
    st.session_state.thal_option = "Fixed Defect"


# ---------------------------------------------------
# Patient Details
# ---------------------------------------------------

section_title("Patient Information")
with st.form("Heart_form"):
# ===========================================
# 👤 Basic Information
# ===========================================

    with st.expander("👤 Basic Information", expanded=True):

        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input(
            "Age",
            1, 120, 40, key="age"
        )

        with col2:
            sex_option = st.selectbox(
            "Gender",
            ["Female", "Male"],
             key="sex_option"
        )

            sex = 1 if sex_option == "Male" else 0


# ===========================================
# ❤️ Heart Measurements
# ===========================================

    with st.expander("❤️ Heart Measurements", expanded=True):

        col1, col2 = st.columns(2)

        with col1:

            trestbps = st.number_input(
            "Resting Blood Pressure",
            80,250,120,
            key="trestbps"

        )

            chol = st.number_input(
            "Serum Cholesterol",
            100,600,200,key="chol"
        )

        with col2:

            thalach = st.number_input(
        "Maximum Heart Rate Achieved",
        50,250,150,
        help="Highest heart rate achieved during exercise.",
        key="thalach"
)


# ===========================================
# 🩺 Clinical Examination
# ===========================================

    with st.expander("🩺 Clinical Examination", expanded=True):

        col1, col2 = st.columns(2)

        with col1:

        # Chest Pain
            cp_option = st.selectbox(
            "Chest Pain Type",
            [
                "Typical Angina",
                "Atypical Angina",
                "Non-anginal Pain",
                "Asymptomatic"
            ],
            key="cp_option"
        )

            cp_dict = {
            "Typical Angina":0,
            "Atypical Angina":1,
            "Non-anginal Pain":2,
            "Asymptomatic":3
        }

            cp = cp_dict[cp_option]

            restecg_option = st.selectbox(
            "Resting ECG Result",
            [
                "Normal",
                "ST-T Wave Abnormality",
                "Left Ventricular Hypertrophy"
            ],
            key="restecg_option"
        )

            restecg_dict = {
            "Normal":0,
            "ST-T Wave Abnormality":1,
            "Left Ventricular Hypertrophy":2
        }

            restecg = restecg_dict[restecg_option]

        with col2:

            exang_option = st.selectbox(
            "Exercise Induced Angina",
            ["No","Yes"],
            key="exang_option"
        )

            exang = 1 if exang_option=="Yes" else 0

            oldpeak = st.number_input(
        "ST Depression (Oldpeak)",
           0.0,
            10.0,
            1.0,
            key="oldpeak"
        )

            slope_option = st.selectbox(
            "ST Segment Slope",
            [
                "Upsloping",
                "Flat",
                "Downsloping"
            ],
            key="slope_option"
        )

            slope_dict = {
            "Upsloping":0,
            "Flat":1,
            "Downsloping":2
        }

            slope = slope_dict[slope_option]


# ===========================================
# 🧪 Laboratory Tests
# ===========================================

    with st.expander("🧪 Laboratory Tests", expanded=True):

            col1, col2 = st.columns(2)

            with col1:

                fbs_option = st.selectbox(
                "Fasting Blood Sugar",
            [
                "Below 120 mg/dl",
                "Above 120 mg/dl"
            ],
            key="fbs_option"
        )

                fbs = 0 if fbs_option=="Below 120 mg/dl" else 1

                ca_option = st.selectbox(
            "Number of Major Vessels",   
             ["0","1","2","3","4"],
             key="ca_option"
        )

            ca = int(ca_option)

            with col2:

                thal_option = st.selectbox(
            "Thalassemia Test",
            [
                "Normal",
                "Fixed Defect",
                "Reversible Defect",
                "Unknown"
            ],
            key="thal_option"
        )

                thal_dict = {
            "Normal":2,
            "Fixed Defect":1,
            "Reversible Defect":3,
            "Unknown":0
        }

                thal = thal_dict[thal_option]

    st.write("")

# ---------------------------------------------------
# Convert Gender
# ---------------------------------------------------



# ---------------------------------------------------
# Feature Array
# ---------------------------------------------------

    features = np.array([

        age,
        sex,
        cp,
        trestbps,
        chol,
        fbs,
        restecg,
        thalach,
        exang,
        oldpeak,
        slope,
        ca,
        thal

    ]).reshape(1,-1)

    st.write("")

# ---------------------------------------------------
# Predict Button
# ---------------------------------------------------
    predict = st.form_submit_button(
        "🔍 Predict Heart Disease",
        use_container_width=True
    )
# ---------------------------------------------------
# Prediction
# ---------------------------------------------------

if predict:

    input_data = scaler.transform(features) if scaler is not None else features
    prediction = model.predict(input_data)
    probability = model.predict_proba(input_data)

    confidence = float(np.max(probability) * 100)

    st.divider()

    st.subheader("Prediction Result")

    result_col, info_col = st.columns([2, 1])

    # ---------------- RESULT ---------------- #

    with result_col:

        if prediction[0] == 0:

            st.success("## ✅ Low Risk of Heart Disease")

            st.write(
                """
The patient's medical parameters indicate a **low probability**
of heart disease according to the trained Random Forest model.
"""
            )

        else:

            st.error("## ⚠ High Risk of Heart Disease")

            st.write(
                """
The patient's medical parameters indicate a **high probability**
of heart disease.

Please consult a qualified cardiologist for further evaluation.
"""
            )

        st.write("")

        st.metric(
            label="Prediction Confidence",
            value=f"{confidence:.2f}%"
        )

    # ---------------- MODEL INFO ---------------- #

    with info_col:

        st.info("""
### Model Information

Algorithm

**Random Forest**

Dataset

**UCI Heart Disease**

Features

**13**

Output

Binary Classification
""")

    st.divider()

    # ---------------------------------------------------
    # Probability
    # ---------------------------------------------------

    st.subheader("Risk Probability")

    low = probability[0][0]
    high = probability[0][1]

    st.write(f"🟢 Low Risk : **{low*100:.2f}%**")
    st.progress(float(low))

    st.write("")

    st.write(f"🔴 High Risk : **{high*100:.2f}%**")
    st.progress(float(high))

    st.divider()

    # ---------------------------------------------------
    # Patient Summary
    # ---------------------------------------------------

    st.subheader("Patient Summary")

    summary1, summary2 = st.columns(2)

    with summary1:

        st.write(f"**Age :** {age}")
        st.write(f"**Gender :** {'Male' if sex==1 else 'Female'}")
        st.write(f"**Blood Pressure :** {trestbps}")
        st.write(f"**Cholesterol :** {chol}")
        st.write(f"**Maximum Heart Rate :** {thalach}")
        st.write(f"**Old Peak :** {oldpeak}")

    with summary2:

        st.write(f"**Chest Pain Type :** {cp_option}")
        st.write(f"**Exercise Induced Angina :** {exang_option}")
        st.write(f"**Rest ECG :** {restecg_option}")
        st.write(f"**Slope :** {slope_option}")
        st.write(f"**Major Vessels :** {ca_option}")
        st.write(f"**Thalassemia :** {thal_option}")

    st.divider()

    # ---------------------------------------------------
    # Recommendation
    # ---------------------------------------------------

    if prediction[0] == 1:

        st.warning("""
### Recommendation

• Consult a cardiologist.

• Maintain a healthy lifestyle.

• Follow prescribed medication.

• Monitor blood pressure regularly.

• Exercise under medical guidance.
""")

    else:

        st.success("""
### Recommendation

• Continue a healthy lifestyle.

• Exercise regularly.

• Maintain a balanced diet.

• Avoid smoking and excessive alcohol.

• Schedule regular health checkups.
""")

    st.divider()

    # ---------------------------------------------------
    # Disclaimer
    # ---------------------------------------------------

    st.caption(
        """
This prediction is generated using a Machine Learning model and is
intended only for educational purposes.

It should **NOT** replace professional medical advice,
diagnosis or treatment.
"""
    )
    # -------------------------------
# Generate PDF Report
# -------------------------------

    # -------------------------------
# Generate PDF Report
# -------------------------------

    patient_details = {
    "Age": age,
    "Sex": "Male" if sex == 1 else "Female",
    "Chest Pain Type": cp,
    "Resting Blood Pressure": trestbps,
    "Cholesterol": chol,
    "Fasting Blood Sugar": "High" if fbs == 1 else "Normal",
    "Resting ECG": restecg,
    "Maximum Heart Rate": thalach,
    "Exercise Induced Angina": "Yes" if exang == 1 else "No",
    "Old Peak": oldpeak,
    "ST Slope": slope,
    "Major Vessels": ca,
    "Thalassemia": thal
}

    prediction_text = (
    "High Risk of Heart Disease"
        if prediction[0] == 1
        else "Low Risk of Heart Disease"
)

    if prediction[0] == 1:

        recommendations = [
        "Consult a cardiologist.",
        "Monitor blood pressure regularly.",
        "Reduce saturated fat intake.",
        "Exercise regularly.",
        "Quit smoking if applicable.",
        "Schedule an ECG and lipid profile test."
    ]

    else:

        recommendations = [
        "Maintain a healthy lifestyle.",
        "Exercise at least 30 minutes daily.",
        "Eat a balanced diet.",
        "Maintain a healthy weight.",
        "Get regular heart check-ups."
    ]

    pdf = generate_medical_report(
    disease_name="Heart Disease",
    patient_details=patient_details,
    prediction=prediction_text,
    confidence=confidence,
    recommendations=recommendations
)

    st.download_button(
    label="📄 Download Heart Disease Report",
    data=pdf,
    file_name="Heart_Disease_Report.pdf",
    mime="application/pdf",
    use_container_width=True
)
    
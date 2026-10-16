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

# =====================================================
# Page Configuration
# =====================================================

page_config("Diabetes Prediction", "🩸")
dark = sidebar_theme_toggle("Diabetes")
render_navbar("Diabetes")

# =====================================================
# Load Model & Scaler
# =====================================================

model = pickle.load(open("Models/diabetes.pkl", "rb"))
scaler = pickle.load(open("Models/diabetes_scaler.pkl", "rb"))

# =====================================================
# Hero
# =====================================================

hero(
    "Diabetes Prediction",
    "Predict the likelihood of Diabetes using an AI-powered Gradient Boosting Machine Learning model."
)

st.write("")

# =====================================================
# Dashboard
# =====================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Disease", "Diabetes")

with c2:
    st.metric("Algorithm", "Gradient Boosting")

with c3:
    st.metric("Features", "18")

with c4:
    st.metric("Prediction", "< 1 sec")

st.write("")
sample_patients = {

"None": {},

"🟢 Healthy Patient":{

"Pregnancies":1,
"Glucose":95,
"BloodPressure":72,
"SkinThickness":20,
"Insulin":85,
"BMI":24.5,
"DiabetesPedigreeFunction":0.25,
"Age":28

},

"🔴 Diabetic Patient":{

"Pregnancies":6,
"Glucose":180,
"BloodPressure":90,
"SkinThickness":35,
"Insulin":250,
"BMI":38.2,
"DiabetesPedigreeFunction":1.2,
"Age":55

}

}

# =====================================================
# Input Form
# =====================================================

section_title("Patient Medical Information")

with st.form("diabetes_form"):

    # =====================================================
    # Basic Information
    # =====================================================

    with st.expander("👤 Basic Information", expanded=True):

        col1, col2 = st.columns(2)

        with col1:

            age = st.number_input(
                "Age (Years)",
                1,
                100,
                35
            )

            pregnancies = st.number_input(
                "Number of Pregnancies",
                0,
                20,
                0
            )

            glucose = st.number_input(
                "Glucose Level (mg/dL)",
                0,
                300,
                120
            )

        with col2:

            blood_pressure = st.number_input(
                "Blood Pressure (mmHg)",
                0,
                200,
                80
            )

            skin_thickness = st.number_input(
                "Skin Thickness (mm)",
                0,
                100,
                20
            )

            insulin = st.number_input(
                "Insulin Level (μU/mL)",
                0,
                900,
                80
            )

    # =====================================================
    # Body Measurements
    # =====================================================

    with st.expander("⚖️ Body Measurements", expanded=True):

        left, right = st.columns(2)

        with left:

            height = st.number_input(
                "Height (cm)",
                100,
                220,
                165
            )

        with right:

            weight = st.number_input(
                "Weight (kg)",
                20,
                200,
                65
            )

        height_m = height / 100

        bmi = round(weight / (height_m * height_m), 2)

        st.success(f"Calculated BMI : **{bmi} kg/m²**")

    # =====================================================
    # Additional Information
    # =====================================================

    with st.expander("🩺 Additional Clinical Information", expanded=True):

        diabetes_pedigree = st.number_input(
            "Diabetes Pedigree Function",
            0.05,
            3.00,
            0.47,
            step=0.01
        )

    st.write("")
        # =====================================================
    # AI Feature Engineering
    # =====================================================

    # ---------- BMI Category ----------

    bmi_obesity1 = 0
    bmi_obesity2 = 0
    bmi_obesity3 = 0
    bmi_overweight = 0
    bmi_underweight = 0

    if bmi < 18.5:
        bmi_underweight = 1

    elif bmi <= 24.9:
        pass

    elif bmi <= 29.9:
        bmi_overweight = 1

    elif bmi <= 34.9:
        bmi_obesity1 = 1

    elif bmi <= 39.9:
        bmi_obesity2 = 1

    else:
        bmi_obesity3 = 1

    # ---------- Insulin Score ----------

    insulin_normal = 1 if 16 <= insulin <= 166 else 0

    # ---------- Glucose Category ----------

    glucose_low = 0
    glucose_normal = 0
    glucose_overweight = 0
    glucose_secret = 0

    if glucose <= 70:
        glucose_low = 1

    elif glucose <= 99:
        glucose_normal = 1

    elif glucose <= 126:
        glucose_overweight = 1

    else:
        glucose_secret = 1

    # =====================================================
    # AI Generated Summary
    # =====================================================

    st.info(f"""
### 🤖 AI Derived Health Information

**Calculated BMI :** {bmi}

**BMI Category :**
{"Underweight" if bmi_underweight else
"Normal" if not (bmi_overweight or bmi_obesity1 or bmi_obesity2 or bmi_obesity3) else
"Overweight" if bmi_overweight else
"Obesity Class I" if bmi_obesity1 else
"Obesity Class II" if bmi_obesity2 else
"Obesity Class III"}

**Insulin Status :**
{"Normal" if insulin_normal else "Abnormal"}

**Glucose Status :**
{"Low" if glucose_low else
"Normal" if glucose_normal else
"Prediabetes" if glucose_overweight else
"Diabetic"}
""")

    st.write("")

    predict = st.form_submit_button(
        "🔍 Predict Diabetes Risk",
        use_container_width=True
    )

# =====================================================
# Prediction
# =====================================================

if predict:

    features = np.array([[
        pregnancies,
        glucose,
        blood_pressure,
        skin_thickness,
        insulin,
        bmi,
        diabetes_pedigree,
        age,
        bmi_obesity1,
        bmi_obesity2,
        bmi_obesity3,
        bmi_overweight,
        bmi_underweight,
        insulin_normal,
        glucose_low,
        glucose_normal,
        glucose_overweight,
        glucose_secret
    ]])

    # Scale using saved scaler
    features = scaler.transform(features)

    prediction = model.predict(features)
    probability = model.predict_proba(features)

    confidence = np.max(probability) * 100

    st.divider()

    st.subheader("🩺 Prediction Result")

    if prediction[0] == 1:

        st.error("## ⚠ High Risk of Diabetes")

        st.write(
            "The AI model predicts a **high likelihood of diabetes**. "
            "Please consult a healthcare professional for further evaluation."
        )

    else:

        st.success("## ✅ Low Risk of Diabetes")

        st.write(
            "The AI model predicts a **low likelihood of diabetes**. "
            "Maintain a healthy lifestyle and continue regular health checkups."
        )

    st.metric(
        "Model Confidence",
        f"{confidence:.2f}%"
    )

    st.divider()

    st.subheader("📊 Risk Probability")

    low = probability[0][0]
    high = probability[0][1]

    st.write(f"🟢 Low Risk : **{low*100:.2f}%**")
    st.progress(float(low))

    st.write("")

    st.write(f"🔴 High Risk : **{high*100:.2f}%**")
    st.progress(float(high))

    st.divider()

    st.subheader("📋 Patient Summary")

    left, right = st.columns(2)

    with left:

        st.write(f"**Age :** {age}")
        st.write(f"**Pregnancies :** {pregnancies}")
        st.write(f"**Glucose :** {glucose}")
        st.write(f"**Blood Pressure :** {blood_pressure}")
        st.write(f"**BMI :** {bmi}")

    with right:

        st.write(f"**Insulin :** {insulin}")
        st.write(f"**Skin Thickness :** {skin_thickness}")
        st.write(f"**Pedigree Function :** {diabetes_pedigree}")

    st.divider()

    if prediction[0] == 1:

        st.warning("""
### 💡 Recommendations

- Consult an endocrinologist.
- Monitor blood glucose regularly.
- Reduce sugar and refined carbohydrates.
- Exercise at least 30 minutes daily.
- Maintain a healthy body weight.
- Get HbA1c and fasting glucose tests periodically.
""")

    else:

        st.success("""
### 🌿 Healthy Lifestyle Tips

- Continue eating a balanced diet.
- Exercise regularly.
- Drink enough water.
- Maintain your ideal body weight.
- Schedule regular health checkups.
""")

    st.divider()

    st.caption("""
**Medical Disclaimer:** This prediction is generated using a Machine Learning model for educational purposes only. It should not replace professional medical advice, diagnosis, or treatment.
""")
    
   # -------------------------------
# Generate PDF Report
# -------------------------------

    patient_details = {
    "Age": age,
    "Pregnancies": pregnancies,
    "Glucose": glucose,
    "Blood Pressure": blood_pressure,
    "Skin Thickness": skin_thickness,
    "Insulin": insulin,
    "BMI": round(bmi, 2),
    "Diabetes Pedigree Function": round(diabetes_pedigree, 3),

    "BMI Category": (
        "Obese Class III" if bmi_obesity3 == 1 else
        "Obese Class II" if bmi_obesity2 == 1 else
        "Obese Class I" if bmi_obesity1 == 1 else
        "Overweight" if bmi_overweight == 1 else
        "Underweight" if bmi_underweight == 1 else
        "Normal"
    ),

    "Glucose Status": (
        "Low" if glucose_low == 1 else
        "Normal" if glucose_normal == 1 else
        "High"
    ),

    "Insulin Status": (
        "Normal" if insulin_normal == 1 else
        "Abnormal"
    )
}

    prediction_text = (
    "High Risk of Diabetes"
        if prediction[0] == 1
        else "Low Risk of Diabetes"
)

    if prediction[0] == 1:

        recommendations = [
        "Consult an endocrinologist.",
        "Monitor blood glucose regularly.",
        "Reduce sugar intake.",
        "Exercise for at least 30 minutes daily.",
        "Get an HbA1c test.",
        "Maintain a healthy body weight.",
        "Follow a diabetic-friendly diet."
    ]

    else:

        recommendations = [
        "Maintain a balanced diet.",
        "Exercise regularly.",
        "Maintain a healthy weight.",
        "Drink adequate water.",
        "Schedule annual diabetes screening."
    ]

    pdf = generate_medical_report(
    disease_name="Diabetes",
    patient_details=patient_details,
    prediction=prediction_text,
    confidence=confidence,
    recommendations=recommendations
)

    st.download_button(
    label="📄 Download Diabetes Report",
    data=pdf,
    file_name="Diabetes_Report.pdf",
    mime="application/pdf",
    use_container_width=True
)
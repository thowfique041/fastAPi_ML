import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/predict"

st.set_page_config(
    page_title="Diabetes Prediction",
    page_icon="🩺",
    layout="centered"
)

st.markdown("""
<style>
    .main > div { padding-top: 1.5rem; }
    div[data-testid="stNumberInput"] input { border-radius: 8px; }
    .result-box {
        padding: 1.2rem 1.5rem;
        border-radius: 12px;
        margin-top: 1rem;
    }
    .diabetic { background-color: #fff0f0; border-left: 5px solid #e24b4a; color: #1a1a1a; }
    ..non-diabetic { background-color: #f0faf0; border-left: 5px solid #639922; color: #1a1a1a; }
    .prob-label { font-size: 0.85rem; color: #555; margin-bottom: 2px; }
</style>
""", unsafe_allow_html=True)


# ── Header ──────────────────────────────────────────────────────────────────
st.markdown("## 🩺 Diabetes Prediction")
st.caption("Enter patient details below and click **Predict** to get an ML-based diagnosis.")
st.divider()


# ── Patient Info ─────────────────────────────────────────────────────────────
st.markdown("#### 👤 Patient info")
col1, col2 = st.columns([2, 1])
with col1:
    name = st.text_input("Full name", placeholder="e.g. Saminer Bow")
with col2:
    age = st.number_input("Age", min_value=0, max_value=120, value=43, step=1)

gender = st.radio("Gender", ["Female", "Male"], horizontal=True)

if gender == "Male":
    pregnancies = 0
    st.info("ℹPregnancies automatically set to **0** for male patients.")
else:
    pregnancies = st.number_input("Number of pregnancies", min_value=0, max_value=20, value=6, step=1)

st.divider()


# ── Clinical Measurements ────────────────────────────────────────────────────
st.markdown("####  Clinical measurements")

col3, col4 = st.columns(2)
with col3:
    glucose = st.number_input("Glucose (mg/dL)", min_value=0, max_value=300, value=98, step=1)
    skin_thickness = st.number_input("Skin thickness (mm)", min_value=0, max_value=100, value=33, step=1)
with col4:
    blood_pressure = st.number_input("Blood pressure (mm Hg)", min_value=0, max_value=200, value=72, step=1)
    insulin = st.number_input("Insulin (μU/mL)", min_value=0.0, max_value=1000.0, value=190.0, step=0.1, format="%.1f")

st.divider()


# ── Body Metrics ─────────────────────────────────────────────────────────────
st.markdown("####  Body metrics")

col5, col6 = st.columns(2)
with col5:
    bmi = st.number_input("BMI (kg/m²)", min_value=0.0, max_value=80.0, value=34.0, step=0.1, format="%.1f")
with col6:
    dpf = st.number_input("Diabetes pedigree function", min_value=0.0, max_value=3.0, value=0.43, step=0.01, format="%.2f")

st.divider()


# ── Predict Button ───────────────────────────────────────────────────────────
predict_clicked = st.button("🔍  Predict", use_container_width=True, type="primary")

if predict_clicked:
    if not name.strip():
        st.error("Please enter the patient's name.")
    else:
        payload = {
            "name": name.strip(),
            "pregnancies": int(pregnancies),
            "glucose": int(glucose),
            "blood_pressure": int(blood_pressure),
            "skin_thickness": int(skin_thickness),
            "insulin": float(insulin),
            "bmi": float(bmi),
            "diabetes_pedigree_function": float(dpf),
            "age": int(age),
        }

        with st.spinner("Running prediction…"):
            try:
                response = requests.post(API_URL, json=payload, timeout=10)
                response.raise_for_status()
                data = response.json()
            except requests.exceptions.ConnectionError:
                st.error(" Cannot connect to the API. Make sure the FastAPI server is running at `http://127.0.0.1:8000`.")
                st.stop()
            except requests.exceptions.HTTPError as e:
                st.error(f" API error {response.status_code}: {response.text}")
                st.stop()
            except Exception as e:
                st.error(f" Unexpected error: {e}")
                st.stop()

        # ── Results ──────────────────────────────────────────────────────────
        prediction = data["prediction"]["prediction"]
        prob = data["prediction"]["probability"]

        is_diabetic = prediction == "Diabetic"
        box_class = "diabetic" if is_diabetic else "non-diabetic"
        icon = "🔴" if is_diabetic else "🟢"

        st.markdown(f"""
        <div class="result-box {box_class}">
            <h4 style="margin:0 0 4px;">{icon} {data['name']}</h4>
            <p style="margin:0; font-size:1.1rem; font-weight:600;">
                Prediction: <span>{"Diabetic" if is_diabetic else "Non-Diabetic"}</span>
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### Prediction probabilities")

        diab_pct = prob["Diabetic"] * 100
        non_diab_pct = prob["Non-Diabetic"] * 100

        st.markdown('<p class="prob-label">Diabetic</p>', unsafe_allow_html=True)
        st.progress(prob["Diabetic"], text=f"{diab_pct:.1f}%")

        st.markdown('<p class="prob-label">Non-Diabetic</p>', unsafe_allow_html=True)
        st.progress(prob["Non-Diabetic"], text=f"{non_diab_pct:.1f}%")

        with st.expander("📋 Full patient record"):
            st.json(data)

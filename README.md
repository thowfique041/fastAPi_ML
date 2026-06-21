# 🩺 Diabetes Prediction App

A machine learning-powered web application that predicts diabetes risk based on patient clinical data. Built with **FastAPI** (backend) and **Streamlit** (frontend), trained on the [Pima Indians Diabetes Database](https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database).

---

##  Features

- Patient info form with gender-aware pregnancies field (auto-sets to 0 for male)
- Real-time prediction via FastAPI ML backend
- Probability visualization with progress bars
- Color-coded result — 🔴 Diabetic / 🟢 Non-Diabetic
- Full patient record viewer (JSON)

---

##  Project Structure

```
fastAPi_ML/
├── main.py             # FastAPI backend + ML inference
├── streamlit_app.py    # Streamlit frontend
├── model.pkl           # Trained ML model (not included in repo)
├── requirements.txt
└── README.md
```

---

##  Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/thowfique041/fastAPi_ML.git
cd fastAPi_ML
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your trained model

Place your trained model file as `model.pkl` in the root directory.  
The model must be trained on the following features (in this order):

| Feature | Description |
|---|---|
| `Pregnancies` | Number of pregnancies |
| `Glucose` | Plasma glucose concentration (mg/dL) |
| `BloodPressure` | Diastolic blood pressure (mm Hg) |
| `SkinThickness` | Triceps skinfold thickness (mm) |
| `Insulin` | 2-hour serum insulin (μU/mL) |
| `BMI` | Body mass index (kg/m²) |
| `DiabetesPedigreeFunction` | Diabetes pedigree function |
| `Age` | Age in years |

---

##  Running the App

You need **two terminals** running simultaneously.

### Terminal 1 — FastAPI backend

```bash
uvicorn main:app --reload
```

API will be available at `http://127.0.0.1:8000`  
Swagger docs at `http://127.0.0.1:8000/docs`

### Terminal 2 — Streamlit frontend

```bash
streamlit run streamlit_app.py
```

App will open at `http://localhost:8501`

---

##  Requirements

```
fastapi
uvicorn
pydantic
pandas
scikit-learn
streamlit
requests
```

Or install via:

```bash
pip install fastapi uvicorn pydantic pandas scikit-learn streamlit requests
```

---

##  API Endpoints

### `GET /`
Health check.

```json
{ "message": "Welcome to the Diabetes Prediction API!" }
```

### `POST /predict`
Predict diabetes for a patient.

**Request body:**
```json
{
  "name": "John Doe",
  "pregnancies": 6,
  "glucose": 148,
  "blood_pressure": 72,
  "skin_thickness": 35,
  "insulin": 0.0,
  "bmi": 33.6,
  "diabetes_pedigree_function": 0.627,
  "age": 50
}
```

**Response:**
```json
{
  "name": "John Doe",
  "pregnancies": 6,
  "glucose": 148,
  "blood_pressure": 72,
  "skin_thickness": 35,
  "insulin": 0.0,
  "bmi": 33.6,
  "diabetes_pedigree_function": 0.627,
  "age": 50,
  "prediction": {
    "prediction": "Diabetic",
    "probability": {
      "Diabetic": 0.82,
      "Non-Diabetic": 0.18
    }
  }
}
```

---

##  Dataset

- **Source:** [Pima Indians Diabetes Database — Kaggle](https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database)
- **Origin:** National Institute of Diabetes and Digestive and Kidney Diseases
- **Target:** `Outcome` — `0` = Non-Diabetic, `1` = Diabetic

---

##  Notes

- `model.pkl` is excluded from this repository. Train your own model using the Pima Indians Diabetes Dataset and save it with `pickle`.
- Make sure the FastAPI server is running before using the Streamlit frontend.
- For cross-origin requests, CORS is enabled in `main.py`.

---

##  Author

**Your Name**  
[GitHub](https://github.com/thowfique041) 

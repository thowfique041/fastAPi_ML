import pickle as pkl
import pandas as pd
from pathlib import Path

MODEL_VERSION = "1.0.0"


model_path = Path("model/model.pkl")
if not model_path.exists():
    raise FileNotFoundError("Model file not found.")

with model_path.open("rb") as f:
    model = pkl.load(f)


def make_diabetes_prediction(patient_data):
    input_data = pd.DataFrame([{
        "Pregnancies": patient_data.pregnancies,
        "Glucose": patient_data.glucose,
        "BloodPressure": patient_data.blood_pressure,
        "SkinThickness": patient_data.skin_thickness,
        "Insulin": patient_data.insulin,
        "BMI": patient_data.bmi,
        "DiabetesPedigreeFunction": patient_data.diabetes_pedigree_function,
        "Age": patient_data.age
    }])
    
    prediction = model.predict(input_data)
    prediction_proba = model.predict_proba(input_data)[0]
    return {
        "prediction": "Diabetic" if prediction[0] == 1 else "Non-Diabetic",
        "probability": {
            "Diabetic": float(prediction_proba[1]),
            "Non-Diabetic": float(prediction_proba[0])
        }
    }



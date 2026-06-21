from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Annotated
import pickle as pkl
import pandas as pd
from pathlib import Path


def load_model():
    model_path = Path("model.pkl")
    if not model_path.exists():
        raise FileNotFoundError("Model file not found.")
    with model_path.open("rb") as f:
        return pkl.load(f)

model = load_model()


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


class Patient(BaseModel):  
    name: Annotated[str, Field(..., description="Patient's name", examples=["Saminer bow"])]  
    pregnancies: Annotated[int, Field(..., description="Number of pregnancies", examples=[6])]
    glucose: Annotated[int, Field(..., description="Glucose level", examples=[98])]
    blood_pressure: Annotated[int, Field(..., description="Blood pressure", examples=[72])]
    skin_thickness: Annotated[int, Field(..., description="Skin thickness", examples=[33])]
    insulin: Annotated[float, Field(..., description="Insulin level", examples=[190.0])]
    bmi: Annotated[float, Field(..., description="Body Mass Index (BMI)", examples=[34.0])]
    diabetes_pedigree_function: Annotated[float, Field(..., description="Diabetes pedigree function", examples=[0.43])]
    age: Annotated[int, Field(..., description="Age", examples=[43])]


app = FastAPI()


@app.get("/")
def display_home():
    return {"message": "Welcome to the Diabetes Prediction API!"}


@app.post("/predict")
def predict_patient_diabetes(patient_data: Patient):
    prediction_result = make_diabetes_prediction(patient_data)
    return {
        "name": patient_data.name,
        "pregnancies": patient_data.pregnancies,
        "glucose": patient_data.glucose,
        "blood_pressure": patient_data.blood_pressure,
        "skin_thickness": patient_data.skin_thickness,
        "insulin": patient_data.insulin,
        "diabetes_pedigree_function": patient_data.diabetes_pedigree_function,
        "age": patient_data.age,
        "bmi": patient_data.bmi,
        "prediction": prediction_result
    }
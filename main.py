from fastapi import FastAPI
from schema.user_input import Patient
from schema.response_pd import PredictionResponse
from model.predict import make_diabetes_prediction, MODEL_VERSION, model






app = FastAPI()


@app.get("/")
def display_home():
    return {"message": "Welcome to the Diabetes Prediction API!"}



@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "version": MODEL_VERSION,
        "model_loaded": model is not None
        }



@app.post("/predict", response_model=PredictionResponse)
def predict_patient_diabetes(patient_data: Patient):
    prediction_result = make_diabetes_prediction(patient_data)
    return {
        "name": patient_data.name,
        # "pregnancies": patient_data.pregnancies,
        # "glucose": patient_data.glucose,
        # "blood_pressure": patient_data.blood_pressure,
        # "skin_thickness": patient_data.skin_thickness,
        # "insulin": patient_data.insulin,
        # "diabetes_pedigree_function": patient_data.diabetes_pedigree_function,
        # "age": patient_data.age,
        # "bmi": patient_data.bmi,
        "prediction": prediction_result
    }
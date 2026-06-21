from pydantic import BaseModel, Field
from typing import Annotated




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


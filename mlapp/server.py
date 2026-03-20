from fastapi import FastAPI
from pydantic import BaseModel
import mlflow
import numpy as np
import os

mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://host.docker.internal:5000"))

model_uri = "models:/diabetes_model/1" 
model = mlflow.sklearn.load_model(model_uri)

app = FastAPI(title="Diabetes Prediction API")

class PatientData(BaseModel):
    age: float
    sex: float
    bmi: float
    bp: float
    s1: float
    s2: float
    s3: float
    s4: float
    s5: float
    s6: float

@app.get("/")
def root():
    return {"message": "Diabetes Prediction API with trained model"}

@app.post("/api/v1/predict")
def predict(data: PatientData):
    features = np.array([[
        data.age, data.sex, data.bmi, data.bp,
        data.s1, data.s2, data.s3, data.s4, data.s5, data.s6
    ]])
    prediction = model.predict(features)[0]
    return {"predict": float(prediction)}
    return {"predict": prediction}
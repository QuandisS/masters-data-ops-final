import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.responses import PlainTextResponse
from prometheus_client import (
    Counter,
    Histogram,
    Gauge,
    generate_latest,
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
)
from pydantic import BaseModel
import mlflow
import numpy as np
import os

mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://host.docker.internal:5000"))

model_uri = "models:/diabetes_model/1"
model = mlflow.sklearn.load_model(model_uri)

registry = CollectorRegistry()

http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
    registry=registry,
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
    buckets=(0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
    registry=registry,
)

model_predictions_total = Counter(
    "model_predictions_total",
    "Total model predictions",
    registry=registry,
)

model_prediction_duration_seconds = Histogram(
    "model_prediction_duration_seconds",
    "Model prediction duration in seconds",
    buckets=(0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0),
    registry=registry,
)

model_loaded = Gauge(
    "model_loaded",
    "Indicates if the model is loaded (1) or not (0)",
    registry=registry,
)
model_loaded.set(1)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown


app = FastAPI(title="Diabetes Prediction API", lifespan=lifespan)


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    http_requests_total.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code,
    ).inc()

    http_request_duration_seconds.labels(
        method=request.method,
        endpoint=request.url.path,
    ).observe(duration)

    return response


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


@app.get("/metrics")
def metrics():
    """Expose Prometheus metrics endpoint."""
    return PlainTextResponse(
        generate_latest(registry),
        media_type=CONTENT_TYPE_LATEST,
    )


@app.post("/api/v1/predict")
def predict(data: PatientData):
    start_time = time.time()

    features = np.array([[
        data.age, data.sex, data.bmi, data.bp,
        data.s1, data.s2, data.s3, data.s4, data.s5, data.s6
    ]])
    prediction = model.predict(features)[0]

    model_predictions_total.inc()
    prediction_duration = time.time() - start_time
    model_prediction_duration_seconds.observe(prediction_duration)

    return {"predict": float(prediction)}
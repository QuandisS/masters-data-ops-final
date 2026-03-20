FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./mlapp/

ENV MLFLOW_TRACKING_URI=http://localhost:5000

EXPOSE 8000

CMD ["python", "-m", "mlapp"]
FROM python:3.9-slim
LABEL authors="Quanted"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
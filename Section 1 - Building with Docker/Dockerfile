FROM python:3.8-slim-buster

# Set current working directory
WORKDIR /opt

# Install python packages
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ .

# Start FastAPI application using Uvicorn
uvicorn predict
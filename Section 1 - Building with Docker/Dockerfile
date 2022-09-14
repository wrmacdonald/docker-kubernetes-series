FROM python:3.8-slim-buster

# Set current working directory
WORKDIR /opt

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV DATA_DIR '/data'
ENV PORT 8000

#update system dependencies
RUN apt-get update \
    && apt-get upgrade \
    && apt-get clean

# Install python packages
COPY requirements.txt .
RUN pip install -r requirements.txt \
    && rm requirements.txt

COPY app/ ./app/

EXPOSE 8000

# Start FastAPI application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
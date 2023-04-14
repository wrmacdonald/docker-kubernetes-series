# Section 1 - Building with Docker

## Running the application

This application can run both locally and in a Docker container. These commands are meant to run on Unix based system. If you are on a Windows system, please adjust filepaths accordingly.

### To Run Locally

1. Run `https://github.com/PDXPythonPirates/docker-kubernetes-series.git` to clone the repo locally.

2. Create a virtual environment by running `python -m venv .venv`. Once your virtual environment is installed use activate it using `source .venv/bin/activate` and run `pip install requirements.txt` to install the necessary dependencies.

3. Create a `.env` file in `app` directory with the contents:

```
RALEIGH_TEMP_PATH=temperature_data_Raleigh_012020_062022.csv
```

4. Run `uvicorn app.main:app --reload`

### To Run as Docker container

1. Create a `.env` file in the `app/` directory with `RALEIGH_TEMP_PATH=temperature_data_Raleigh_012020_062022.csv`

2. Create a Dockerfile name `Dockerfile`.

```
FROM python:3.8-slim-buster

# Set current working directory
WORKDIR /opt

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV DATA_DIR '/data'
ENV PORT 8000

#update system dependencies
RUN apt-get update \
    && apt-get -y upgrade \
    && apt-get clean

# Install python packages
COPY requirements.txt .
RUN pip install -r requirements.txt \
    && rm requirements.txt

COPY app/ ./app/

EXPOSE 8000

# Start FastAPI application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
```

3. Build your container image by running `docker build -t docker-demo:0.1.0 .`

4. Run `docker run --rm -p 8000:8000 --env-file=app/.env -v ${PWD}/data:/data --name docker-demo docker-demo:0.1.0` to run the container.

5. When you want to stop the container run `docker stop docker-demo`.

Once the application is running locally or as a conatiner, open a browser and navigate to `localhost:8000`. You should see the Swagger documentation window.

My Notes:
Followed these instructions to move changes to my fork:
1. Fork their repo on Github
2. In your local, rename your origin remote to upstream

    git remote rename origin upstream

3. Add a new origin

    git remote add origin git@github...my-fork

4. Fetch & push

    git fetch origin
    git push origin

5. Change to push goes to my repo

    git push -u origin branchname

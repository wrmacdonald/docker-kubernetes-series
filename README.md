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

2. Build your container image by running `docker build -t docker-demo:0.1.0 .`

3. Run `docker run --rm -p 8000:8000 --env-file=app/.env -v ${PWD}/data:/data --name docker-demo docker-demo:0.1.0` to run the container.

4. When you want to stop the container run `docker stop docker-demo`.

Once the application is running locally or as a conatiner, open a browser and navigate to `localhost:8000/docs`. You should see the Swagger documentation window.

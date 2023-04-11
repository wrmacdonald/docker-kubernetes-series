# Section 2 - Microservices with Docker Compose

## Running the application
These commands are meant to run on Unix based system. If you are on a Windows system, please adjust filepaths accordingly.

1. Create a `.env` file in the base directory with

```
RALEIGH_TEMP_PATH=raleigh_temps.csv
POSTGRES_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

2. Run the application by running `docker-compose up` in the same directory as the `docker-compose.yaml`.

3. When you want to stop the application run `docker-compose down` in the same directory as the `docker-compose.yaml`.

Once the application is running locally or as a conatiner, open a browser and navigate to `localhost:8000`. You should see the Swagger documentation window.

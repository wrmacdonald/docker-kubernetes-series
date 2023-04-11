# Section 2 - Microservices with Docker Compose

## Running the application
These commands are meant to run on Unix based system. If you are on a Windows system, please adjust filepaths accordingly.

1. Create a Docker Compose file named `docker-compose.yaml`.

```
version: "3.9"

services:
    postgres:
      image: postgres
      container_name: postgres
      environment:
        - POSTGRES_DB=postgres
        - POSTGRES_USER=postgres
        - POSTGRES_PASSWORD=postgres
      volumes:
        - ./csvs:/var/lib/postgresql/csvs/
        - ./scripts/init.sql:/docker-entrypoint-initdb.d/init.sql
      expose:
        - "5432"
      networks:
        - backend

    predict:
      build:
        dockerfile: predict/Dockerfile.predict
        tags:
          - 0.1.0
      container_name: predict
      command: uvicorn app.main:app --host 0.0.0.0
      ports:
        - "8000:8000"
      networks:
        - frontend
      depends_on:
        - postgres

    preprocess:
      build:
        dockerfile: preprocess/Dockerfile.preprocess
        tags:
          - 0.1.0
      container_name: preprocess
      command: uvicorn app.main:app --host 0.0.0.0
      env_file:
        - .env
      expose:
        - "8000"
      networks:
        - backend
        - frontend
      depends_on:
        - postgres

networks:
  backend:
    name: backend
  frontend:
    name: frontend

```

2. Create a `.env` file in the base directory with

```
RALEIGH_TEMP_PATH=raleigh_temps.csv
POSTGRES_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

3. Run the application by running `docker-compose up` in the same directory as the `docker-compose.yaml`.

4. When you want to stop the application run `docker-compose down` in the same directory as the `docker-compose.yaml`.

Once the application is running locally or as a conatiner, open a browser and navigate to `localhost:8000`. You should see the Swagger documentation window.

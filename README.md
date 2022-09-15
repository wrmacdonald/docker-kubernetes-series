# Introduction 
This tutorial will give you an introduction to Docker and Kubernetes by deploying MLFlow. 

In Section 1, we build a simple Docker container.

In Section 2, we will learn how to use Docker Compose to network multiple Docker containers together.

In Section 3, we will make our application scalable by deploying it to Kubernetes.

This introduction only assumes familiarity with Python, although it would also help to have a basic understanding of MLFlow to gain a deeper insight into why we might need containerization.

# Installing Docker Desktop

1. Navigate to the [Docker website](https://www.docker.com) and download the Docker Desktop installer for your [Mac](https://hub.docker.com/editions/community/docker-ce-desktop-mac) or [Windows](https://hub.docker.com/editions/community/docker-ce-desktop-windows) operating system.

2. Once the download finishes, click the installer to install Docker Desktop Community Edition on your machine.

3. To ensure that Docker installed correctly, open a terminal window and run `docker run hello-world`. If it is successful you should get the following output:

```
Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

**NOTE**: Docker also comes installed with Kubernetes, so this one install takes care of both dependencies!

# Section 1 - Building with Docker

## Running the application 

This application can run both locally and in a Docker container.You must be in `Section 1 - Building with Docker` for the commands in this section to execute properly. Also these commands are meant to run on Unix based system. If you are on a Windows system, please adjust filepaths accordingly.

### To Run Locally

1. Create a virtual environment using one of the two methods:
   
   a. Run `python -m venv .venv`. Once your virtual environment is installed use `pip install requirements.txt` to install the necessary dependencies.
   
   b. If you have conda Run `conda env create --file conda.yaml`

2. Navigate to `mlflow-with-docker-kubernetes/Section 1 - Building with Docker`

3. Create a `.env` file in `app` directory with the contents 

`RALEIGH_TEMP_PATH=temperature_data_Raleigh_012020_062022.csv`

4. Run `uvicorn app.main:app --reload`

### To Run as Docker container

1. Build your container image by running `docker build -t docker-demo:0.1.0 .`

2. Run `docker run --rm -p 8000:8000 --env-file=app/.env -v ${PWD}/data:/data --name docker-demo docker-demo:0.1.0` to run the container.

Once the application is running locally or as a conatiner, open a browser and navigate to `localhost:8000/docs`. You should see the Swagger documentation window.

# Section 2 - Microservices with Docker Compose

*Coming Soon*

# Section 3 - Scaling with Kubernetes

*Coming Soon*
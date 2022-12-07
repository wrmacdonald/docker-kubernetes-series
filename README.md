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

This application can run both locally and in a Docker container. You must be in `Section 1 - Building with Docker` for the commands in this section to execute properly. Also, these commands are meant to run on Unix based system. If you are on a Windows system, please adjust filepaths accordingly.

### To Run Locally

1. Run `git clone https://MeaganGentry@dev.azure.com/MeaganGentry/NAIP/_git/containerizing-apps-docker-kubernetes` to clone the repo locally.

2. Navigate to the repo directory using and create a virtual environment using one of the two methods:
   
   a. Run `python -m venv .venv`. Once your virtual environment is installed use `pip install requirements.txt` to install the necessary dependencies.
   
   b. If you have conda Run `conda env create --file conda.yaml`

3. Navigate to `mlflow-with-docker-kubernetes/Section 1 - Building with Docker`

4. Create a `.env` file in `app` directory with the contents 

`RALEIGH_TEMP_PATH=temperature_data_Raleigh_012020_062022.csv`

5. Run `uvicorn app.main:app --reload`

### To Run as Docker container
1. Create a `.env` file in the `app/` directory with `RALEIGH_TEMP_PATH=temperature_data_Raleigh_012020_062022.csv`

2. Build your container image by running `docker build -t docker-demo:0.1.0 .`

3. Run `docker run --rm -p 8000:8000 --env-file=app/.env -v ${PWD}/data:/data --name docker-demo docker-demo:0.1.0` to run the container.

4. When you want to stop the container run `docker stop docker-demo`.

Once the application is running locally or as a conatiner, open a browser and navigate to `localhost:8000/docs`. You should see the Swagger documentation window.

# Section 2 - Microservices with Docker Compose

## Running the application
You must be in `Section 2 - Microservices with Docker Compose` for the commands in this section to execute properly. Also, these commands are meant to run on Unix based system. If you are on a Windows system, please adjust filepaths accordingly.

1. Create a `.env` file in the base directory with

```
RALEIGH_TEMP_PATH=raleigh_temps.csv
POSTGRES_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

2. Run the application by running `docker-compose up` in the same directory as the `docker-compose.yaml`.

3. When you want to stop the application run `docker-compose down` in the same directory as the `docker-compose.yaml`.

Once the application is running locally or as a conatiner, open a browser and navigate to `localhost:8000/docs`. You should see the Swagger documentation window.

# Section 3 - Scaling with Kubernetes
You must be in `Section3 - Scaling with Kubernetes` for the commands in this section to execute properly. Also, these commands are meant to run on Unix based system. If you are on a Windows system, please adjust filepaths accordingly.

## Activate Kubernetes
Docker Desktop comes with an option to spin up a local Kubernetes cluster. Use the following steps to activate it.

1. Open the Docker Desktop Dashboard either by navigating to it in your applications or by using the tray  icon and selecting `Dashboard` from the dropdown.

2. Open settings by clicking on the gear icon.

3. Navigate to Kubernetes and check the box next to `Enable Kubernetes` and click `Apply and Restart`

4. Once Docker Desktop restarts, test that your Kubernetes cluster is running.

```
$kubectl create deployment nginx --image=nginx

$kubectl get deployment --watch
```
After a few seconds, you should see output similar to this:

```
NAME    READY   UP-TO-DATE   AVAILABLE   AGE
nginx   1/1     1            1           8s
```

This means that your cluster is ready to go! You can use `ctrl-X` to stop watching and then delete the deployment using:
```
$kubectl delete deployment nginx
```

## Start Postgres
A Postgres container should be started separately from the Kubernetes application to simulate an external database. 

To do this, run the command below. Don't forget to replace the <GIT_DIR_PATH> with the absolute path to your local `` directory.

```
docker run -d --rm -e POSTGRES_DB=postgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -v <GIT_DIR_PATH>/containerizing-apps-docker-kubernetes/csvs:/var/lib/postgresql/csvs/ -v <GIT_DIR_PATH>/scripts/init.sql:/docker-entrypoint-initdb.d/init.sql -p 5432:5432 postgres:latest
```

To check if your database is running correctly you can either look in your Docker Desktop dashboard or 

## Running the Application
To run the application, navigate to `Section 3 - Scaling with Kubernetes` and apply the api.yaml manifest.

```
$kubectl apply -f api.yaml
```

You should see:

```
service/prophet-model-svc created
deployment.apps/prophet-model created
```

Open a browser and navigate to `http://localhost` to see the application. If you receive an error, try repeating the previous steps.

## See Scaling in Action
To see scaling working in real time, open a terminal.

In the terminal, run

```
$kubectl get pods --watch

or

$kubectl get deployments --watch
```

This will put a coninuous watch on the pods or the deployments. You will see the same behavior either way. You could also open another terminal and run both of the commands above to monitor pods and deployments simultaneously.

Now open `api.yaml` in a text editor of your choice and change `replicas: 1` to `replicas: 3`. 

Now make sure you are in the `Section 3 - Scaling with Kubernetes` directory and run
```
$kubectl apply -f api.yaml
```

In your terminal(s), you should see the number of pods and/or deployments increase from one to three. You can scale down by using these same steps.

## See Load Balancing in Action
Follow the steps in the [previous](#see-scaling-in-action) to ensure that you have at least two pods running. 

To see the load balancer working, open two terminals or split a single terminal. 

In the first terminal, run

```
$kubectl get pods --watch
```

This will put a coninuous watch on the pods.

In the second terminal, navigate to the root directory `containerizing-apps-docker-kubernetes` and run `python3 test_request.py`. You should see some output similar to this:

```
{"hostname":"prophet-model-977fdcb5f-4kqmm"}


{"hostname":"prophet-model-977fdcb5f-kdfsg"}


{"hostname":"prophet-model-977fdcb5f-p92q4"}
```

These are the different pods that the load balancer is directing traffic to. Cool!

## Cleanup Kubernetes Environment
Cleanup is a breeze with Kubernetes. Just remove the resources your created by running

```
$kubectl delete -f api.yaml
```
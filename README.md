# Section 3 - Scaling with Kubernetes

These commands are meant to run on Unix based system. If you are on a Windows system, please adjust filepaths accordingly.

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

First create a file called `api.yaml`.

```
# kubernetes-fastapi LoadBalancer Service
# Enables the pods in a deployment to be accessible from outside the cluster
apiVersion: v1
kind: Service
metadata:
  name: prophet-model-svc
spec:
  selector:
    app: prophet-model
  ports:
    - protocol: "TCP"
      port: 8000
      targetPort: 8000
  type: LoadBalancer

---
# kf-api Deployment
# Defines the deployment of the app running in a pod on any worker node
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prophet-model
  labels:
    app: prophet-model
spec:
  replicas: 3
  selector:
    matchLabels:
      app: prophet-model
  template:
    metadata:
      labels:
        app: prophet-model
    spec:
      containers:
        - name: predict
          image: dockerdemo/predict:0.1.0
          ports:
            - containerPort: 8000
          imagePullPolicy: Never
          resources:
            # You must specify requests for CPU to autoscale
            # based on CPU utilization
            requests:
              cpu: "250m"
        - name: preprocess
          image: dockerdemo/preprocess:0.1.0
          ports:
            - containerPort: 9000
          imagePullPolicy: Never
          resources:
            # You must specify requests for CPU to autoscale
            # based on CPU utilization
            requests:
              cpu: "250m"
```

To run the application, apply the api.yaml manifest.

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

Now open `api.yaml` in a text editor of your choice and change `replicas: 1` to `replicas: 3` and run run:

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

In the second terminal, navigate to the root directory `docker-kubernetes-series` and run `python3 test_request.py`. You should see some output similar to this:

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

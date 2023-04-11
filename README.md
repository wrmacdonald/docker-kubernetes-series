# Introduction

This tutorial will give you an introduction to Docker and Kubernetes. To get to a particular section, switch to the relevant branch.

In Section 1, we build a simple Docker container.

In Section 2, we will learn how to use Docker Compose to network multiple Docker containers together.

In Section 3, we will make our application scalable by deploying it to Kubernetes.

Access the [Notion template](https://ebony-interest-a3a.notion.site/Docker-and-Kubernetes-Series-af82efeb0e7b47f4bcb1bc3d5e81067e) to follow along with the full tutorial.

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

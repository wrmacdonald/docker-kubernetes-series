# Introduction 
This tutorial will give you an introduction to Docker and Kubernetes by deploying MLFlow. 

In Section 1, we build a simple Docker container, then add some complexity by deploying our container with Docker Compose. 

In Section 2, we will learn how to make our deployment more scalable using Kubernetes.

This introduction only assumes familiarity with Python, although it would also help to have a basic understanding of MLFlow to gain a deeper insight into why we might need containerization.

# Installing Docker Desktop
TODO: Guide users through getting your code up and running on their own system. In this section you can talk about:
1.	Installation process
2.	Software dependencies
3.	Latest releases
4.	API references

1. Navigate to the [Docker website](https://www.docker.com/get-started/) and download the Docker Desktop installer for your operating system.

2. Once the download finishes, click the installer to install Docker Desktop on your machine.

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

# Build and Test
TODO: Describe and show how to build your code and run the tests. 

# Contribute
TODO: Explain how other users and developers can contribute to make your code better. 

If you want to learn more about creating good readme files then refer the following [guidelines](https://docs.microsoft.com/en-us/azure/devops/repos/git/create-a-readme?view=azure-devops). You can also seek inspiration from the below readme files:
- [ASP.NET Core](https://github.com/aspnet/Home)
- [Visual Studio Code](https://github.com/Microsoft/vscode)
- [Chakra Core](https://github.com/Microsoft/ChakraCore)`
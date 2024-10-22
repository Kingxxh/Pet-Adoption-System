# CSE5306 Project 2 
----
## Team Members
| Name | UTA ID | Email | Finished Task |
| --- | --- | --- |---------------|
| Chenfei Liao | 1002234830 | cxl4830@mavs.uta.edu | Q1, Q2 |
| Xuhao Xie | 1002249206 | xxx9206@mavs.uta.edu | Q3, Q4 |
----

## Question 2
Implement two basic server-client pairs using the same stub with gRPC. 

You can define your own functionality to implement.

**NOTE: You should use two different languages to implement the two pairs.**

----

**Answer:**
We implemented a simple pet registraion and search system using gRRPC. The system has two services, one for registering a pet and the other for searching a pet. We implemented the server/client pair in both Python and Java.

### 2.1 Prerequisites
#### Python
- Python 3.7 or later
- grpcio-tools: ```python -m pip install grpcio-tools```
- grpcio: ```python -m pip install grpcio```
  
#### Java
- Java 8 or later
- Gradle

### 2.2 Unzip the file
1. In the  zip file directory, unzip the file 
   
   ```tar -xvf cse5306project2-main.zip```
2. Change the directory to the unzipped folder

   ```cd cse5306project2-main```

### 2.3 gRPC Proto file
The proto file is located in the ```protos``` directory. The proto file defines the services and messages used in the system. To generate the stubs, run the following command in the project directory.

```python -m grpc_tools.protoc -I./protos --python_out=. --pyi_out=. --grpc_python_out=. ./protos/pet.proto```

```mkdir generated```

```protoc -I=./protos --java_out=./generated --grpc-java_out=./generated ./protos/pet.proto```

### 2.4 Python Server/Client
1. Run the server
   ```python petserver.py```

   The server will start running on port 58453.
2. Run the client
   ```python pet_client.py```
    
    The client will start running and you can register and search for pets.

### 2.5 Java Server/Client
1. Build the project
   ```./gradlew build```
2. Run the server
   ```java -jar build/libs/server.jar```

    The server will start running on port 58455.
3. Run the client ```java -jar build/libs/client.jar```

    The client will start running and you can register and search for pets.

## Question 3
# Pet Adoption System - gRPC Backed Virtual Pet Adoption System

This project is a gRPC-backed virtual pet adoption system. The system includes both server and client components, allowing users to register pets and search for pets available for adoption.
  
You can find our source code in the zip file, or you can find this project on GitHub.<br>
[GitHub - Java-based Server](https://github.com/Kingxxh/Pet-Adoption-System-Server)<br>
[GitHub - Python-based Client](https://github.com/Kingxxh/Pet-Adoption-System-Client)

## Project Structure

The project is divided into the following components:

1. **Server (Java-based)**
   - The server is a gRPC server implemented in Java that handles requests for registering and searching for pets.
   
2. **Client (Python-based)**
   - The client is a Python application that interacts with the gRPC server. It allows users to register pets, search for pets, and display pet details such as name, breed, age, and a photo.

### Client Variants:
- **Graphical User Interface (GUI) Version**: Uses `tkinter` to provide a GUI for interacting with the system.
- **Command-Line Interface (CLI) Version**: A no-GUI version designed for command-line interaction.

## Running the System

You have two options to run the Pet Adoption system:

### Option 1: Run via Docker (Command-Line Interface Only)

Due to current technical limitations, the system cannot run the GUI version in a Docker container. However, the command-line version of the client can be run using Docker.

### Prerequisites
- Docker (for containerization of both the server and client components)
- A basic understanding of gRPC and Docker

### Step 1: Pull the Docker Images from Docker Hub

To download and use the pre-built Docker images for the client and server, use the following commands, make sure use the exact tag number:

#### Pull the Server Image
```bash
docker pull kingxxh/grpc-pet-adoption-server:2.0.0
```
Alternatively, you can manually download the server image from [Docker Hub Server Image](https://hub.docker.com/repository/docker/kingxxh/grpc-pet-adoption-server/general).

#### Pull the Client (CLI Version) Image
```bash
docker pull kingxxh/pet-adoption-client-cli:3.0.0
```
Alternatively, you can manually download the client image from [Docker Hub Client Image](https://hub.docker.com/repository/docker/kingxxh/pet-adoption-client-cli/general).

### Step 2: Run System by using docker-compose.yml

Automatically run the system by using docker-compose run Command  
With this method, you can set up and launch the entire system (server and client) with a single command by using a docker-compose.yml file.

#### Detailed steps:
- **Prepare the docker-compose.yml file**: Find the provided docker-compose.yml in the zip file, and place it in any folder where you plan to run the system.
- **Run the system**: Once the docker-compose.yml file is in place, navigate to its location in your terminal or command prompt and use the following command to start both the server and the CLI client:

```bash
docker-compose run pet-adoption-client-cli
```

### Step 4: Using the CLI Client

Once the client container is running, you'll be prompted to interact with the system using the following options:

1. Register a Pet
2. Search for a Pet
3. Exit

#### Registering a Pet
To register a pet, follow the prompts to enter the pet's details:
- Name
- Gender (Male/Female)
- Age (in years)
- Breed
- File path to the pet's photo

#### Searching for a Pet
To search for a pet, select the search option and enter the criteria (name, gender, age, or breed).


### Option 2: Run GUI Version Client (Python-based, outside Docker)

If you want to run the GUI version of the client, you can do so by running the Python script directly on your local machine. This version provides a graphical interface using `tkinter`.

### Prerequisites

### Step 1:  Server-side:

First, make sure you run the server by using below command in the location where you place the docker-compose.yml.
```bash
docker-compose up
```
This will run the server automatically, allow you to use the GUI client to communicate with the server.
### Step 2: Install Python Dependencies

Ensure you have Python 3.11 installed, and install the required Python packages:
- Python 3.11
- Required Python packages: `grpcio`, `grpcio-tools`, `google-api-python-client`, `Pillow`, `protobuf`
- You can check the specific version number below, or find the requirements.txt file in the client directory of the compressed package to view the necessary dependencies or packages. Or just run the command below in the project's client directory to install dependencies in one step:
```bash
pip install -r requirements.txt
```


### Step 3: Running the GUI Client

Once the dependencies are installed, navigate to the client directory and run the GUI version using the following command:

```bash
python client_gui.py
```

The GUI will launch, allowing you to register and search for pets visually.

## Development

### Regenerating gRPC Files (Protobuf)
If you modify the `.proto` files, you'll need to regenerate the gRPC classes.

For Python:
```bash
python -m grpc_tools.protoc -I./ --python_out=. --grpc_python_out=. ./pet_adoption.proto
```

For Java (server):
Ensure that your build system (Gradle) is configured to compile the `.proto` files.


## Dependencies

### Server
- `grpc-java`
- `protobuf-java`
- `Gradle`

### Client
- `grpcio==1.66.2`
- `grpcio-tools==1.66.2`
- `google-api-python-client==2.100.0`
- `Pillow==10.4.0`
- `protobuf==5.28.2`
- `setuptools==75.1.0`
- `tk==0.1.0`



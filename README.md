# Pet Adoption System - gRPC Backed Virtual Pet Adoption System

This project is a gRPC-backed virtual pet adoption system. The system includes both server and client components, allowing users to register pets and search for pets available for adoption.

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

To download and use the pre-built Docker images for the client and server, use the following commands:

#### Pull the Server Image
```bash
docker pull kingxxh/grpc-pet-adoption-server
```
Alternatively, you can manually download the server image from [Docker Hub Server Image](https://hub.docker.com/repository/docker/kingxxh/grpc-pet-adoption-server/general).

#### Pull the Client (CLI Version) Image
```bash
docker pull kingxxh/pet-adoption-client-cli
```
Alternatively, you can manually download the client image from [Docker Hub Client Image](https://hub.docker.com/repository/docker/kingxxh/pet-adoption-client-cli/general).

### Step 2: Docker Network Setup

Create a Docker network to ensure communication between the client and server containers.
```bash
docker network create pet-adoption-network
```

### Step 3: Running the Containers

#### Running the Server
```bash
docker run -d --name grpc-pet-adoption-server --network pet-adoption-network -p 50051:50051 grpc-pet-adoption-server
```

#### Running the Client (CLI Version)
```bash
docker run -it --name pet-adoption-client-cli --network pet-adoption-network pet-adoption-client-cli
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

### Step 5: Cleaning Up

To stop and remove the containers after use:
```bash
docker stop grpc-pet-adoption-server pet-adoption-client-cli
docker rm grpc-pet-adoption-server pet-adoption-client-cli
```

If you want to remove the Docker network:
```bash
docker network rm pet-adoption-network
```

### Option 2: Run GUI Version (Python-based, outside Docker)

If you want to run the GUI version of the client, you can do so by running the Python script directly on your local machine. This version provides a graphical interface using `tkinter`.

### Prerequisites

#### Client-side:
- Python 3.11
- Required Python packages: `grpcio`, `grpcio-tools`, `google-api-python-client`, `Pillow`, `protobuf`

### Step 1: Install Python Dependencies

Ensure you have Python 3.11 installed, and install the required Python packages:

```bash
pip install grpcio grpcio-tools google-api-python-client Pillow protobuf
```

### Step 2: Running the GUI Client

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
Ensure that your build system (e.g., Maven/Gradle) is configured to compile the `.proto` files.

## Dependencies

### Server
- `grpc-java`
- `protobuf-java`

### Client
- `grpcio==1.57.0`
- `grpcio-tools==1.57.0`
- `google-api-python-client==2.100.0`
- `Pillow==9.2.0`
- `protobuf==5.27.2`

## Troubleshooting

- **Issue**: `ModuleNotFoundError: No module named 'grpc'`
  - **Solution**: Ensure that `grpcio` and `grpcio-tools` are installed in the Python environment, and confirm that the Docker image has been built correctly.

- **Issue**: `failed to connect to all addresses; last error: UNKNOWN`
  - **Solution**: Ensure that the client and server are running on the same Docker network and that the correct port is mapped.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

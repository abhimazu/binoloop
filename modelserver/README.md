# Triton Inference Server

## Introduction

This document provides guidance on setting up and running the Nvidia Triton Inference Server, configured with two custom machine learning models: phi-2 and gemma. Each model is set up with its unique Python execution environment and configuration to facilitate diverse inference tasks.

### Prerequisites

Before you begin, ensure you have the following installed:

- **Docker**: Triton Server will be run within a Docker container. Install Docker if it's not already installed.

**Directory Structure**

```
/modelserver
|-- models
|   |-- phi-2
|   |   |-- 1
|   |   |   |-- model.py
|   |   |   |-- config.pbtxt
|   |-- gemma
|   |   |-- 1
|   |   |   |-- model.py
|   |   |   |-- config.pbtxt
|-- Dockerfile
|-- docker-compose.yml
```

- *model.py*: Python script tailored for each model to execute specific machine learning tasks.
- *config.pbtxt*: Configuration file for each model, specifying operational parameters for the Triton server.

### Clone the Repository

To get started, clone this repository to your local machine:

```
git clone https://github.com/abhimazu/binoloop.git
git checkout trition_server
cd binoloop/modelserver
```

## Docker Setup

The provided Dockerfile is configured to run Triton Server with your models:

```
FROM nvcr.io/nvidia/tritonserver:23.06-py3

RUN pip install torch transformers

RUN mkdir /models

ADD ./phi-2 /models/phi-2
ADD ./gemma /models/gemma

CMD ["tritonserver", "--model-repository=/models"]
```
A docker-compose file is created to build and run the server:

```
version: '3.8'  
services:
  tritonserver:
    build: 
      context: .  
      dockerfile: Dockerfile  
    ports:
      - "8000:8000"  # Port mapping for HTTP requests
      - "8001:8001"  # Port mapping for gRPC requests
      - "8002:8002"  # Port mapping for metrics
    volumes:
      - type: bind
        source: ./models
        target: /models

    restart: unless-stopped
```

Run the docker-compose file to build and deploy your Trition Server:

'''
docker-compose up
'''

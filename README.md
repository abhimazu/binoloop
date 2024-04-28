# Github Actions CI/CD Pipeline

This repository has a basic implementation of a CI/CD pipeline implemented for the project. In comparison to the **main** branch, this branch has three additional files: [test_client.py](https://github.com/abhimazu/binoloop/blob/cicd_github_actions/client/test_client.py), [test_server.py](https://github.com/abhimazu/binoloop/blob/cicd_github_actions/server/test_server.py), and [ci-cd-pipeline.yml](https://github.com/abhimazu/binoloop/blob/cicd_github_actions/.github/workflows/ci-cd-pipeline.yml)

Here is the folder structure of the repo with the added files:

```
binoloop/
│
├── .github/
│   └── workflows/
│       └── ci-cd-pipeline.yml  # **GitHub Actions workflow file**
│
├── server/
│   ├── docker-compose.yml
│   ├── Dockerfile
│   ├── run.sh
│   ├── requirements.txt
│   ├── server.py
│   └── test_server.py          # **Pytest tests for server**
│
├── client/
│   ├── run.sh
│   ├── requirements.txt
│   ├── modelclient.py
│   └── test_client.py          # **Pytest tests for client**
│
└── README.md                   
```

The **test_server** and **test_client** files contain unit tests for individual functions inside the **server.py** and **client.py** files that shall be triggered by the **actions workflow file**. The workflow ensures that every push and pull request to the main branch triggers a series of checks and operations to maintain code quality and deployment readiness.

## Workflow Overview

### Trigger Events:

- Push and Pull Requests: Triggered on any push or pull request to the main branch, ensuring all changes are automatically built and tested.

```
name: Python Application CI/CD Pipeline

on:
  push:
    branches:
      - cicd_github_actions
  pull_request:
    branches:
      - cicd_github_actions
```

## Jobs and Steps:

1. ### Build and Test

- Environment: The workflow runs on the latest Ubuntu runner provided by GitHub Actions.
- Python Setup: Python 3.9 is set up for compatibility and consistency across test and build environments.

```
jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2

      - name: Set up Python 3.9
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
```

**Dependency Installation:**

Dependencies for both the server and client components are installed separately, using their respective requirements.txt files.

```
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install pytest pytest-mock
    if [ -d "server/" ]; then
      pip install -r server/requirements.txt
    fi
    if [ -d "client/" ]; then
      pip install -r client/requirements.txt
    fi
```

**Testing:**

Automated tests are run separately for both the server and client using pytest to ensure that each component functions as expected independently.

```
- name: Run tests in Server
        run: |
          cd server
          pytest

      - name: Run tests in Client
        run: |
          cd client
          pytest
  ```

2. ### Docker Build for Server

- **Conditionally Executed**: Only runs if changes are detected in the server directory.
- **Process**: Builds a Docker image from the Dockerfile located in the server directory. This ensures that the server can be containerized consistently with every change.

```
      - name: Build Docker Image for Server
        run: |
          if [ -d "server/" ]; then
            cd server
            docker build -t fastapi-server .
          fi
      
      - name: Run Docker Container
        if: ${{ github.workspace }}/server
        run: |
          docker run -d -p 8000:8000 fastapi-server
```
- **Uploads to Docker Registry**: Logs in to the configured Dockerhub account and uploads the successfully tested image to the registry with the **:latest** tag
- 
```
- name: Docker login
        uses: docker/login-action@v1
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

- name: Push Docker image to registry
  run: |
    docker tag fastapi-server ${{ secrets.DOCKER_REGISTRY_URL }}/fastapi-server:latest
    docker push ${{ secrets.DOCKER_REGISTRY_URL }}/fastapi-server:latest
```

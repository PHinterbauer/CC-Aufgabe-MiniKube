# Content

This project is for educational purpose. It illustrates a project with some relevant tools for DevOps.

## Quickstart

### Run the full stack with Docker Compose

```sh
docker compose up --build
```

After the containers start, open:

| Service | URL |
| ------- | --- |
| Client | http://localhost:8080 |
| Server API | http://localhost:8000 |
| Grafana | http://localhost:3000 |
| Prometheus | http://localhost:9090 |

Stop the stack with:

```sh
docker compose down
```

### Run the server locally

```sh
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[test]"
uvicorn app.main:app --reload --app-dir server/src
```

The FastAPI server is available at http://localhost:8000.

Run the test suite with:

```sh
pytest
```

## Code
This repository contains a small FastAPI app in `server/src/app` and a simple Nginx client in `client/`.

## Dockerfile
The server Dockerfile lives at `server/Dockerfile` and builds the FastAPI app.

````sh
docker build -t test-server:latest -f server/Dockerfile .
docker run -p 8000:8000 test-server:latest
````

## Docker Compose
This repository contains a `docker-compose.yml` that starts the FastAPI server and the Nginx client.

````yml
services:
  server:
    build:
      context: .
      dockerfile: server/Dockerfile
    container_name: test_server
    ports:
      - "8000:8000"
  client:
    build:
      context: ./client
      dockerfile: Dockerfile
    container_name: test_client
    depends_on:
      - server
    ports:
      - "8080:80"
````

````sh
docker compose up --build
````

## Workflow
To demonstrate CI in GitHub, the workflow runs tests and imports the FastAPI app. The workflow is defined in `.github/workflows/CI.yml`.

## Local Deployment Simulation
A "deployment" via docker compose is defined in:
````sh
.\deploy-local.ps1
````

## Minikube
The `myapp.yml` contains deployment rules for **Minkube** and deploys **only the server** (no frontend is served via Kubernetes in this setup). Minkube has to be downloaded, e.g. *https://minikube.sigs.k8s.io/docs/start/* (eventually `minikube` has to be set as environment variable).

````sh
.\deploy-minikube.ps1
````

The service can be stopped with

````sh
.\stop-minikube.ps1
````

## Monitoring & Logging
In the ``docker-compose.yml`` images of **Grafana** and **Prometheus** are included. A simple dashboard is defined in `./grafana/dashboards`. In `./grafana/provisioning` the dashboard is provided and the Prometheus is set as data source.

*Note:* The server needs a route `/metrics` (see. `./server/src/app/main.py`) to work with Prometheus. In the `prometheus.yml` the block

````yml
  - job_name: "server"
    metrics_path: /metrics
    static_configs:
      - targets: ["server:8000"]
````
tells Prometheus to scrape http://server:8000/metrics (within the container!) and attach the label job="server" to those metrics (it pulls the data into Prometheus’ time‑series database with that job label.)

# Ports
The script `deploy-local.ps1` will run `docker-compose.yml`. The services run on `127.0.0.1` (localhost) following ports:
| Service                  | Port |
| ------------------------ | ---- |
| Client (nginx)           | 8080 |
| Server (python fastapi)  | 8000 |
| Grafana                  | 3000 |
| Prometheus               | 9090 |


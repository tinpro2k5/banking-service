# Banking Service

This project is a microservice-based banking support system built from the banking-ai-agent workflow.

## Architecture

- `backend` is a FastAPI service that receives customer messages, calls the intent service over gRPC, retrieves policy text, generates a draft reply through an Ollama endpoint, validates the result, and returns a structured response.
- `intent-service` is an independent gRPC microservice that predicts the customer intent and confidence score.
- Ollama is used as an external model endpoint, not a container in the current Docker Compose setup.
- `frontend` is a simple Streamlit UI that sends messages to the backend service.

## gRPC code generation

The intent service includes `intent_service.proto` plus compatibility modules for local development. To regenerate the gRPC files, run:

```bash
cd intent_service
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. intent_service.proto
```

## Build Docker images

```bash
docker compose build
```

## Run the system

```bash
docker compose up
```

The services will be available on:

- Frontend: `http://localhost:8501`
- Backend: `http://localhost:8000`
- Intent Service: `localhost:50051`
- Ollama endpoint: `http://host.docker.internal:11434` (from containers)

## Container roles

- `backend`: orchestrates the full workflow and exposes the HTTP API.
- `intent-service`: predicts the banking intent through gRPC.
- `frontend`: provides a simple user interface.
- Ollama is expected to be reachable as an external endpoint.

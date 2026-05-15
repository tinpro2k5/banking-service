# Banking Service

This project is a microservice-based banking support system built from the banking-ai-agent workflow.

## Architecture

- `api-gateway` is a FastAPI service that receives customer messages, calls the intent service over gRPC, retrieves policy text, generates a draft reply through Ollama, validates the result, and returns a structured response.
- `intent-service` is an independent gRPC microservice that predicts the customer intent and confidence score.
- `ollama` serves the language model used for response generation.
- `frontend` is a simple Streamlit UI that sends messages to the API gateway.

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
- API Gateway: `http://localhost:8000`
- Intent Service: `localhost:50051`
- Ollama: `http://localhost:11434`

## Container roles

- `api-gateway`: orchestrates the full workflow and exposes the HTTP API.
- `intent-service`: predicts the banking intent through gRPC.
- `ollama`: provides the model endpoint for response generation.
- `frontend`: provides a simple user interface.

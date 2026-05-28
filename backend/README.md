# Banking Service Backend

This folder contains the backend API service for the banking microservice system.

Endpoints:

- `GET /health`
- `GET /config`
- `POST /run-agent`

The backend calls the intent service through gRPC and an Ollama endpoint through HTTP.

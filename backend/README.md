# Banking Service Backend

This folder contains the API Gateway for the banking microservice system.

Endpoints:

- `GET /health`
- `GET /config`
- `POST /run-agent`

The gateway calls the intent service through gRPC and Ollama through HTTP.

# API Gateway Backend

This folder contains the FastAPI API Gateway for the Banking Service project. It is the main HTTP entry point of the system and is responsible for orchestrating the full banking agent workflow.

## Role In The System

The API Gateway receives customer messages from the frontend or external clients, then coordinates the following workflow:

```text
Customer message
  -> Intent Node via gRPC Intent Service
  -> Priority Node
  -> Policy Node
  -> Draft Node via Ollama HTTP API
  -> Validation Node
  -> Router Node
  -> Final structured response
```

The backend communicates with:

- `intent-service` through gRPC for intent prediction.
- External Ollama server through HTTP for response generation.
- `frontend` through HTTP requests from the Streamlit UI.

## API Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/health` | Check whether the API Gateway is running. |
| `GET` | `/config` | Return the active runtime configuration. |
| `POST` | `/run-agent` | Run the full banking agent workflow. |
| `POST` | `/chat` | Alias endpoint that runs the same workflow as `/run-agent`. |

Example request:

```bash
curl -X POST http://localhost:8000/run-agent \
  -H "Content-Type: application/json" \
  -d "{\"message\":\"My card payment was declined yesterday.\"}"
```

Example response fields:

- `intent`
- `priority`
- `policy`
- `draft`
- `validation`
- `routing`
- `final_reply`

## gRPC Client Files

The backend imports generated gRPC client files from:

```text
backend/app/clients/intent_grpc/
  intent_service_pb2.py
  intent_service_pb2_grpc.py
```

These files are generated from:

```text
intent_service/intent_service.proto
```

After running `make` inside `intent_service`, copy the generated files into `backend/app/clients/intent_grpc/`.

The root `docker-compose.yml` sets:

```yaml
PYTHONPATH: /src:/src/app/clients/intent_grpc
```

This makes the generated gRPC modules importable inside the API Gateway container.

## Environment Variables

The backend uses these main environment variables:

| Variable | Example | Description |
| --- | --- | --- |
| `INTENT_SERVICE_HOST` | `intent-service` | Hostname of the gRPC intent service inside Docker Compose. |
| `INTENT_SERVICE_PORT` | `50051` | Port of the gRPC intent service. |
| `INTENT_SERVICE_TIMEOUT` | `20.0` | Timeout for gRPC intent prediction. |
| `OLLAMA_BASE_URL` | `http://host.docker.internal:11434` | External Ollama server URL. Replace this with the Colab/tunnel URL if Ollama is hosted from Colab. |
| `OLLAMA_MODEL` | `gpt-oss:20b` | Ollama model used for response generation. |
| `FRONTEND_BASE_URL` | `http://frontend:8501` | Frontend URL used in configuration output. |

## Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the API Gateway:

```bash
python run.py
```

The backend will be available at:

```text
http://localhost:8000
```

Local execution requires a reachable intent service and Ollama endpoint. For the complete multi-container setup, run Docker Compose from the project root.

## Run With Docker Compose

From the project root:

```bash
docker compose up --build
```

The API Gateway container is named `api-gateway` in `docker-compose.yml` and exposes port `8000`.

## Important Files

```text
app/main.py                       FastAPI endpoints
app/agent/orchestrator.py         Full workflow orchestration
app/clients/grpc_intent_client.py gRPC client for intent-service
app/clients/ollama_client.py      HTTP client for Ollama
app/nodes/intent_node.py          Calls the gRPC intent service
app/nodes/priority_node.py        Priority/risk detection
app/nodes/policy_node.py          Policy retrieval
app/nodes/draft_node.py           Ollama response generation
app/nodes/validation_node.py      Draft validation
app/nodes/router_node.py          Final action routing
```

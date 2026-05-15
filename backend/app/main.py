"""FastAPI application that exposes the API gateway endpoints."""

from fastapi import FastAPI

from app.agent.orchestrator import Orchestrator
from app.core.schemas import AgentResponse, CustomerRequest, SystemConfig
from app.core.settings import settings


app = FastAPI(title="Banking Service API Gateway")
orchestrator = Orchestrator()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/config", response_model=SystemConfig)
def config() -> SystemConfig:
    return SystemConfig(
        api_host=settings.api_host,
        api_port=settings.api_port,
        intent_service_host=settings.intent_service_host,
        intent_service_port=settings.intent_service_port,
        intent_service_timeout=settings.intent_service_timeout,
        ollama_base_url=settings.ollama_base_url,
        ollama_model=settings.ollama_model,
        frontend_base_url=settings.frontend_base_url,
    )


@app.post("/run-agent", response_model=AgentResponse)
def run_agent(request: CustomerRequest) -> AgentResponse:
    return orchestrator.run(request.message)


@app.post("/chat", response_model=AgentResponse)
def chat(request: CustomerRequest) -> AgentResponse:
    return orchestrator.run(request.message)

"""gRPC server for the intent service."""

from __future__ import annotations

from concurrent import futures

import grpc

from app.core.settings import settings
from app.nodes.intent_node import IntentNode
import intent_service_pb2
import intent_service_pb2_grpc


class IntentService(intent_service_pb2_grpc.IntentServiceServicer):
    def __init__(self) -> None:
        self._classifier = IntentNode()

    def PredictIntent(self, request, context):
        result = self._classifier.run(request.message)
        return intent_service_pb2.IntentResponse(
            intent=result.intent,
            confidence=float(result.confidence),
            reason=result.reason,
        )


def serve() -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    intent_service_pb2_grpc.add_IntentServiceServicer_to_server(IntentService(), server)
    server.add_insecure_port(f"{settings.grpc_host}:{settings.grpc_port}")
    server.start()
    print(f"Intent service listening on {settings.grpc_host}:{settings.grpc_port}")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()

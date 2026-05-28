"""Compatibility gRPC helpers for the intent service."""

from __future__ import annotations

import grpc

from app.clients.intent_grpc import intent_service_pb2 as intent__service__pb2

SERVICE_NAME = "intent_classify.v1.IntentService"


class IntentServiceStub:
    def __init__(self, channel: grpc.Channel) -> None:
        self.IntentRecognizer = channel.unary_unary(
            f"/{SERVICE_NAME}/IntentRecognizer",
            request_serializer=lambda request: request.SerializeToString(),
            response_deserializer=intent__service__pb2.IntentResponse.FromString,
        )


class IntentServiceServicer:
    def IntentRecognizer(self, request, context):  # pragma: no cover - interface only
        raise NotImplementedError()


def add_IntentServiceServicer_to_server(servicer: IntentServiceServicer, server: grpc.Server) -> None:
    rpc_method_handlers = {
        "IntentRecognizer": grpc.unary_unary_rpc_method_handler(
            servicer.IntentRecognizer,
            request_deserializer=intent__service__pb2.IntentRequest.FromString,
            response_serializer=lambda response: response.SerializeToString(),
        )
    }
    generic_handler = grpc.method_handlers_generic_handler(SERVICE_NAME, rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

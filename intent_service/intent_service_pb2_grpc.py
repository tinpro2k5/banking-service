"""Compatibility gRPC helpers for the intent service."""

from __future__ import annotations

import grpc

import intent_service_pb2 as intent__service__pb2

SERVICE_NAME = "intent_classify.v1.IntentService"


class IntentServiceStub:
    def __init__(self, channel: grpc.Channel) -> None:
        self.PredictIntent = channel.unary_unary(
            f"/{SERVICE_NAME}/PredictIntent",
            request_serializer=lambda request: request.SerializeToString(),
            response_deserializer=intent__service__pb2.IntentResponse.FromString,
        )


class IntentServiceServicer:
    def PredictIntent(self, request, context):  # pragma: no cover - interface only
        raise NotImplementedError()


def add_IntentServiceServicer_to_server(servicer: IntentServiceServicer, server: grpc.Server) -> None:
    rpc_method_handlers = {
        "PredictIntent": grpc.unary_unary_rpc_method_handler(
            servicer.PredictIntent,
            request_deserializer=intent__service__pb2.IntentRequest.FromString,
            response_serializer=lambda response: response.SerializeToString(),
        )
    }
    generic_handler = grpc.method_handlers_generic_handler(SERVICE_NAME, rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))

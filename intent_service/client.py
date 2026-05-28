"""Small local client for testing the gRPC intent service."""

from __future__ import annotations

import grpc

import intent_service_pb2
import intent_service_pb2_grpc


def predict(message: str, target: str = "localhost:50051") -> intent_service_pb2.IntentResponse:
    with grpc.insecure_channel(target) as channel:
        stub = intent_service_pb2_grpc.IntentServiceStub(channel)
        return stub.IntentRecognizer(intent_service_pb2.IntentRequest(message=message))


if __name__ == "__main__":
    result = predict("My card payment was declined at the supermarket")
    print(result)

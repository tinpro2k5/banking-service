"""Small local client for testing the gRPC intent service."""

from __future__ import annotations

import argparse
import grpc

import intent_service_pb2
import intent_service_pb2_grpc


def predict(message: str, target: str = "localhost:50051") -> intent_service_pb2.IntentResponse:
    """Call the remote IntentRecognizer RPC and return the IntentResponse."""
    with grpc.insecure_channel(target) as channel:
        stub = intent_service_pb2_grpc.IntentServiceStub(channel)
        return stub.IntentRecognizer(intent_service_pb2.IntentRequest(message=message))


def main() -> None:
    parser = argparse.ArgumentParser(description="Simple gRPC client for intent_service")
    parser.add_argument("--target", "-t", default="localhost:50051",
                        help="gRPC target in the form host:port (default: localhost:50051)")
    parser.add_argument("--message", "-m", required=False,
                        default="My card payment was declined at the supermarket",
                        help="Customer message to classify")
    args = parser.parse_args()

    try:
        result = predict(args.message, target=args.target)
        print(result)
    except Exception as exc:
        print(f"gRPC call failed: {exc}")


if __name__ == "__main__":
    main()

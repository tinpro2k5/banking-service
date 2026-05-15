PROTO=intent_service.proto
GENERATED=intent_service_pb2.py intent_service_pb2_grpc.py

all: $(GENERATED)

$(GENERATED): $(PROTO)
	python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. $(PROTO)

run:
	python server.py

clean:
	rm -f $(GENERATED)

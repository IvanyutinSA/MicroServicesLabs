from pathlib import Path

import grpc

from test_utils.test_suit import TestSuit
from src.user_service.server import setup_server
from src.middleware.jwt_controller import JWTController

import src.user_service.protos.user_service_pb2_grpc as user_service_pb2_grpc
import src.user_service.protos.user_service_pb2 as user_service_pb2


class TestMTLS(TestSuit):
    def __init__(self):
        self.server = setup_server(secure=True)

    def test_(self):
        was_connected = False

        certs_dir = Path("certs")

        with open(certs_dir / "ca-bundle.pem", 'rb') as f:
            root_certificates = f.read()

        with open(certs_dir / "client-cert.pem", 'rb') as f:
            certificate_chain = f.read()

        with open(certs_dir / "client-key.pem", 'rb') as f:
            private_key = f.read()

        credentials = grpc.ssl_channel_credentials(
                root_certificates=root_certificates,
                private_key=private_key,
                certificate_chain=certificate_chain
                )

        with grpc.secure_channel("localhost:50051", credentials) as _:
            was_connected = True

        self.assert_true(was_connected)

    def __enter__(self):
        self.server.start()
        return self

    def __exit__(self, *args, **kargs):
        self.server.stop(0)
        pass

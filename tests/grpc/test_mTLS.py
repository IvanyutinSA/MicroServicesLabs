from pathlib import Path

import grpc

from src.utilities.folk_certificate_controller import FolkCertificateController

from test_utils.test_suit import TestSuit
from src.user_service.server import setup_server
from src.middleware.jwt_controller import JWTController

import src.user_service.protos.user_service_pb2_grpc as user_service_pb2_grpc
import src.user_service.protos.user_service_pb2 as user_service_pb2


class TestMTLS(TestSuit):
    def __init__(self):
        self.server = setup_server(secure=True)

    def test_folk(self):
        was_connected = False
        controller = FolkCertificateController()

        credentials = grpc.ssl_channel_credentials(
                **controller.get_channel_credentials('client'))

        with grpc.secure_channel("localhost:50051", credentials) as channel:
            was_connected = True

        self.assert_true(was_connected)

    def __enter__(self):
        self.server.start()
        return self

    def __exit__(self, *args, **kargs):
        self.server.stop(0)
        pass

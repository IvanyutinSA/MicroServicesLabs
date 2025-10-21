import grpc
from pathlib import Path

import src.user_service.protos.user_service_pb2_grpc as user_service_pb2_grpc
import src.user_service.protos.user_service_pb2 as user_service_pb2


class UserServiceApi:
    def __init__(self):
        self.credentials = self._get_credentials()

    def _get_credentials(self):
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
                certificate_chain=certificate_chain)
        return credentials

    def _status_error(self, status):
        raise Exception(
                f'Register terminated with status {status}')

    def _connection_error(self):
        raise Exception('Cannot connect to server')

    def register(self, username, password, role='user'):
        with grpc.secure_channel('localhost:50051',
                                 self.credentials) as channel:
            stub = user_service_pb2_grpc.UserServiceStub(channel)

            request = user_service_pb2.RegisterRequest(
                    user_name=username, password=password, role=role)
            reply = stub.Register(request)
            if reply.status:
                self._status_error(reply.status)
            return 'Success'
        self._connection_error()

    def authenticate(self, username, password):
        with grpc.secure_channel('localhost:50051',
                                 self.credentials) as channel:
            stub = user_service_pb2_grpc.UserServiceStub(channel)

            request = user_service_pb2.AuthenticateRequest(
                    user_name=username, password=password)
            reply = stub.Authenticate(request)
            if reply.status:
                self._status_error(reply.status)
            return 'Success'
        self._connection_error()

    def user_get_information(self, username=None):
        with grpc.secure_channel('localhost:50051',
                                 self.credentials) as channel:
            stub = user_service_pb2_grpc.UserServiceStub(channel)
            request = user_service_pb2.UserGetInformationRequest(
                    user_name=username)
            reply = stub.UserGetInformation(request)
            if reply.status:
                self._status_error(reply.status)
            return f'\nusername: {reply.user_name}\nrole: {reply.role}'
        self._connection_error()

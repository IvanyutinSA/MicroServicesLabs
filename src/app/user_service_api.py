import grpc
import msgpack

from pathlib import Path

from src.vk_auth_service.vk_auth_service import VkAuthService

import src.user_service.protos.user_service_pb2_grpc as user_service_pb2_grpc
import src.user_service.protos.user_service_pb2 as user_service_pb2

from src.utilities.folk_certificate_controller import FolkCertificateController


class UserServiceApi:
    def __init__(self):
        controller = FolkCertificateController()
        self.credentials = grpc.ssl_channel_credentials(
                **controller.get_channel_credentials('user-service'))

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

    def authenticate_vk(self):
        vk_service = VkAuthService()
        data = vk_service.authorize()
        data = msgpack.unpackb(data)
        username = data.get('username', None)
        password = data.get('password', None)
        self.register(username, password)
        return self.authenticate(username, password)

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

import grpc

from test_utils.test_suit import TestSuit
from src.user_service.server import setup_server
from src.middleware.jwt_controller import JWTController

import src.user_service.protos.user_service_pb2_grpc as user_service_pb2_grpc
import src.user_service.protos.user_service_pb2 as user_service_pb2


class TestUserService(TestSuit):
    def __init__(self):
        self.server = setup_server()

    def test_register(self):
        with grpc.insecure_channel("localhost:50051") as channel:
            stub = user_service_pb2_grpc.UserServiceStub(channel)
            user_name = 'user_register'
            password = 'password'
            role = 'user'

            request = user_service_pb2.RegisterRequest(
                    user_name=user_name, password=password, role=role)
            reply_positive = stub.Register(request)

            request = user_service_pb2.RegisterRequest(
                    user_name=user_name, password=password, role=role)
            reply_negative = stub.Register(request)

            self.assert_eq(reply_positive.status, 0)
            self.assert_eq(reply_negative.status, 1)

    def test_register_admin(self):
        with grpc.insecure_channel("localhost:50051") as channel:
            stub = user_service_pb2_grpc.UserServiceStub(channel)
            user_name = 'user_register_admin'
            password = 'password'
            role = 'admin'

            jwt_controller = JWTController()
            jwt_controller.generate('user_name', 'user')

            request = user_service_pb2.RegisterRequest(
                    user_name=user_name,
                    password=password,
                    role=role)
            reply_no_permission = stub.Register(request)

            jwt_controller = JWTController()
            jwt_controller.generate('user_name', 'admin')

            request = user_service_pb2.RegisterRequest(
                    user_name=user_name,
                    password=password,
                    role=role)
            reply_registration_success = stub.Register(request)

            self.assert_eq(reply_no_permission.status, 2)
            self.assert_eq(reply_registration_success.status, 0)

    def test_authenticate(self):
        with grpc.insecure_channel("localhost:50051") as channel:
            stub = user_service_pb2_grpc.UserServiceStub(channel)
            user_name = 'user_authenticate'
            unknown_name = 'unknown_name'
            password = 'password'
            role = 'user'
            wrong_password = 'wrong_password'

            request = user_service_pb2.RegisterRequest(
                    user_name=user_name, password=password, role=role)
            _ = stub.Register(request)

            request = user_service_pb2.AuthenticateRequest(
                    user_name=user_name, password=password)
            reply_positive = stub.Authenticate(request)

            request = user_service_pb2.AuthenticateRequest(
                    user_name=unknown_name, password=password)
            reply_unkown_name = stub.Authenticate(request)

            request = user_service_pb2.AuthenticateRequest(
                    user_name=user_name, password=wrong_password)
            reply_wrong_password = stub.Authenticate(request)

            self.assert_eq(reply_positive.status, 0)
            self.assert_eq(reply_unkown_name.status, 1)
            self.assert_eq(reply_wrong_password.status, 1)

    def test_user_get_information(self):
        with grpc.insecure_channel("localhost:50051") as channel:
            stub = user_service_pb2_grpc.UserServiceStub(channel)
            user_name = 'user_name_user_get_information'
            role = 'user'
            unknown_name = 'uknown_name'
            password = 'password'

            request = user_service_pb2.RegisterRequest(
                    user_name=user_name, password=password, role=role)
            _ = stub.Register(request)

            request = user_service_pb2.AuthenticateRequest(
                    user_name=user_name, password=password)
            _ = stub.Authenticate(request)

            request = user_service_pb2.UserGetInformationRequest(
                    user_name=user_name)
            reply_positive = stub.UserGetInformation(request)

            request = user_service_pb2.UserGetInformationRequest(
                    user_name=unknown_name)
            reply_negative = stub.UserGetInformation(request)

            self.assert_eq(reply_positive.status, 0)
            self.assert_eq(reply_positive.user_name, user_name)

            self.assert_eq(reply_negative.status, 1)
            self.assert_eq(reply_negative.user_name, '')

    def __enter__(self):
        self.server.start()
        return self

    def __exit__(self, *args, **kargs):
        self.server.stop(0)
        pass

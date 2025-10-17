from hashlib import sha256

from concurrent import futures
import logging

import grpc
import src.user_service.protos.user_service_pb2 as user_service_pb2
import src.user_service.protos.user_service_pb2_grpc as user_service_pb2_grpc
from src.middleware.jwt_controller import JWTController

fool = {'user_name': 'fool',
        'hashed_password': 'dsKJx2@1s>',
        'role': 'admin'}

alice = {'user_name': 'Alice',
         'hashed_password': 'password',
         'role': 'user'}

bob = {'user_name': 'Bob',
       'hashed_password': 'password',
       'role': 'user'}

users = [fool, alice, bob]


class UserServiceServicer(user_service_pb2_grpc.UserServiceServicer):
    def __init__(self):
        self.jwt_controller = JWTController()

    def Register(self, request, context):
        user_name = request.user_name
        password = request.password
        role = request.role

        if any([user_name == user['user_name'] for user in users]):
            return user_service_pb2.RegisterReply(status=1)

        if not self.jwt_controller.get_access('Register',
                                              role=role,
                                              is_special=True):
            return user_service_pb2.RegisterReply(status=2)

        user = {'user_name': user_name,
                'hashed_password': sha256(
                    password.encode('utf-8')).hexdigest(),
                'role': role}

        users.append(user)

        return user_service_pb2.RegisterReply(status=0)

    def Authenticate(self, request, context):
        user_name = request.user_name
        password = request.password

        user = [user for user in users
                if user['user_name'] == user_name]

        if not user:
            return user_service_pb2.AuthenticateReply(status=1)

        user = user[0]

        if user['hashed_password'] != sha256(
                password.encode('utf-8')).hexdigest():
            return user_service_pb2.AuthenticateReply(status=1)

        self.jwt_controller.generate(user['user_name'], role=user['role'])

        return user_service_pb2.AuthenticateReply(status=0)

    def UserGetInformation(self, request, context):
        user_name = request.user_name
        user = [user for user in users
                if user['user_name'] == user_name]
        if not user:
            return user_service_pb2.UserGetInformationReply(status=1)
        user = user[0]

        if not self.jwt_controller.get_access('UserGetInformation',
                                              user_name=user_name):
            return user_service_pb2.UserGetInformationReply(status=2)
        return user_service_pb2.UserGetInformationReply(
                status=0, user_name=user_name, role=user['role'])


def setup_server():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_service_pb2_grpc.add_UserServiceServicer_to_server(
            UserServiceServicer(), server)
    server.add_insecure_port("[::]:" + port)
    return server


if __name__ == "__main__":
    logging.basicConfig()
    server = setup_server()
    server.start()
    print("Server going to listening on " + 50051)
    server.wait_for_termination()

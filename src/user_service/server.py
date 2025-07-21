from hashlib import sha256

from concurrent import futures
import logging

import grpc
from protos import user_service_pb2
from protos import user_service_pb2_grpc
# import protos.user_service_pb2 as user_service_pb2
# import protos.user_service_pb2_grpc as user_service_pb2_grpc


users = []


class UserService(user_service_pb2_grpc.UserService):
    def RegisterRequest(self, request, context):
        user_name = request.user_name
        password = request.password

        if any([user_name == user['user_name'] for user in users]):
            return user_service_pb2.RegisterReply(status=1)

        user = {'user_name': user_name,
                "hashed_password": sha256(
                    password.encode('utf-8')).hexdigest()}

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

        if user['password'] != sha256(
                password.encode('utf-8')).hexdigest():
            return user_service_pb2.AuthenticateReply(status=1)

        return user_service_pb2.AuthenticateReply(status=1)

    def UserGetInformation(self, request, context):
        user_name = request.user_name
        user = [user for user in users
                if user['user_name'] == user_name]
        if not user:
            return user_service_pb2.UserGetInformationReply(status=1)
        user = user[0]

        return user_service_pb2.UserGetInformationReply(
                status=0, user_name=user_name)


def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_service_pb2_grpc.add_UserServiceServicer_to_server(
            UserService(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig()
    serve()

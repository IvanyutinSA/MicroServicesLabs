from concurrent import futures
import logging

import grpc
from protos import user_service_pb2
from protos import user_service_pb2_grpc


users = []


class UserService(user_service_pb2_grpc.UserService):
    def RegisterRequest(self, request, context):
        pass

    def Authenticate(self, request, context):
        pass

    def UserGetInformation(self, request, context):
        pass


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

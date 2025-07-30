import datetime

from src.middleware.jwt_controller import JWTController

from concurrent import futures
import logging

import grpc
import src.transaction_service.protos.transaction_service_pb2 as transaction_service_pb2
import src.transaction_service.protos.transaction_service_pb2_grpc as transaction_service_pb2_grpc


transactions_db = []


class TransactionServiceServicer(transaction_service_pb2_grpc.TransactionServiceServicer):
    def __init__(self):
        self.jwt_controller = JWTController()

    def TransactionAdd(self, request, context):
        transaction = request.transaction
        transaction = {'owner_name': transaction.owner_name,
                       'transaction_name': transaction.transaction_name,
                       'amount': transaction.amount,
                       'date': datetime.datetime.fromisoformat(
                           transaction.date)}
        if not self.jwt_controller.get_access(
                'TransactionAdd',
                owner_name=transaction['owner_name']):
            return transaction_service_pb2.TransactionAddReply(status=2)
        transactions_db.append(transaction)
        return transaction_service_pb2.TransactionAddReply(status=0)

    def TransactionGet(self, request, context):
        owner_name = request.owner_name
        start_date = datetime.datetime.fromisoformat(
                request.start_date)
        end_date = datetime.datetime.fromisoformat(
                request.end_date)

        if not self.jwt_controller.get_access(operation='TransactionGet',
                                              owner_name=owner_name):
            return transaction_service_pb2.TransactionGetReply(status=2)

        transactions = [transaction for transaction in transactions_db
                        if (transaction['date'] < end_date and
                            start_date <= transaction['date'])]
        transactions = [transaction_service_pb2.Transaction(
            owner_name=transaction['owner_name'],
            transaction_name=transaction['transaction_name'],
            amount=transaction['amount'],
            date=transaction['date'].isoformat()
            ) for transaction in transactions
            if transaction['owner_name'] == owner_name]
        return transaction_service_pb2.TransactionGetReply(
                status=0, transactions=transactions)


def setup_server():
    port = "50052"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    transaction_service_pb2_grpc.add_TransactionServiceServicer_to_server(
            TransactionServiceServicer(), server)
    server.add_insecure_port("[::]:" + port)
    return server


if __name__ == "__main__":
    logging.basicConfig()
    server = setup_server()
    server.start()
    print("Server going to listening on " + 50052)
    server.wait_for_termination()

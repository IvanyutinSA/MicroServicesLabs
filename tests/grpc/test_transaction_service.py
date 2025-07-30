import grpc

from test_utils.test_suit import TestSuit
from src.transaction_service.server import setup_server
from src.middleware.jwt_controller import JWTController

import src.transaction_service.protos.transaction_service_pb2 as transaction_service_pb2
import src.transaction_service.protos.transaction_service_pb2_grpc as transaction_service_pb2_grpc


class TestTransactionService(TestSuit):
    def __init__(self):
        self.server = setup_server()
        self.jwt_controller = JWTController()

    def test_add_transaction_user(self):
        with grpc.insecure_channel("localhost:50052") as channel:
            stub = transaction_service_pb2_grpc.TransactionServiceStub(channel)
            user_name = 'user_name'
            role = 'user'

            self.jwt_controller.generate(user_name, role)

            owner_name = user_name
            transaction_name = 'test_add_transaction'
            amount = 1500
            date = '1990-01-01'
            transaction = transaction_service_pb2.Transaction(
                    owner_name=owner_name,
                    transaction_name=transaction_name,
                    amount=amount,
                    date=date)

            illigal_transaction = transaction_service_pb2.Transaction(
                    owner_name='fake user',
                    transaction_name=transaction_name,
                    amount=amount,
                    date=date)

            request = transaction_service_pb2.TransactionAddRequest(
                    transaction=transaction)
            reply_permissions_ok = stub.TransactionAdd(request)

            request = transaction_service_pb2.TransactionAddRequest(
                    transaction=illigal_transaction)
            reply_permissions_bad = stub.TransactionAdd(request)

            self.assert_eq(reply_permissions_ok.status, 0)
            self.assert_eq(reply_permissions_bad.status, 2)

    def test_add_transaction_admin(self):
        with grpc.insecure_channel("localhost:50052") as channel:
            stub = transaction_service_pb2_grpc.TransactionServiceStub(channel)
            user_name = 'user_name'
            role = 'admin'

            self.jwt_controller.generate(user_name, role)

            owner_name = user_name
            transaction_name = 'test_add_transaction'
            amount = 1500
            date = '1990-01-01'
            transaction = transaction_service_pb2.Transaction(
                    owner_name=owner_name,
                    transaction_name=transaction_name,
                    amount=amount,
                    date=date)

            illigal_transaction = transaction_service_pb2.Transaction(
                    owner_name='fake user',
                    transaction_name=transaction_name,
                    amount=amount,
                    date=date)

            request = transaction_service_pb2.TransactionAddRequest(
                    transaction=transaction)
            reply_permissions_ok = stub.TransactionAdd(request)

            request = transaction_service_pb2.TransactionAddRequest(
                    transaction=illigal_transaction)
            reply_permissions_still_ok = stub.TransactionAdd(request)

            self.assert_eq(reply_permissions_ok.status, 0)
            self.assert_eq(reply_permissions_still_ok.status, 0)

    def test_get_transaction_user(self):
        with grpc.insecure_channel("localhost:50052") as channel:
            stub = transaction_service_pb2_grpc.TransactionServiceStub(channel)
            transaction_name = 'test_get_transaction'
            amount = 1500
            date = '1990-01-01'
            start_date = '1990-01-01'
            end_date = '1991-01-01'

            user_name = 'user_name'
            owner_name = user_name
            another_owner_name = 'another_owner'
            role = 'user'

            transaction = transaction_service_pb2.Transaction(
                    owner_name=user_name,
                    transaction_name=transaction_name,
                    amount=amount,
                    date=date)

            illigal_transaction = transaction_service_pb2.Transaction(
                    owner_name=another_owner_name,
                    transaction_name=transaction_name,
                    amount=amount,
                    date=date)

            self.jwt_controller.generate(user_name, 'admin')

            request = transaction_service_pb2.TransactionAddRequest(
                    transaction=transaction)
            _ = stub.TransactionAdd(request)

            request = transaction_service_pb2.TransactionAddRequest(
                    transaction=illigal_transaction)
            _ = stub.TransactionAdd(request)

            self.jwt_controller.generate(user_name, role)

            request = transaction_service_pb2.TransactionGetRequest(
                    owner_name=owner_name,
                    start_date=start_date,
                    end_date=end_date)
            reply_permissions_ok = stub.TransactionGet(request)

            request = transaction_service_pb2.TransactionGetRequest(
                    owner_name=another_owner_name,
                    start_date=start_date,
                    end_date=end_date)
            reply_permissions_bad = stub.TransactionGet(request)

            self.assert_true(
                    transaction_name in [
                        transaction.transaction_name
                        for transaction in reply_permissions_ok.transactions])
            self.assert_eq(reply_permissions_ok.status, 0)
            self.assert_eq(reply_permissions_bad.status, 2)

    def test_get_transaction_admin(self):
        with grpc.insecure_channel("localhost:50052") as channel:
            stub = transaction_service_pb2_grpc.TransactionServiceStub(channel)
            transaction_name = 'test_get_transaction'
            amount = 1500
            date = '1990-01-01'
            start_date = '1990-01-01'
            end_date = '1991-01-01'

            user_name = 'user_name'
            owner_name = user_name
            another_owner_name = 'another_owner'
            role = 'admin'

            transaction = transaction_service_pb2.Transaction(
                    owner_name=user_name,
                    transaction_name=transaction_name,
                    amount=amount,
                    date=date)

            illigal_transaction = transaction_service_pb2.Transaction(
                    owner_name=another_owner_name,
                    transaction_name=transaction_name,
                    amount=amount,
                    date=date)

            self.jwt_controller.generate(user_name, 'admin')

            request = transaction_service_pb2.TransactionAddRequest(
                    transaction=transaction)
            _ = stub.TransactionAdd(request)

            request = transaction_service_pb2.TransactionAddRequest(
                    transaction=illigal_transaction)
            _ = stub.TransactionAdd(request)

            self.jwt_controller.generate(user_name, role)

            request = transaction_service_pb2.TransactionGetRequest(
                    owner_name=owner_name,
                    start_date=start_date,
                    end_date=end_date)
            reply_permissions_ok = stub.TransactionGet(request)

            request = transaction_service_pb2.TransactionGetRequest(
                    owner_name=another_owner_name,
                    start_date=start_date,
                    end_date=end_date)
            reply_permissions_still_ok = stub.TransactionGet(request)

            self.assert_true(
                    transaction_name in [
                        transaction.transaction_name
                        for transaction in reply_permissions_ok.transactions])
            self.assert_eq(reply_permissions_ok.status, 0)
            self.assert_eq(reply_permissions_still_ok.status, 0)

    def test_get_transaction_bad_interval(self):
        with grpc.insecure_channel("localhost:50052") as channel:
            stub = transaction_service_pb2_grpc.TransactionServiceStub(channel)
            user_name = 'user_name'
            owner_name = user_name
            role = 'user'
            start_date = '3001-01-01'
            end_date = '3000-01-01'

            self.jwt_controller.generate(user_name, role)

            request = transaction_service_pb2.TransactionGetRequest(
                    owner_name=owner_name,
                    start_date=start_date,
                    end_date=end_date)
            reply = stub.TransactionGet(request)

            self.assert_eq(reply.status, 0)
            self.assert_eq(reply.transactions, [])

    def __enter__(self):
        self.server.start()
        return self

    def __exit__(self, *args, **kargs):
        self.server.stop(0)
        pass

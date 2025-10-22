import grpc
from pathlib import Path

import src.transaction_service.protos.transaction_service_pb2 as transaction_service_pb2
import src.transaction_service.protos.transaction_service_pb2_grpc as transaction_service_pb2_grpc

from src.utilities.folk_certificate_controller import FolkCertificateController


class TransactionServiceApi:
    def __init__(self):
        controller = FolkCertificateController()
        self.credentials = grpc.ssl_channel_credentials(
                **controller.get_channel_credentials('transaction-service'))

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

    def transaction_add(self, owner_name, transaction_name, amount, date):
        with grpc.secure_channel('localhost:50052',
                                 self.credentials) as channel:
            stub = transaction_service_pb2_grpc.TransactionServiceStub(channel)
            amount = int(amount)
            transaction = transaction_service_pb2.Transaction(
                    owner_name=owner_name,
                    transaction_name=transaction_name,
                    amount=amount,
                    date=date)
            request = transaction_service_pb2.TransactionAddRequest(
                    transaction=transaction)
            reply = stub.TransactionAdd(request)
            if reply.status:
                self._status_error(reply.status)
            return 'Success'
        self._connection_error()

    def transaction_get(self, owner_name, start_date, end_date):
        with grpc.secure_channel('localhost:50052',
                                 self.credentials) as channel:
            stub = transaction_service_pb2_grpc.TransactionServiceStub(channel)
            request = transaction_service_pb2.TransactionGetRequest(
                    owner_name=owner_name,
                    start_date=start_date,
                    end_date=end_date)
            reply = stub.TransactionGet(request)

            if reply.status:
                self._status_error(reply.status)
            return reply.transactions
        self._connection_error()

import grpc
from pathlib import Path

import src.report_service.protos.report_service_pb2 as report_service_pb2
import src.report_service.protos.report_service_pb2_grpc as report_service_pb2_grpc
import src.transaction_service.protos.transaction_service_pb2 as transaction_service_pb2
import src.transaction_service.protos.transaction_service_pb2_grpc as transaction_service_pb2_grpc

class ReportServiceApi:
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

    def report_generate(self, owner_name, month, year):
        with (grpc.secure_channel('localhost:50052',
                                  self.credentials) as transaction_channel,
              grpc.secure_channel('localhost:50053',
                                  self.credentials) as report_channel
              ):
            rs_stub = report_service_pb2_grpc.ReportServiceStub(
                    report_channel)
            ts_stub = transaction_service_pb2_grpc.TransactionServiceStub(
                    transaction_channel)
            start_date, end_date = self._get_start_date_end_date(month, year)
            request = transaction_service_pb2.TransactionGetRequest(
                    owner_name=owner_name,
                    start_date=start_date,
                    end_date=end_date)
            reply = ts_stub.TransactionGet(request)
            if reply.status:
                self._status_error(reply.status)
            r_transactions = [
                    report_service_pb2.RTransaction(
                        owner_name=transaction.owner_name,
                        transaction_name=transaction.transaction_name,
                        amount=transaction.amount,
                        date=transaction.date)
                    for transaction in reply.transactions]
            request = report_service_pb2.ReportGenerateRequest(
                    transactions=r_transactions)
            reply = rs_stub.ReportGenerate(request)
            if reply.status:
                self._status_error(reply.status)
            report = reply.report
            request = report_service_pb2.ReportExportRequest(report=report)
            reply = rs_stub.ReportExport(request)
            if reply.status:
                self._status_error(reply.status)
            report_path = reply.report_name
            return f'Report was generated and exported with path: {report_path}'
        self._connection_error()

    def _get_start_date_end_date(self, month, year):
        int_month, int_year = map(int, [month, year])
        month = '{:02d}'.format(int_month)
        start_date = f'{year}-{month}-01'
        if month == '12':
            end_date = f'{int_year+1}-01-01'
        else:
            end_date = f'{year}-{'{:02d}'.format(int_month+1)}-01'
        return start_date, end_date

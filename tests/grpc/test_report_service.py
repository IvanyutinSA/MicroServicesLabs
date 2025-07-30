import json
import grpc

from test_utils.test_suit import TestSuit
from src.report_service.server import setup_server
from src.middleware.jwt_controller import JWTController

import src.report_service.protos.report_service_pb2 as report_service_pb2
import src.report_service.protos.report_service_pb2_grpc as report_service_pb2_grpc


class TestReportService(TestSuit):
    def __init__(self):
        self.server = setup_server()
        self.jwt_controller = JWTController()

    def test_generate_report(self):
        with grpc.insecure_channel("localhost:50053") as channel:
            stub = report_service_pb2_grpc.ReportServiceStub(channel)
            transactions = [
                    {'owner_name': 'owner_name',
                     'transaction_name': 'x', 'amount': 10.,
                     'date': '1990-01-01'},
                    {'owner_name': 'owner_name',
                     'transaction_name': 'y', 'amount': 20.,
                     'date': '1990-01-02'},
                    {'owner_name': 'owner_name',
                     'transaction_name': 'z', 'amount': 50.,
                     'date': '1990-01-30'}]
            total_income = sum([transaction['amount']
                                for transaction in transactions])
            total_operations = len(transactions)

            self.jwt_controller.generate('user_name', 'user')

            request = report_service_pb2.ReportGenerateRequest(
                    transactions=[
                        report_service_pb2.RTransaction(
                            transaction_name=transaction['transaction_name'],
                            amount=transaction['amount'],
                            date=transaction['date'])
                        for transaction in transactions])
            reply = stub.ReportGenerate(request)

            self.assert_eq(reply.status, 0)
            self.assert_eq(reply.report.total_income, total_income)
            self.assert_eq(reply.report.total_operations, total_operations)
            self.assert_eq(reply.report.transactions, request.transactions)

    def test_export_report(self):
        with grpc.insecure_channel("localhost:50053") as channel:
            stub = report_service_pb2_grpc.ReportServiceStub(channel)
            transactions = [
                    {'owner_name': 'owner_name',
                     'transaction_name': 'x', 'amount': 10.,
                     'date': '1990-01-01'},
                    {'owner_name': 'owner_name',
                     'transaction_name': 'y', 'amount': 20.,
                     'date': '1990-01-02'},
                    {'owner_name': 'owner_name',
                     'transaction_name': 'z', 'amount': 50.,
                     'date': '1990-01-30'}]

            total_income = sum([transaction['amount']
                                for transaction in transactions])
            total_operations = len(transactions)

            pre_json_report = {
                    'transactions': transactions,
                    'total_income': total_income,
                    'total_operations': total_operations}
            report = report_service_pb2.Report(
                    transactions=[
                        report_service_pb2.RTransaction(
                            owner_name=transaction['owner_name'],
                            transaction_name=transaction['transaction_name'],
                            amount=transaction['amount'],
                            date=transaction['date'])
                        for transaction in transactions],
                    total_income=total_income,
                    total_operations=total_operations)

            self.jwt_controller.generate('user_name', 'user')

            request = report_service_pb2.ReportExportRequest(
                    report=report)
            reply = stub.ReportExport(request)

            self.assert_eq(reply.status, 0)
            with open(f'/tmp/services_reports/{reply.report_name}') as f:
                json_report = f.readline()
                self.assert_eq(json_report, json.dumps(pre_json_report))

    def __enter__(self):
        self.server.start()
        return self

    def __exit__(self, *args, **kargs):
        self.server.stop(0)
        pass

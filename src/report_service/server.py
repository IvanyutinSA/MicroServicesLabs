import os

import time
import json

from src.middleware.jwt_controller import JWTController

from concurrent import futures
import logging

import grpc
import src.report_service.protos.report_service_pb2 as report_service_pb2
import src.report_service.protos.report_service_pb2_grpc as report_service_pb2_grpc


class ReportServiceServicer(report_service_pb2_grpc.ReportServiceServicer):
    def __init__(self):
        self.jwt_controller = JWTController()

    def ReportGenerate(self, request, context):
        if not self.jwt_controller.get_access('ReportGenerate'):
            return report_service_pb2.ReportGenerateReply(status=2)

        transactions = request.transactions
        total_income = sum([transaction.amount
                            for transaction in transactions])
        total_operations = len(transactions)
        report = report_service_pb2.Report(
                transactions=transactions,
                total_income=total_income,
                total_operations=total_operations)
        return report_service_pb2.ReportGenerateReply(
                status=0,
                report=report)

    def ReportExport(self, request, context):
        if not self.jwt_controller.get_access('ReportExport'):
            return report_service_pb2.ReportExportReply(status=0)

        report = request.report
        report_name = f'report_{time.time()}'.replace('.', '')
        transactions = [
                {'owner_name': transaction.owner_name,
                 'transaction_name': transaction.transaction_name,
                 'amount': transaction.amount,
                 'date': transaction.date}
                for transaction in report.transactions]
        pre_json_report = {'transactions': transactions,
                           'total_income': report.total_income,
                           'total_operations': report.total_operations}
        json_report = json.dumps(pre_json_report)

        os.makedirs('/tmp/services_reports', exist_ok=True)
        with open(f'/tmp/services_reports/{report_name}', 'w') as f:
            f.write(json_report)
        return report_service_pb2.ReportExportReply(
                status=0,
                report_name=report_name)


def setup_server():
    port = "50053"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    report_service_pb2_grpc.add_ReportServiceServicer_to_server(
            ReportServiceServicer(), server)
    server.add_insecure_port("[::]:" + port)
    return server


if __name__ == "__main__":
    logging.basicConfig()
    server = setup_server()
    server.start()
    print("Server going to listening on " + 50051)
    server.wait_for_termination()

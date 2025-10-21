from test_utils.test_suit import TestSuit
from src.utilities.certificate_controller import CertificateController


class TestCertificateGeneration(TestSuit):
    def test_generation(self):
        certificates = ['user-service-cert.pem',
                        'transaction-service-cert.pem',
                        'report-service-cert.pem',
                        'client-cert.pem']
        controller = CertificateController()
        for cert in certificates:
            cmd = f"openssl verify -CAfile ca-bundle.pem {cert}"
            self.assert_eq(controller.run_openssl_command(cmd), 0)

    def test_revoking(self):
        controller = CertificateController()
        service_name = 'user-service'
        service_cert = f'{service_name}-cert.pem'

        controller()
        # print(controller.revoke_certificate(service_cert))

        # self.assert_true(controller._is_certificate_revoked(service_cert))
        self.assert_eq(
                controller.get_certificate_status(service_cert)['status'],
                'revoked')

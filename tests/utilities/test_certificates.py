from test_utils.test_suit import TestSuit
from src.utilities.certificate_controller import CertificateController


class TestCertificateGeneration():
    def test_generation(self):
        certificates = ['user-service-cert.pem',
                        'transaction-service-cert.pem',
                        'report-service-cert.pem',
                        'client-cert.pem']
        controller = CertificateController()
        for cert in certificates:
            cmd = f"openssl verify -CAfile ca-bundle.pem {cert}"
            self.assert_eq(controller.run_openssl_command(cmd), 0)

    def test_renew(self):
        controller = CertificateController()
        service_name = 'user-service'
        service_cert = f'{service_name}-cert.pem'
        target_days_remaining = 699
        days = target_days_remaining+1

        controller()
        old_days_remaining = controller.get_certificate_status(
                service_cert).get('days_remaining', None)
        controller.renew_certificate(service_name, days=days)
        actual_days_remaining = controller.get_certificate_status(
                service_cert).get('days_remaining', None)

        self.assert_true(old_days_remaining < actual_days_remaining)
        self.assert_eq(actual_days_remaining, target_days_remaining)

    def test_revoking(self):
        controller = CertificateController()
        service_name = 'user-service'
        service_cert = f'{service_name}-cert.pem'

        controller()

        self.assert_false(controller._is_certificate_revoked(service_cert))
        print(controller.revoke_certificate(service_cert))
        # self.assert_eq(
        #         controller.get_certificate_status(service_cert)['status'],
        #         'revoked')

from test_utils.test_suit import TestSuit
from src.utilities.folk_certificate_controller import FolkCertificateController


class TestCertificateGeneration(TestSuit):
    def test_(self):
        controller = FolkCertificateController()
        controller.create_all()
        # controller.create_root()
        # controller.create_intermediate_pair()
        # controller.create_server_cert('user-service')
        # controller.create_crl()
        # controller.revoke_cert('user-service')

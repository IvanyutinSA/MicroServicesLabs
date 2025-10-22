from test_utils.test_suit import TestSuit
from src.utilities.folk_certificate_controller import FolkCertificateController


class TestFolkCertificateGeneration(TestSuit):
    def test_(self):
        controller = FolkCertificateController(delete_all=True)
        controller.create_all()

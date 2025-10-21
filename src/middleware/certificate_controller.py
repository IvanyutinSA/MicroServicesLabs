from pathlib import Path
from src.utilities.generate_certificates import CertificateGenerator


class CertificateController:
    def __init__(self):
        self.generator = CertificateGenerator()

    def generate(self):
        self.generator()

    def get_client_credentials(self):
        certs_dir = Path("certs")

        with open(certs_dir / "ca-bundle.pem", 'rb') as f:
            root_certificates = f.read()

        with open(certs_dir / "client-cert.pem", 'rb') as f:
            certificate_chain = f.read()

        with open(certs_dir / "client-key.pem", 'rb') as f:
            private_key = f.read()

        return {'root_certificates': root_certificates,
                'private_key': private_key,
                'certificate_chain': certificate_chain}

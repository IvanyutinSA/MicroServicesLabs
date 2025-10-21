import json
import subprocess
from pathlib import Path
import shutil
import datetime


class CertificateController:
    def __init__(self, base_dir="certs"):
        self.subj = "/C=RU/ST=Moscow/L=Moscow/O=X/CN=X"
        self.subj_serv = "/C=RU/ST=Moscow/L=Moscow/O=X/CN="

        self.base_dir = Path(base_dir)
        self.crl_dir = self.base_dir / "crl"
        self.backup_dir = self.base_dir / "backup"

        self.setup_directories()

        self.revoked_db = self.crl_dir / "revoked_certs.json"
        self.setup_revoked_db()

    def setup_directories(self):
        self.base_dir.mkdir(exist_ok=True)
        self.crl_dir.mkdir(exist_ok=True)
        self.backup_dir.mkdir(exist_ok=True)
        print(f'directory: {self.base_dir.absolute()}')

    def setup_revoked_db(self):
        if not self.revoked_db.exists():
            with open(self.revoked_db, 'w') as f:
                json.dump({"revoked_certificates": {}}, f)

    def run_openssl_command(self, cmd, return_result=False):

        result = subprocess.run(cmd, shell=True, capture_output=True,
                                text=True, cwd=self.base_dir)
        if result.returncode:
            print(cmd)
            print(result.stderr)
        if return_result:
            return result
        return result.returncode

    def generate_root_ca(self):
        cmd = "openssl genrsa -out root-ca-key.pem 4096"
        if self.run_openssl_command(cmd):
            return False
        cmd = ("openssl req -new -x509 -days 3650 -key root-ca-key.pem "
               "-out root-ca-cert.pem "
               f"-subj \"{self.subj} Root CA\"")
        if self.run_openssl_command(cmd):
            return False
        return True

    def generate_intermediate_ca(self):
        cmd = "openssl genrsa -out intermediate-ca-key.pem 4096"
        if self.run_openssl_command(cmd):
            return False
        cmd = ("openssl req -new -key intermediate-ca-key.pem "
               "-out intermediate-ca.csr "
               f"-subj \"{self.subj} Intermediate CA\"")
        if self.run_openssl_command(cmd):
            return False
        cmd = ("openssl x509 -req -in intermediate-ca.csr "
               "-CA root-ca-cert.pem -CAkey root-ca-key.pem -CAcreateserial "
               "-out intermediate-ca-cert.pem -days 1825 -sha256 "
               "-extfile <(printf \"basicConstraints=critical,CA:true\")")
        if self.run_openssl_command(cmd):
            return False
        cmd = ("openssl x509 -req -in intermediate-ca.csr "
               "-CA root-ca-cert.pem -CAkey root-ca-key.pem -CAcreateserial "
               "-out intermediate-ca-cert.pem -days 1825 -sha256 "
               "-extfile <(printf \"basicConstraints=critical,CA:true\")")
        return True

    def generate_service_certificate(self, service_name, dns_names):
        key_name = f"{service_name}-key.pem"
        cmd = f"openssl genrsa -out {key_name} 2048"
        if self.run_openssl_command(cmd):
            return False
        csr_name = f"{service_name}.csr"
        cmd = (f"openssl req -new -key {key_name} "
               f"-out {csr_name} "
               f"-subj {self.subj_serv}{service_name}.internal.net")
        if self.run_openssl_command(cmd):
            return False
        san_string = ",".join([f"DNS:{dns}" for dns in dns_names])

        cert_name = f"{service_name}-cert.pem"
        cmd = (f"openssl x509 -req -in {csr_name} "
               f"-CA intermediate-ca-cert.pem -CAkey intermediate-ca-key.pem "
               "-CAcreateserial "
               f"-out {cert_name} -days 365 -sha256 "
               f"-extfile <(printf \"subjectAltName={san_string}\")")
        if self.run_openssl_command(cmd):
            return False
        chain_name = f"{service_name}-chain.pem"
        with (open(self.base_dir / cert_name, 'r') as cert,
              open(self.base_dir / "intermediate-ca-cert.pem",
                   "r") as intermediate,
              open(self.base_dir / chain_name, "w") as chain):
            chain.write(cert.read())
            chain.write(intermediate.read())
        (self.base_dir / csr_name).unlink(missing_ok=True)
        return True

    def create_bundle(self):
        with (open(self.base_dir / "ca-bundle.pem", "w") as bundle,
              open(self.base_dir / "intermediate-ca-cert.pem",
                   "r") as intermediate,
              open(self.base_dir / "root-ca-cert.pem", "r") as root):
            bundle.write(intermediate.read())
            bundle.write(root.read())
        return True

    def __call__(self):
        services = ['user-service', 'transaction-service',
                    'report-service', 'client']
        dnses = [['localhost', f'{service}.internal.net', f'{service}']
                 for service in services]
        _ = (self.generate_root_ca(),
             self.generate_intermediate_ca(),
             self.create_bundle(),
             (lambda: [self.generate_service_certificate(service_name, dns)
                       for service_name, dns in zip(services, dnses)])())

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

    def revoke_certificate(self, cert_file, reason='unspecified'):
        cert_path = self.base_dir / cert_file
        if not cert_path.exists():
            return False

        serial = self._get_certificate_serial(cert_path)
        if serial is None:
            return False

        if self._add_to_revoked_db(serial, cert_file, reason):
            if self._generate_crl():
                return True

        return False

    def renew_certificate(self, service_name, days=365, dns_names=None):
        if dns_names is None:
            dns_names = [service_name, f'{service_name}.internal.net',
                         'localhost']

        self._backup_service_certificates(service_name)

        success = self.generate_service_certificate(service_name, dns_names)
        if not success:
            self._restore_service_certificates(service_name)

        return success

    def get_certificate_status(self, cert_file):
        # cert_path = self.base_dir / cert_file
        cert_path = Path(cert_file)
        if not cert_path.exists():
            return {'status': 'doesn\'t exists'}

        expiry_date = self._get_certificate_expiry_date(cert_path)
        if not expiry_date:
            return {'status': 'invalid'}

        days_remaining = (expiry_date - datetime.now()).days

        is_revoked = self._is_certificate_revoked(cert_path)

        status = 'valid'
        if days_remaining <= 0:
            status = 'expired'
        if is_revoked:
            status = 'revoked'

        return {'status': status,
                'days_remaining': days_remaining,
                'expiry_date': expiry_date.isoformat()}

    def _backup_service_certificates(self, service_name):
        timestamp = datetime.now()
        backup_path = self.backup_dir / timestamp
        backup_path.mkdir(parents=True, exist_ok=True)

        files_to_backup = [f'{service_name}-key.pem',
                           f'{service_name}-cert.pem',
                           f'{service_name}-chain.pem']

        for file in files_to_backup:
            source = self.base_dir / file
            if source.exists():
                shutil.copy2(source, backup_path / file)

    def _restore_service_certificates(self, service_name):
        backups = sorted(self.backup_dir.glob("*"))
        if not backups:
            return False

        latest_backup = backups[-1]

        files_to_restore = [f'{service_name}-key.pem',
                            f'{service_name}-cert.pem',
                            f'{service_name}-chain.pem']

        for file in files_to_restore:
            source = latest_backup / file
            destination = self.base_dir / file
            if source.exists():
                shutil.copy2(source, destination)

        return True

    def _get_certificate_serial(self, cert_path):
        cert_path = cert_path
        cmd = f'openssl x509 -in {cert_path} -serial -noout'
        result = self.run_openssl_command(cmd, return_result=True)
        print(result)

        if result.returncode:
            return None
        return result.stdout.strip().split('=')[1]

    def _get_certificate_expiry_date(self, cert_path):
        cmd = f'openssl x509 -in {cert_path} -enddate -noout'
        result = self.run_openssl_command(cmd, return_result=True)
        if result.returncode:
            return None
        date_str = result.stdout.split('=')[1].strip()
        return datetime.strptime(date_str, '%b %d %H:%M:%S %Y GMT')

    def _add_to_revoked_db(self, serial, cert_file, reason='undefined'):
        try:
            with open(self.revoked_db, 'r') as f:
                db = json.load(f)

            db['revoked_certificates'][serial] = {
                    'certificate': cert_file,
                    'revocation_date': datetime.now().isoformat(),
                    'reason': reason}

            with open(self.revoked_db, 'w') as f:
                json.dump(db, f)

            return True
        except Exception:
            return False

    def _generate_crl(self):
        try:
            with open(self.revoked_db, 'r') as f:
                db = json.load(f)

            if not db['revoked_certificates']:
                return True

            crl_config = self.crl_dir / 'crl_config.txt'
            with open(crl_config, 'w') as f:
                for serial, info in db['revoked_certificates'].items():
                    rev_date = datetime.fromisoformat(info['revocation_date'])
                    f.write(f'{serial}\t{rev_date.strftime('%y%m%d%H%M%SZ')}'
                            f'\t{info['reason']}\n')
            crl_file = self.crl_dir / 'intermediate-ca.crl'
            cmd = (f'openssl ca -gencrl '
                   f'-keyfile {self.base_dir}/intermediate-ca-key.pem '
                   f'-cert {self.base_dir}/intermediate-ca-cert.pem '
                   f'-out {crl_file} '
                   f'-config <(echo \"[ca]\ndatabase = {crl_config}\")')

            rc = not self.run_openssl_command(cmd)

            crl_config.unlink(missing_ok=True)

            return not rc

        except Exception:
            return False

    def _is_certificate_revoked(self, cert_path):
        crl_file = self.crl_dir / 'intermediate-ca.crl'
        if not crl_file.exists():
            False

        cmd = f'openssl verify -CRLfile {crl_file} -crl_check {cert_path}'
        rc = self.run_openssl_command(cmd)

        return rc


if __name__ == "__main__":
    generator = CertificateController()
    generator()

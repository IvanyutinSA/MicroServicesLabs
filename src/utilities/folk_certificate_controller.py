import shutil
import subprocess
from pathlib import Path


class FolkCertificateController:
    def __init__(
            self,
            base_dir="ca",
            conf_path='/home/sergey/Projects/Services/'
            'src/utilities/openssl.cnf'):
        self.base_dir = Path(base_dir)
        shutil.rmtree(self.base_dir.absolute(), ignore_errors=True)
        dirs = [self.base_dir,
                self.base_dir / 'certs',
                self.base_dir / 'crl',
                self.base_dir / 'newcerts',
                self.base_dir / 'csr',
                self.base_dir / 'private',
                self.base_dir / 'private/.rand']
        files_to_touch = ['index.txt']
        files_to_echo = ['serial', 'crlnumber']

        self.setup_directories(dirs)
        self.setup_files(files_to_touch, files_to_echo)
        self.cp_cnf(conf_path)

    def create_all(self):
        services = ['client', 'user-service',
                    'transaction-service', 'report-service']
        self.create_root()
        self.create_intermediate_pair()
        for service in services:
            self.create_server_cert(service)

    def get_server_credentials(self, server):
        root = self.base_dir / 'certs/ca-bundle.pem'
        key = self.base_dir / f'intermediate/private/{server}.key.pem'
        chain = self.base_dir / f'intermediate/certs/{server}-chain.pem'

        return {'private_key_certificate_chain_pairs':
                [(open(key, 'rb').read(),
                  open(chain, 'rb').read())],
                'root_certificates': open(root, 'rb').read(),
                'require_client_auth': True}

    def get_channel_credentials(self, server):
        root = self.base_dir / 'certs/ca-bundle.pem'
        key = self.base_dir / f'intermediate/private/{server}.key.pem'
        chain = self.base_dir / f'intermediate/certs/{server}-chain.pem'

        return {'root_certificates': open(root, 'rb').read(),
                'private_key': open(key, 'rb').read(),
                'certificate_chain': open(chain, 'rb').read()}

    def __gen_subj(self, C='RU', ST='Moscow', L='Moscow', o='X', CN='.'):
        return f'/C={C}/ST={ST}/L={L}/O={o}/CN={CN}'

    def setup_directories(self, dirs):
        for dir in dirs:
            dir.mkdir(exist_ok=True)

    def setup_files(self, to_touch, to_echo):
        for file in to_touch:
            cmd = f'touch {file}'
            self.run_cmd(cmd)
        for file in to_echo:
            cmd = f'echo \"1000\" > {file}'
            self.run_cmd(cmd)

    def cp_cnf(self, conf_path):
        cmd = f'cp {conf_path} {self.base_dir.absolute()}/openssl.cnf'
        self.config_path = self.base_dir.absolute()/'openssl.cnf'
        self.ic_path = self.base_dir.absolute()/'intermediate/openssl.cnf'
        self.run_cmd(cmd)

    def run_cmd(self, cmd):
        cwd = self.base_dir.absolute()
        result = subprocess.run(cmd, shell=True, capture_output=True,
                                text=True, cwd=cwd)
        if result.returncode:
            print(cmd)
            print(result.stderr)
        return result

    def create_root(self):
        cmd = 'openssl genrsa -out private/ca.key.pem 4096'
        self.run_cmd(cmd)
        cmd = (f'openssl req -config {self.config_path} '
               f'-key private/ca.key.pem '
               f'-new -x509 -days 7300 -sha256 -extensions v3_ca '
               f'-out certs/ca.cert.pem -subj {self.__gen_subj(CN='Root')}')
        self.run_cmd(cmd)

    def create_intermediate_pair(self):
        intermediate_controller = FolkCertificateController(
                base_dir='ca/intermediate', conf_path='/home/sergey/Projects/Services/src/utilities/intermediate_openssl.cnf')
        cmd = ('openssl genrsa '
               '-out intermediate/private/intermediate.key.pem 4096')
        self.run_cmd(cmd)
        cmd = (f'openssl req -config {intermediate_controller.config_path} '
               f'-key intermediate/private/intermediate.key.pem '
               f'-new -out intermediate/csr/intermediate.csr.pem '
               f'-subj {self.__gen_subj(CN='Intermediate')}')
        self.run_cmd(cmd)
        cmd = (f'openssl ca -config {self.config_path} -days 3650 '
               f'-extensions v3_intermediate_ca '
               f'-notext -md sha256 -in intermediate/csr/intermediate.csr.pem '
               f'-out intermediate/certs/intermediate.cert.pem -batch')
        self.run_cmd(cmd)
        cmd = ('cat intermediate/certs/intermediate.cert.pem '
               'certs/ca.cert.pem > '
               'intermediate/certs/ca-chain.cert.pem')
        self.run_cmd(cmd)

    def create_server_cert(self, server):
        cmd = f'openssl genrsa -out intermediate/private/{server}.key.pem 2048'
        self.run_cmd(cmd)
        cmd = (f'openssl req -config {self.ic_path} '
               f'-key intermediate/private/{server}.key.pem '
               f'-new -sha256 -out intermediate/csr/{server}.csr.pem '
               f'-addext \"subjectAltName = DNS:localhost\" '
               f'-subj {self.__gen_subj(CN=server)}')
        self.run_cmd(cmd)
        cmd = (f'openssl ca -config {self.ic_path} -extensions server_cert '
               f'-days 375 -notext -md sha256 '
               f'-in intermediate/csr/{server}.csr.pem '
               f'-out intermediate/certs/{server}.cert.pem '
               f'-batch')
        self.run_cmd(cmd)
        cmd = ('cat intermediate/certs/{server}.cert.pem '
               'intermediate/certs/intermediate.cert.pem > '
               'intermediate/certs/{server}-chain.cert.pem')

    def create_crl(self):
        cmd = (f'openssl ca -config {self.ic_path} -gencrl '
               f'-out intermediate/crl/intermediate.crl.pem')
        self.run_cmd(cmd)

    def revoke_cert(self, service):
        cmd = (f'openssl ca -config {self.ic_path} -revoke '
               f'intermediate/certs/{service}.cert.pem')
        self.run_cmd(cmd)

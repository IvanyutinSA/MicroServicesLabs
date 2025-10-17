import requests
from hashlib import sha256
from base64 import urlsafe_b64encode
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import threading

auth_code = None
auth_event = threading.Event()
device_id = None
server_shutdown_event = threading.Event()


class VKAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code, device_id
        query = urlparse(self.path).query
        params = parse_qs(query)

        if "code" in params:
            auth_code = params["code"][0]
            device_id = params["device_id"][0]
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b'<h1>Auth successful!'
                             b'You can close this page.</h1>')
        else:
            self.send_response(400)
            self.end_headers()
        auth_event.set()


class VKAuth:
    def __init__(self,
                 client_id,
                 client_secret,
                 redirect_uri,
                 vk_api_version=0):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.vk_api_version = vk_api_version

    def generate_url(self):
        code_verifier = "0"*50
        self.code_verifier = code_verifier

        code_challenge = urlsafe_b64encode(
            sha256(code_verifier.encode()).digest()
        ).rstrip(b'=').decode()

        auth_url = (
            f"https://id.vk.com/authorize?"
            f"client_id={self.client_id}&"
            f"redirect_uri={self.redirect_uri}&"
            f"response_type=code&"
            f"code_verifier={code_verifier}&"
            f"code_challenge={code_challenge}&"
            f"code_challenge_method=S256"
        )

        return auth_url

    def auth_procedure(self, timeout=60):
        global auth_code, device_id

        auth_url = self.generate_url()

        webbrowser.open_new(auth_url)
        server = create_http_server()

        auth_event.wait(timeout=timeout)
        auth_event.clear()

        server.shutdown()
        server.server_close()

        token, user_id = self.get_access_token(
                auth_code, device_id, self.code_verifier)
        data = self.get_vk_user_info(token)

        return data

    def get_access_token(self, code, device_id, code_verifier):
        token_url = (
            f"https://id.vk.com/oauth2/auth?"
            f"grant_type=authorization_code&"
            f"code_verifier={code_verifier}&"
            f"client_id={self.client_id}&"
            f"device_id={device_id}&"
            f"redirect_uri={self.redirect_uri}"
        )

        response = requests.post(token_url, json={"code": code})

        data = response.json()
        return data.get("access_token"), data.get("user_id")

    def get_vk_user_info(self, access_token):
        user_info_url = (
            f"https://id.vk.ru/oauth2/user_info?"
            f"client_id={self.client_id}&"
            f"access_token={access_token}"
        )

        response = requests.post(user_info_url, json={
            "access_token": access_token,
            "client_id": self.client_id,
            })
        data = response.json()
        return data


def create_http_server(port=80, timeout=300) -> HTTPServer:
    server_address = ("", port)
    httpd = HTTPServer(server_address, VKAuthHandler)

    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    return httpd

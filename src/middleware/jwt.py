import hmac
import time
import json
import base64
from hashlib import sha256


class JWT:
    def __init__(self, key=None):
        self.key = '69'.encode() if not key else key

    def __b64_encode(self, msg):
        return base64.b64encode(msg.encode()).decode()

    def __b64_decode(self, msg):
        return base64.b64decode(msg.encode()).decode()

    def __is_jwt(self, msg):
        if not isinstance(msg, str):
            return False
        if msg.count('.') != 2:
            return False
        return True

    def generate(self, header={}, payload={}):
        header = self.__b64_encode(json.dumps(header))
        payload = self.__b64_encode(json.dumps(payload))
        signature = self.__b64_encode(
                hmac.new(self.key, msg=f'{header}.{payload}'.encode(),
                         digestmod=sha256).hexdigest())
        return f'{header}.{payload}.{signature}'

    def verify(self, token):
        if not self.__is_jwt(token):
            return False

        header, payload, signature = token.split('.')

        if (self.__b64_decode(signature) !=
            hmac.new(self.key, msg=f'{header}.{payload}'.encode(),
                     digestmod=sha256).hexdigest()):
            return False

        payload = json.loads(self.__b64_decode(payload))
        if payload.get('exp', 0) < time.time():
            return False

        return True

    def extract_all(self, token):
        if not self.__is_jwt(token):
            return {}, {}

        header, payload, _ = map(self.__b64_decode, token.split('.'))
        return json.loads(header), json.loads(payload)


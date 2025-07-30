from src.middleware.jwt import JWT
from test_utils.test_suit import TestSuit


class TestJWT(TestSuit):
    def test_jwt_valid_token(self):
        jwt = JWT('key'.encode())
        header = {'typ': 'jwt', 'alg': 'hs256'}
        payload = {'exp': 10**30, 'role': 'admin'}
        token = jwt.generate(header, payload)

        self.assert_true(jwt.verify(token))

        actual_header, actual_payload = jwt.extract_all(token)

        self.assert_eq(actual_header, header)
        self.assert_eq(actual_payload, payload)

    def test_jwt_expired_token(self):
        jwt = JWT('key'.encode())
        header = {'typ': 'jwt', 'alg': 'hs256'}
        payload = {'exp': 0}
        token = jwt.generate(header, payload)

        self.assert_false(jwt.verify(token))

    def test_jwt_fake_sign(self):
        jwt = JWT('key'.encode())
        header = {'typ': 'jwt', 'alg': 'hs256'}
        payload = {'exp': 10**30}
        token = jwt.generate(header, payload)

        token = token[:token.rfind('.')+1]+jwt._JWT__b64_encode('fakesign')

        self.assert_false(jwt.verify(token))

    def test_jwt_invalid_token(self):
        jwt = JWT('key'.encode())
        token = 'invalid_token'

        self.assert_false(jwt.verify(token))

    def test_jwt_extract_all_valid_token(self):
        jwt = JWT('key'.encode())
        header = {'typ': 'jwt', 'alg': 'hs256'}
        payload = {'exp': 10**30}
        token = jwt.generate(header, payload)

        actual_header, actual_payload = jwt.extract_all(token)

        self.assert_true(actual_header, header)
        self.assert_true(actual_payload, payload)

    def test_jwt_extract_all_invalid_token(self):
        jwt = JWT('key'.encode())
        token = 'invalid token'

        header, payload = jwt.extract_all(token)

        self.assert_eq(header, {})
        self.assert_eq(payload, {})

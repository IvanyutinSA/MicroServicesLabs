from src.middleware.jwt import JWT

import time
import os
import json


class JWTController:
    def __init__(self, **kargs):
        self.jwt = JWT()
        self.load_config(**kargs)

    def load_config(self, *args, **kwargs):
        with open(".config/jwt_controller.config") as f:
            self.config = json.load(f)

    def generate(self, user_name, role, type=None, issuer="UserService"):
        header = {'alg': 'HS256', 'typ': 'JWT'}
        payload = {'user_name': user_name, 'role': role,
                   'exp': time.time()+self.config['exp_delta'],
                   'iss': issuer}
        access_token = self.jwt.generate(header, payload)
        payload['exp'] = time.time()+self.config['refresh_exp_delta']
        refresh_token = self.jwt.generate(header, payload)
        self.save_token(access_token, 'access')
        self.save_token(refresh_token, 'refresh')

    def generate_access_token(self, refresh_token):
        header, payload = self.jwt.extract_all(refresh_token)
        payload['exp'] = time.time()+self.config['exp_delta']
        token = self.jwt.generate(header, payload)
        self.save_token(token, 'access')
        return token

    def save_token(self, token, type):
        os.makedirs('/tmp/services', exist_ok=True)
        with open(f'/tmp/services/{type}_token', 'w') as f:
            f.write(token)

    def issue_access_token(self):
        try:
            with open('/tmp/services/access_token') as f:
                token = f.readline()
                return token
        except Exception:
            return ''

    def issue_refresh_token(self):
        try:
            with open('/tmp/services/refresh_token') as f:
                token = f.readline()
                return token
        except Exception:
            return ''

    def is_expired(self, token):
        _, payload = self.jwt.extract_all(token)
        return payload.get('exp', 0) < time.time()

    def get_access(self, operation,  **meta_data):
        if meta_data.get('is_special', False):
            return self.verify_special(None, operation, **meta_data)
        access_token = self.issue_access_token()
        if not self.is_expired(access_token):
            return self.verify_privilages(access_token, operation, **meta_data)

        refresh_token = self.issue_refresh_token()
        if self.is_expired(refresh_token):
            return False

        access_token = self.generate_access_token(refresh_token=refresh_token)
        self.save_token(access_token, 'access')

        return self.verify_privilages(access_token, operation, **meta_data)

    def verify_special(self, token, operation, **meta_data):
        if operation == 'Register':
            role = meta_data.get('role', '')
            if role == 'user':
                return True
            token = self.issue_access_token()
            _, payload = self.jwt.extract_all(token)
            if not token:
                return False
            return self.__is_equivalent_role('admin', payload.get('role', ''))

        if operation == 'TransactionAdd':
            _, payload = self.jwt.extract_all(token)
            if self.__is_equivalent_role('admin', payload.get('role', '')):
                return True
            owner_name = meta_data.get('owner_name', '')
            return owner_name == payload['user_name']

        if operation == 'TransactionGet':
            _, payload = self.jwt.extract_all(token)
            if self.__is_equivalent_role('admin', payload.get('role', '')):
                return True
            owner_name = meta_data.get('owner_name', '')
            return owner_name == payload['user_name']

        if operation == 'UserGetInformation':
            _, payload = self.jwt.extract_all(token)
            if self.__is_equivalent_role('admin', payload.get('role', '')):
                return True

            user_name = payload.get('user_name', '')
            if user_name != meta_data.get('user_name', ''):
                return False
            return True

    def verify_privilages(self, token, operation, **meta_data):
        _, payload = self.jwt.extract_all(token)
        role = payload.get('role', '')
        if self.config['permissions'][operation] == "special":
            return self.verify_special(token, operation, **meta_data)

        return self.__is_equivalent_role(
                self.config['permissions'][operation], role)

    def __is_equivalent_role(self, target_role, actual_role):
        if (
            target_role not in self.config['roles'] or
            actual_role not in self.config['roles']
        ):
            return False

        return (self.config['roles'][target_role] <=
                self.config['roles'][actual_role])

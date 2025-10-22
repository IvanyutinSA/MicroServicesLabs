from hashlib import sha256
import msgpack
from os import environ

from src.middleware.vk_auth import VKAuth
from dotenv import load_dotenv


class VkAuthService:
    def __init__(self):
        load_dotenv()
        self.key = 'vk'.encode()
        self.VK_CLIENT_ID = environ['VK_CLIENT_ID']
        self.VK_CLIENT_SECRET = environ['VK_CLIENT_SECRET']
        self.VK_REDIRECT_URI = environ['VK_REDIRECT_URI']

    def authorize(self):
        vk_auth = VKAuth(self.VK_CLIENT_ID, self.VK_CLIENT_SECRET,
                         self.VK_REDIRECT_URI)
        data = vk_auth.auth_procedure(60)
        user_id = data.get('user', {}).get('user_id')
        username = self.create_username(user_id)
        password = self.create_password(user_id)
        return msgpack.packb({'username': username,
                              'password': password})

    def create_username(self, user_id):
        return f'vk_user_{user_id}'

    def create_password(self, user_id):
        return sha256(str(user_id).encode('utf-8')).hexdigest()

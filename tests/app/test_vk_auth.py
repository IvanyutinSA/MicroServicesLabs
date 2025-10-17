from os import environ

from src.middleware.vk_auth import VKAuth
from dotenv import load_dotenv

from test_utils.test_suit import TestSuit

load_dotenv()

VK_CLIENT_ID = environ['VK_CLIENT_ID']
VK_CLIENT_SECRET = environ['VK_CLIENT_SECRET']
VK_REDIRECT_URI = environ['VK_REDIRECT_URI']


class TestVkAuth():
    def test_vk_auth(self):

        vk_auth = VKAuth(VK_CLIENT_ID, VK_CLIENT_SECRET, VK_REDIRECT_URI)
        code = vk_auth.auth_procedure(60)

        self.assert_true(code is not None)

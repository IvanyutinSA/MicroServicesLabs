from src.middleware.jwt_controller import JWTController
from src.middleware.jwt import JWT


def get_username_from_token(func):
    def wrapper(self):
        jwt = JWT()
        jwt_controller = JWTController()
        try:
            token = jwt_controller.issue_access_token()
        except Exception:
            token = ' . . '
        _, payload = jwt.extract_all(token)
        return func(self, payload.get('user_name', 'not logged'))
    return wrapper

from src.middleware.jwt_controller import JWTController
from src.middleware.jwt import JWT
from test_utils.test_suit import TestSuit


class TestJWTController(TestSuit):
    def test_token_generation(self):
        jwt_controller = JWTController()
        jwt = JWT()

        jwt_controller.generate('user_name', 'user')

        access_token = jwt_controller.issue_access_token()
        refresh_token = jwt_controller.issue_refresh_token()

        self.assert_true(jwt.verify(access_token))
        self.assert_true(jwt.verify(refresh_token))

    def test_privilage_verification(self):
        jwt_controller = JWTController()
        user_name = 'user_name'
        role = 'user'

        jwt_controller.generate(user_name, role)
        user_token = jwt_controller.issue_access_token()
        jwt_controller.generate(user_name, 'admin')
        admin_token = jwt_controller.issue_access_token()

        self.assert_true(jwt_controller.verify_privilages(user_token,
                                                          'ReportExport'))
        self.assert_false(jwt_controller.verify_privilages(user_token,
                                                           'default'))

        self.assert_false(
                jwt_controller.verify_privilages(user_token,
                                                 'UserGetInformation'))

        self.assert_true(
                jwt_controller.verify_privilages(user_token,
                                                 'UserGetInformation',
                                                 user_name=user_name))

        self.assert_true(
                jwt_controller.verify_privilages(admin_token,
                                                 'UserGetInformation'))

    def test_get_access_valid_access_token(self):
        jwt_controller = JWTController()
        user_name = 'user_name'
        role = 'user'

        jwt_controller.generate(user_name, role)

        self.assert_true(jwt_controller.get_access('ReportExport'))

    def test_get_access_expired_access_token(self):
        jwt_controller = JWTController()
        jwt = JWT()

        user_name = 'user_name'
        role = 'user'

        jwt_controller.generate(user_name, role)
        access_token = jwt_controller.issue_access_token()
        header, payload = jwt.extract_all(access_token)
        payload['exp'] = 0
        access_token = jwt.generate(header, payload)
        jwt_controller.save_token(access_token, 'access')

        self.assert_true(jwt_controller.get_access('ReportExport'))

    def test_get_access_expired_refresh_token(self):
        jwt_controller = JWTController()
        jwt = JWT()

        user_name = 'user_name'
        role = 'user'

        jwt_controller.generate(user_name, role)
        access_token = jwt_controller.issue_access_token()
        header, payload = jwt.extract_all(access_token)
        payload['exp'] = 0
        token = jwt.generate(header, payload)
        jwt_controller.save_token(token, 'access')
        jwt_controller.save_token(token, 'refresh')

        self.assert_false(jwt_controller.get_access('ReportExport'))

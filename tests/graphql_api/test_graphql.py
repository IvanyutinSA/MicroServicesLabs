from time import sleep
import threading

import src.user_service.server as user_server
import src.transaction_service.server as transaction_server

from test_utils.test_suit import TestSuit
from src.graphql_api.schema import build_schema

from src.middleware.jwt_controller import JWTController


class TestGraphQL(TestSuit):
    def __init__(self):
        self.user_server = user_server.setup_server()
        self.transaction_server = transaction_server.setup_server()
        self.jwt_controller = JWTController()

    def test_user_query(self):
        schema = build_schema()
        self.jwt_controller.generate('admin', 'admin')
        user_name = 'fool'
        reply = schema.execute(
            '''
            query ($user_name: String!){
                user(username: $user_name) {
                    username
                    role
                    }
                }
            ''', variables={'user_name': user_name})
        self.assert_eq(reply.errors, None)

    def test_transaction_query(self):
        schema = build_schema()
        self.jwt_controller.generate('admin', 'admin')
        variables = {'owner_name': 'user_name',
                     'start_date': '1990-01-01',
                     'end_date': '1991-01-01'}
        reply = schema.execute(
            '''
            query ($owner_name: String!, $start_date: String!, $end_date: String!){
                transactions(ownerName: $owner_name,
                             startDate: $start_date,
                             endDate: $end_date) {
                                 ownerName
                                 transactionName
                    }
                }
            ''', variables=variables)
        self.assert_eq(reply.errors, None)

    def test_add_transaction(self):
        schema = build_schema()
        self.jwt_controller.generate('admin', 'admin')
        variables = {'transaction': {'ownerName': 'admin',
                                     'transactionName': 'transaction_graphql',
                                     'amount': 700,
                                     'date': '1991-01-01'}}

        reply = schema.execute(
            '''
            mutation ($transaction: TransactionInput!){
                addTransaction(transaction: $transaction) {
                    status
                    }
                }
            ''', variables=variables)
        self.assert_eq(reply.errors, None)

    def test_register(self):
        schema = build_schema()
        self.jwt_controller.generate('test_register_graphql', 'user')
        variables = {'username': 'test_register_graphql',
                     'password': 'password',
                     'role': 'user'}

        reply = schema.execute(
            '''
            mutation ($username: String!, $password: String!, $role: String!){
                register(username: $username, password: $password, role: $role) {
                    status
                    }
                }
            ''', variables=variables)
        self.assert_eq(reply.errors, None)

    async def tst_subscription(self):
        schema = build_schema()
        subscription = "subscription { transactionAdded }"
        result = await schema.subscribe(subscription)
        thread = threading.Thread(target=self.sub)
        thread.start()
        was_logged = 0
        async for item in result:
            was_logged = 1
        thread.join()
        self.assert_true(was_logged)

    def sub(self):
        sleep(1)
        self.test_add_transaction()
        sleep(1)

    def __enter__(self):
        self.user_server.start()
        self.transaction_server.start()
        return self

    def __exit__(self, *args, **kargs):
        self.user_server.stop(0)
        self.transaction_server.stop(0)

import asyncio
import aiohttp
from src.graphql_api.server import GraphQLServer
from test_utils.test_suit import TestSuit

import src.user_service.server as user_server
import src.transaction_service.server as transaction_server
from src.middleware.jwt_controller import JWTController


class TestQraphqlServer(TestSuit):
    def __init__(self):
        self.user_server = user_server.setup_server()
        self.transaction_server = transaction_server.setup_server()
        self.jwt_controller = JWTController()

    async def test_server(self):
        server = GraphQLServer()
        await server.start_server()
        async with aiohttp.ClientSession() as session:

            self.jwt_controller.generate('admin', 'admin')
            query = {'query': '{user(username: \"fool\") {username}}'}

            async with session.post("http://localhost:8000/graphql",
                                    json=query) as response:
                pass
                self.assert_eq(response.status, 200)

        await server.stop_server()

    async def tst_run_server(self):
        self.jwt_controller.generate('admin', 'admin')
        server = GraphQLServer()
        await server.start_server()
        await asyncio.sleep(600)

    def __enter__(self):
        self.user_server.start()
        self.transaction_server.start()
        return self

    def __exit__(self, *args, **kargs):
        self.user_server.stop(0)
        self.transaction_server.stop(0)

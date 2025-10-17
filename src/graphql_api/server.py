import json

from graphql import format_error
from graphql_ws.aiohttp import AiohttpSubscriptionServer


from aiohttp import web
from .schema import build_schema

from .template import render_graphiql


class GraphQLServer:
    def __init__(self, port=8000):

        app = web.Application()
        app.router.add_get("/subscriptions", self.subscriptions)
        app.router.add_get("/graphiql", self.graphiql_view)
        app.router.add_get("/graphql", self.graphql_view)
        app.router.add_post("/graphql", self.graphql_view)

        self.schema = build_schema()
        self.port = port
        self.app = app
        self.subscription_server = AiohttpSubscriptionServer(self.schema)

    # doesn't work
    # change for own implementation
    async def subscriptions(self, request):
        ws = web.WebSocketResponse(protocols=("graphql-ws"))
        await ws.prepare(request)

        await self.subscription_server.handle(ws)
        return ws

    async def graphql_view(self, request):
        payload = await request.json()
        response = await self.schema.execute(payload.get("query", ""),
                                             return_promise=True)
        data = {}
        if response.errors:
            data["errors"] = [format_error(e) for e in response.errors]
        if response.data:
            data["data"] = response.data
        jsondata = json.dumps(data,)
        return web.Response(text=jsondata,
                            headers={"Content-Type": "application/json"})

    async def graphiql_view(self, request):
        return web.Response(text=render_graphiql(),
                            headers={"Content-Type": "text/html"})

    async def start_server(self):
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        self.site = web.TCPSite(self.runner, 'localhost', self.port)
        await self.site.start()

    async def stop_server(self):
        if self.site:
            await self.site.stop()
        if self.runner:
            await self.runner.cleanup()

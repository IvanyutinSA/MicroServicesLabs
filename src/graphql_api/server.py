import json
import asyncio

from graphql import format_error
# from graphql_ws.aiohttp import AiohttpSubscriptionServer

from aiohttp import web, WSMsgType
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
        # self.subscription_server = AiohttpSubscriptionServer(self.schema)
        self.active_subscriptions = {}

    # async def subscriptions(self, request):
    #     ws = web.WebSocketResponse(protocols=("graphql-ws"))
    #     await ws.prepare(request)
    #
    #     await self.subscription_server.handle(ws)
    #     return ws
    async def subscriptions(self, request):
        ws = web.WebSocketResponse(protocols=('graphql-ws',
                                              'graphql-transport-ws'))
        await ws.prepare(request)

        try:
            async for msg in ws:
                if msg.type == WSMsgType.TEXT:
                    await self._handle_ws_message(ws, msg.data)
        except Exception as e:
            print(f"WebSocket error: {e}")
        finally:
            for sub_id in list(self.active_subscriptions.keys()):
                await self._stop_subscription_ws(sub_id)

        return ws

    async def _handle_ws_message(self, ws, message):
        print(f"🔔 WebSocket message: {message}")  # ДОБАВЬ ЭТУ СТРОКУ

        try:
            data = json.loads(message)
            message_type = data.get('type')

            if message_type == 'connection_init':
                print("connection init received")
                await ws.send_str(json.dumps({'type': 'connection_ack'}))

            if message_type == 'start':
                print("subscription start received")
                await self._start_subscription_ws(ws, data)

            if message_type == 'stop':
                print("subscription stop received")
                await self._stop_subscription_ws(data.get('id'))

            if message_type == 'connection_terminate':
                await ws.close()
        except Exception as e:
            print(f"websocket error: {e}")
            await ws.send_str(json.dumps({
                'type': 'error',
                'payload': {'message': str(e)}
                }))

    async def _start_subscription_ws(self, ws, data):
        subscription_id = data.get('id')
        payload = data.get('payload', {})
        query = payload.get('query')
        variables = payload.get('variables', {})
        operation_name = payload.get('operationName')

        if not subscription_id or not query:
            return

        if subscription_id in self.active_subscriptions:
            self.active_subscriptions[subscription_id].cancel()

        task = asyncio.create_task(
                self._execute_subscription_ws(ws,
                                              subscription_id,
                                              query,
                                              variables,
                                              operation_name))
        self.active_subscriptions[subscription_id] = task

    async def _execute_subscription_ws(self, ws, subscription_id, query,
                                       variables, operation_name):
        try:
            result = await self.schema.subscribe(query,
                                                 variable_values=variables,
                                                 operation_name=operation_name)
            if hasattr(result, '__aiter__'):
                async for item in result:
                    print(result)
                    if ws.closed:
                        break

                    await ws.send_str(json.dumps({
                        'type': 'data',
                        'id': subscription_id,
                        'payload': {
                            'data': item.data,
                            'errors': [self._format_error(error)
                                       for error in item.errors] if item.errors else None
                            }}))
        except asyncio.CancelledError:
            print("Subscription cancelled")
        except Exception as e:
            print(f"Subscription error: {e}")
            if not ws.closed:
                await ws.send_str(json.dumps({
                    'type': 'error',
                    'id': subscription_id,
                    'payload': {'errors': [str(e)]}}))

    def _format_error(self, error):
        return {'message': str(error),
                'locations': getattr(error, 'locations', None),
                'path': getattr(error, 'path', None)}

    async def graphql_view(self, request):
        payload = await request.json()
        response = await self.schema.execute_async(
                payload.get("query", ""),
                variable_values=payload.get("variables"),
                operation_name=payload.get("operationName"))
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
        for sub_id in list(self.active_subscriptions.keys()):
            await self._start_subscription_ws(sub_id)
        if self.site:
            await self.site.stop()
        if self.runner:
            await self.runner.cleanup()

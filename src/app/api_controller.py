import inspect

from contextlib import contextmanager
from src.app.documentation_api import DocumentationApi
from src.app.user_service_api import UserServiceApi
from src.app.transaction_service_api import TransactionServiceApi
from src.app.report_service_api import ReportServiceApi

from src.user_service.server import setup_server as user_server
from src.transaction_service.server import setup_server as transaction_server
from src.report_service.server import setup_server as report_server


class ApiController:
    def __init__(self):
        self.api_list = [DocumentationApi(), UserServiceApi(),
                         TransactionServiceApi(), ReportServiceApi()]
        self.cmd2func = self.build_cmd2func()
        self.api_list[0]._generate_documentation(self.api_list)

    def execute(self, *args, **kargs):
        result = {'output': '',
                  'error': ''}
        try:
            operation_name = kargs.get('operation_name', '')
            output = self.cmd2func.get(
                    operation_name, self.exception_thrower)(*args, **kargs)
            result['output'] = output
        except Exception as e:
            result['error'] = self.error_handler(e)
        return result

    def exception_thrower(*args, **kargs):
        msg = ''
        op_name = kargs.get('operation_name', '')
        if op_name:
            msg = f'Operation {op_name} is not supported'
        raise Exception(msg)

    def error_handler(self, e):
        return str(e)

    def build_cmd2func(self):
        cmd2func = {}
        for api in self.api_list:
            for method in api.__class__.__dict__:
                method = getattr(api.__class__, method)
                if callable(method) and method.__name__[:1] != '_':
                    cmd2func[method.__name__.replace('_', '-')] = \
                            self.create_wrapper(method, api)
        return cmd2func

    def create_wrapper(self, method, api):
        sig = inspect.signature(method)
        method_args = list(sig.parameters.keys())

        def wrapper(*args, **kwargs):
            kwargs = {key: value for key, value in kwargs.items()
                      if key in method_args}
            return method(api, *args, **kwargs)

        return wrapper

    def log(self, info):
        print(f'ApiController: {info}')


class ServerController:
    def __init__(self):
        self.servers = {'user-server': user_server(secure=True),
                        'transaction-server': transaction_server(secure=True),
                        'report-server': report_server(secure=True)}

    def start_server(self, server_name):
        if server_name not in self.servers:
            return
        self.servers[server_name].start()

    def start_all(self):
        for server in self.servers.keys():
            self.start_server(server)

    def stop_all(self):
        for server in self.servers.keys():
            self.stop_server(server)

    def stop_server(self, server_name):
        if server_name not in self.servers:
            return
        self.servers[server_name].stop(0)

    def __enter__(self):
        self.start_all()
        return self

    def __exit__(self, *args):
        self.stop_all()

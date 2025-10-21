import re
from src.app.api_controller import ApiController
from src.app.extra import get_username_from_token


class CliController:
    def __init__(self):
        self.username = 'ordinary'
        self.api = ApiController()
        self.meta = {}
        self.result = {}

    def parse_line(self, line):
        line = line.strip()
        line = re.sub(r"\\s+", r"\\s", line)
        mixed_args = line.split()
        if not mixed_args:
            return [], {}
        args = []
        kargs = {'current_user': self.username,
                 'operation_name': mixed_args.pop(0)}
        i = 0
        while i < len(mixed_args):
            item = mixed_args[i].replace('\"', '')
            if '--' == item[:2]:
                kargs[item[2:]] = mixed_args[i+1]
                i += 1
            else:
                args.append(item)
            i += 1
        return args, kargs

    @get_username_from_token
    def build_line(self, username):
        self.username = username
        lines = ''
        if self.result.get('output', ''):
            lines += f'Result: {self.result['output']}\n'
        if self.result.get('error', ''):
            lines += f'Error: {self.result['error']}\n'
        lines += f'[{self.username}] '
        return lines

    def execute(self, *args, **kargs):
        self.result = self.api.execute(*args, **kargs)

    def __call__(self, line):
        args, kargs = self.parse_line(line)
        self.execute(*args, **kargs)
        return self.build_line()

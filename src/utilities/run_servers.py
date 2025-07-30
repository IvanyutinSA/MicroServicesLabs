from os import fork
import src.user_service.server as us


def run_servers():
    pid = fork()
    if not pid:
        us.serve()

if __name__ == '__main__':
    run_servers()

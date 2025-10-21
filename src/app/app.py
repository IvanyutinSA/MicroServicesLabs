from src.app.cli_controller import CliController
from src.app.api_controller import ServerController


def main():
    with ServerController() as _:
        controller = CliController()
        print(controller.build_line(), end='')
        line = input()
        while True:
            line = input(controller(line))


if __name__ == "__main__":
    main()

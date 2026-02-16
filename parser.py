import sys


class ParserError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

    def __str__(self) -> str:
        return f"ParserError: {self.args[0]}"


class Parser:
    @staticmethod
    def get_options() -> dict:
        options: dict[str, str | bool] = {}
        for arg in range(len(sys.argv)):
            if arg == 0:
                continue
            elif sys.argv[arg] == "--visual" and options.get("vis") is None:
                options["vis"] = True
            elif options.get("map") is None:
                options["map"] = sys.argv[arg]
            else:
                raise ParserError(f"Invalid option: {sys.argv[arg]}")
        return options

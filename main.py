from parser import Parser, ParserError

class Main:
    @staticmethod
    def main() -> None:
        try:
            options = Parser.get_options()
            if options.get("map") is None:
                raise ParserError("No map file found!")
            with open(str(options.get("map"))) as file:
                pass
            print(Parser.get_options())
        except Exception as e:
            print(e)

if __name__ == "__main__":
    Main.main()
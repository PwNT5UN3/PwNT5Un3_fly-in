from parser import Parser, ParserError

class Main:
    @staticmethod
    def main() -> None:
        try:
            options = Parser.get_options()
            if options.get("map") is None:
                raise ParserError("No map file found!")
            map_parts = Parser.parse_map_file(str(options.get("map")))
            print(map_parts)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    Main.main()
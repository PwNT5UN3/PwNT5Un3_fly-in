from parser import Parser, ParserError
from graph import Graph


class Main:
    @staticmethod
    def main() -> None:
        try:
            options = Parser.get_options()
            if options.get("map") is None:
                raise ParserError("No map file found!")
            map_parts = Parser.parse_map_file(str(options.get("map")))
            network = Graph()
            if len(map_parts["start"]) == 0 or len(map_parts["end"]) == 0:
                raise ValueError("Both start and end must be defined")
            print(map_parts)
            for node in map_parts["nodes"]:
                network.add_zone(node)
            for link in map_parts["links"]:
                network.add_connection(link)
            network.set_start(map_parts["start"][0])
            network.set_end(map_parts["end"][0])
            if network.start_node is None or network.end_node is None:
                raise ValueError("Both start and end must be defined")
            print(network.start_node.name)
            print(network.end_node.name)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    Main.main()

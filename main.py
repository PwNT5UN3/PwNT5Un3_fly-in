from parser import Parser, ParserError
from graph import Graph, Drone
from pathfind import Pathfinder
from visualizer import Visualizer


class Main:
    """The main wrapper for the program"""

    @staticmethod
    def finished(drones: list[Drone]) -> bool:
        """A check if all drones have reached the goal"""
        for drone in drones:
            if not drone.found_target:
                return False
        return True

    @staticmethod
    def main() -> None:
        """the main function running parser, pathfinder and visualiser"""
        try:
            options = Parser.get_options()
            if options.get("map") is None:
                raise ParserError("No map file found!")
            map_parts = Parser.parse_map_file(str(options.get("map")))
            network = Graph()
            if len(map_parts["start"]) == 0 or len(map_parts["end"]) == 0:
                raise ValueError("Both start and end must be defined")
            for node in map_parts["nodes"]:
                network.add_zone(node)
            for link in map_parts["links"]:
                network.add_connection(link)
            network.set_start(map_parts["start"][0])
            network.set_end(map_parts["end"][0])
            if network.start_node is None or network.end_node is None:
                raise ValueError("Both start and end must be defined")
            num = map_parts.get("drone_num")
            if num is None:
                raise ValueError("number of drones must be specified!")
            scout = Drone(
                "D_SCOUT",
                network.start_node.name,
                [network.start_node.name],
            )
            Pathfinder.get_best_next_tile(scout, network)
            drones = []
            for i in range(list(num)[0]):
                drones.append(
                    Drone(
                        "D" + str(i + 1),
                        network.start_node.name,
                        [network.start_node.name],
                    )
                )
            network.start_node.current_drone_count = list(num)[0]
            while not Main.finished(drones):
                for drone in drones:
                    Pathfinder.move_to_next_tile(drone, network)
                network.reset_links()
            Visualizer.print_movement_logs(
                drones, network, bool(options.get("vis", False))
            )
            if options.get("vis", False):
                gui = Visualizer()
                gui.run_gui(drones, network)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    Main.main()

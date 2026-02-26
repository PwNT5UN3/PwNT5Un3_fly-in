import sys
from graph import Zone, ZoneType, Connection
from typing import Any


class ParserError(Exception):
    """Parser exception class"""

    def __init__(self, message: str) -> None:
        """constructor"""
        super().__init__(message)

    def __str__(self) -> str:
        """exception message"""
        return f"ParserError: {self.args[0]}"


class Parser:
    """the class for the parser"""

    @staticmethod
    def get_options() -> dict[str, str | bool]:
        """gets all passed options"""
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

    @staticmethod
    def parse_link(line: str) -> Connection:
        """parses a line for a connection"""
        data = line.split("[")
        hard_data = data[0].split(" ")
        if len(hard_data) != 3 and len(hard_data) != 2:
            raise ParserError(f"{line} is not a valid link declaration!1")
        linked_hubs = hard_data[1].split("-", maxsplit=1)
        if len(linked_hubs) != 2:
            raise ParserError(f"{line} is not a valid link declaration!")
        if len(data) >= 2:
            metadata = data[1].split("]")[0].split(" ")
        else:
            metadata = []
        cap = ""
        for data_point in metadata:
            params = data_point.split("=")
            if len(params) == 1:
                raise ParserError(f"{data_point} is not valid metadata!")
            elif params[1] == "":
                raise ParserError(f"{data_point} is not valid metadata!")
            elif params[0] == "max_link_capacity" and cap == "":
                cap = params[1]
            elif params[0] == "max_link_capacity":
                raise ParserError("Do not redefine datapoints!")
            else:
                raise ParserError(f"{params[0]} is not a valid metadata point")
        if cap == "":
            cap_int = 1
        else:
            cap_int = int(cap)
            if cap_int <= 0:
                raise ParserError("capacity cannot be less than one")
        return Connection(
            hard_data[1], linked_hubs[0], linked_hubs[1], cap_int
        )

    @staticmethod
    def parse_zone(line: str, drone_num: int) -> Zone:
        """parses a line for a zone"""
        data = line.split("[")
        hard_data = data[0].split(" ")
        if len(hard_data) != 5 and len(hard_data) != 4:
            raise ParserError(f"{line} is not a valid hub declaration!")
        name = hard_data[1]
        x = int(hard_data[2])
        y = int(hard_data[3])
        if len(data) >= 2:
            metadata = data[1].split("]")[0].split(" ")
        else:
            metadata = []
        color = ""
        zone = ""
        cap = ""
        for data_point in metadata:
            params = data_point.split("=")
            if len(params) == 1:
                raise ParserError(f"{data_point} is not valid metadata!")
            elif params[1] == "":
                raise ParserError(f"{data_point} is not valid metadata!")
            elif params[0] == "color" and color == "":
                color = params[1]
            elif params[0] == "color":
                raise ParserError("Do not redefine datapoints!")
            elif params[0] == "zone" and zone == "":
                zone = params[1]
            elif params[0] == "zone":
                raise ParserError("Do not redefine datapoints!")
            elif params[0] == "max_drones" and cap == "":
                cap = params[1]
            elif params[0] == "max_drones":
                raise ParserError("Do not redefine datapoints!")
            else:
                raise ParserError(f"{params[0]} is not a valid metadata point")
        if zone == "" or zone == "normal":
            zonetype = ZoneType.NORMAL
        elif zone == "restricted":
            zonetype = ZoneType.RESTRICTED
        elif zone == "priority":
            zonetype = ZoneType.PRIO
        elif zone == "blocked":
            zonetype = ZoneType.BLOCKED
        else:
            raise ParserError(f"{zone} is not a valid zone type!")
        if cap == "":
            if hard_data[0] == "start_hub:" or hard_data[0] == "end_hub:":
                cap_int = drone_num
            else:
                cap_int = 1
        else:
            cap_int = int(cap)
            if cap_int <= 0:
                raise ParserError("capacity cannot be less than one")
            if hard_data[0] == "start_hub:" or hard_data[0] == "end_hub:":
                if cap_int != drone_num:
                    raise ParserError(
                        "capacity on the start end end must be equal"
                        + " to the total drone number"
                    )
        return Zone(name, x, y, zonetype, color, cap_int)

    @staticmethod
    def parse_map_file(map_file: str) -> dict[str, list[Any]]:
        """parses the map file using parse_link and parse_zone"""
        drone_map: dict[str, list[Any]] = {}
        drone_map["nodes"] = []
        drone_map["links"] = []
        drone_map["start"] = []
        drone_map["end"] = []
        with open(map_file) as file:
            for line in file:
                if line.startswith("#") or line.strip() == "":
                    continue
                elif (
                    line.startswith("nb_drones:")
                    and len(drone_map["nodes"]) == 0
                    and len(drone_map["links"]) == 0
                    and drone_map.get("drone_num") is None
                ):
                    drone_map["drone_num"] = [int(line.strip().split(" ")[1])]
                elif (
                    line.startswith("start_hub:")
                    and drone_map.get("start") == []
                    and len(drone_map["drone_num"]) == 1
                ):
                    zone = Parser.parse_zone(
                        line.strip(), drone_map["drone_num"][0]
                    )
                    drone_map["start"] = [zone]
                    drone_map["nodes"].append(zone)
                elif (
                    line.startswith("end_hub:")
                    and drone_map.get("end") == []
                    and len(drone_map["drone_num"]) == 1
                ):
                    zone = Parser.parse_zone(
                        line.strip(), drone_map["drone_num"][0]
                    )
                    drone_map["end"] = [zone]
                    drone_map["nodes"].append(zone)
                elif (
                    line.startswith("hub:")
                    and len(drone_map["drone_num"]) == 1
                ):
                    drone_map["nodes"].append(
                        Parser.parse_zone(
                            line.strip(), drone_map["drone_num"][0]
                        )
                    )
                elif (
                    line.startswith("connection:")
                    and len(drone_map["drone_num"]) == 1
                ):
                    drone_map["links"].append(Parser.parse_link(line.strip()))
                else:
                    raise ParserError(f"{line.strip()} is not a valid line!")
        return drone_map

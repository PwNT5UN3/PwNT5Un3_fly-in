import enum


class ZoneType(str, enum.Enum):
    NORMAL = "normal"
    PRIO = "priority"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"


class Zone:
    def __init__(
        self,
        name: str,
        x: int,
        y: int,
        zone_type: ZoneType,
        color: str,
        drone_cap: int,
    ) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.type = zone_type
        self.color = color
        self.drone_cap = drone_cap

    def get_zone_cost(self) -> float:
        if self.type == ZoneType.BLOCKED:
            return 10000000
        elif self.type == ZoneType.RESTRICTED:
            return 2
        else:
            return 1 - (int(self.type == ZoneType.PRIO) / 100)

    def is_blocked(self) -> bool:
        return self.type == ZoneType.RESTRICTED


class Connection:
    def __init__(self, zone_1: str, zone_2: str, capacity: int = 1) -> None:
        if capacity <= 0:
            raise ValueError("Warning: link capacity cannot be less than 1")
        if zone_1 == zone_2:
            raise ValueError("Zones cannot be identical")
        self.zone_1 = zone_1
        self.zone_2 = zone_2
        self.cap = capacity

    def get_linked_zones(self) -> tuple[str, str]:
        return (self.zone_1, self.zone_2)


class Graph:
    def __init__(self) -> None:
        self.nodes: dict[str, Zone] = {}
        self.connections: dict[tuple[str, str], Connection] = {}
        self.links: dict[str, list[str]] = {}
        self.start_node: Zone | None = None
        self.end_node: Zone | None = None
    
    def add_zone(self, zone: Zone) -> None:
        if self.nodes.get(zone.name) is not None:
            raise ValueError(f"Zone {zone.name} already exists!")
        self.nodes[zone.name] = zone
        self.links[zone.name] = list()
    
    def add_connection(self, connection: Connection) -> None:
        if connection in self.connections.values():
            raise ValueError(f"Connection between {connection.zone_1} and " +
                             f"{connection.zone_2} already exists!")
        if connection.zone_1 not in self.nodes \
            or connection.zone_2 not in self.nodes:
            raise ValueError("Both zones need to exist for a valid connection")
        self.connections[(connection.zone_1, connection.zone_2)] = connection
        self.connections[(connection.zone_2, connection.zone_1)] = connection
        self.links[connection.zone_1].append(connection.zone_2)
        self.links[connection.zone_2].append(connection.zone_1)
    
    def get_links(self, zone: str) -> list | None:
        return self.links.get(zone)
    
    def get_zone(self, name: str) -> Zone | None:
        return self.nodes.get(name)
    
    def get_connection(self, zone_1: str, zone_2: str) -> Connection | None:
        return self.connections.get((zone_1, zone_2))
    
    def get_all_zones(self) -> list:
        return list(self.nodes.values())
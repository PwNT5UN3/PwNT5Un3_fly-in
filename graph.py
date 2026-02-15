import enum

class ZoneType(enum.Enum, str):
    NORMAL = "normal"
    PRIO = "priority"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"

class Zone:
    def __init__(self,
                 name: str,
                 x: int,
                 y: int,
                 zone_type: ZoneType,
                 color: str,
                 drone_cap: int) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.type = zone_type
        self.color = color
        self.drone_cap = drone_cap
    
    def get_zone_cost(self):
        if self.type == ZoneType.BLOCKED:
            return 10000000
        elif self.type == ZoneType.RESTRICTED:
            return 2
        else 